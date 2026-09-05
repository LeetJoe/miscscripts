import gc
import json
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from mlx_lm import load, stream_generate
import mxnet as mx  # MLX 内部显存管理

app = FastAPI(title="MLX Multi-Model Dynamic Gateway")

# 1. 映射应用请求的 model 名称到本地 MLX 权重路径
MODEL_MAP = {
    "qwen3.6-instruct": "mlx-community/Qwen3.6-35B-Instruct-4bit",
    "qwen3-coder": "mlx-community/Qwen3-Coder-30B-A3B-4bit",
    "default": "mlx-community/Qwen3.6-35B-Instruct-4bit"
}

# 全局变量记录当前活跃的模型与 tokenizer
CURRENT_MODEL_NAME = None
CURRENT_MODEL = None
CURRENT_TOKENIZER = None

def get_or_load_model(model_alias: str):
    global CURRENT_MODEL_NAME, CURRENT_MODEL, CURRENT_TOKENIZER
    
    target_path = MODEL_MAP.get(model_alias, MODEL_MAP["default"])
    
    # 如果请求的就是当前已加载的模型，直接重用
    if CURRENT_MODEL_NAME == target_path:
        return CURRENT_MODEL, CURRENT_TOKENIZER

    print(f"🔄 [动态切换] 正在卸载旧模型 ({CURRENT_MODEL_NAME})，准备加载: {target_path}...")
    
    # 2. 显式释放旧模型内存
    CURRENT_MODEL = None
    CURRENT_TOKENIZER = None
    CURRENT_MODEL_NAME = None
    
    gc.collect()
    # 强制清理 MLX 显存缓存 (针对 mlx 内置内存池)
    if hasattr(mx, "eval"):
        pass # MLX 自动管理，通过 gc 清除 Python 引用即可

    # 3. 加载新模型
    start_time = time.time()
    CURRENT_MODEL, CURRENT_TOKENIZER = load(target_path)
    CURRENT_MODEL_NAME = target_path
    print(f"✅ [加载完成] 耗时: {time.time() - start_time:.2f}s")
    
    return CURRENT_MODEL, CURRENT_TOKENIZER

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    requested_model = body.get("model", "default")
    messages = body.get("messages", [])
    stream = body.get("stream", False)

    # 动态获取/切换模型
    try:
        model, tokenizer = get_or_load_model(requested_model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模型加载失败: {str(e)}")

    # 使用 Chat Template 格式化 Prompt
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    # 简化的流式返回实现 (OpenAI SSE 格式)
    def event_generator():
        for chunk in stream_generate(model, tokenizer, prompt, max_tokens=2048):
            data = {
                "choices": [{
                    "delta": {"content": chunk.text},
                    "finish_reason": None
                }]
            }
            yield f"data: {json.dumps(data)}\n\n"
        yield "data: [DONE]\n\n"

    if stream:
        return StreamingResponse(event_generator(), media_type="text/event-stream")
    else:
        # 非流式直接拼接返回
        response_text = "".join([chunk.text for chunk in stream_generate(model, tokenizer, prompt)])
        return {
            "choices": [{
                "message": {"role": "assistant", "content": response_text},
                "finish_reason": "stop"
            }]
        }

if __name__ == "__main__":
    import uvicorn
    # 监听统一端口
    uvicorn.run(app, host="0.0.0.0", port=8000)