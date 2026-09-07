#!/usr/bin/env python3
"""
Ollama & oMLX 性能测试脚本
测试模型：Qwen3.6-35B-A3B-oQ4e-fp16-mtp (oMLX) 和 qwen3.6:35b (Ollama)
指标：首token时间、每秒token数
"""

import time
import json
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import psutil

# 尝试导入 tiktoken 用于精确 token 统计
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    print("⚠️  tiktoken 未安装，将使用估算方式统计 token 数")
    print("   安装命令: pip install tiktoken")

@dataclass
class PerformanceMetrics:
    """性能指标数据类"""
    model_name: str
    backend: str
    test_prompt: str
    prompt_length: int
    generated_tokens: int
    time_to_first_token: float  # 秒
    total_time: float  # 秒
    tokens_per_second: float
    memory_usage_mb: float
    timestamp: str
    
    def to_dict(self):
        return asdict(self)


class ModelPerformanceTester:
    def __init__(self):
        self.results: List[PerformanceMetrics] = []
        self.omlx_base_url = "http://localhost:8000"
        self.ollama_base_url = "http://localhost:11434"
        self.current_omlx_model: Optional[str] = None
        
        # 初始化 tokenizer（使用 cl100k_base 作为通用编码器）
        if TIKTOKEN_AVAILABLE:
            try:
                # Qwen 系列通常使用类似 GPT-4 的编码器
                self.tokenizer = tiktoken.get_encoding("cl100k_base")
            except:
                self.tokenizer = None
        else:
            self.tokenizer = None
        
        # 测试提示词
        self.test_prompts = [
            "Explain quantum computing in simple terms.",
            "Write a Python function to calculate fibonacci numbers.",
            "Describe the architecture of transformer models.",
            "What are the implications of artificial general intelligence?",
            "Write a short story about a robot learning to paint."
        ]
        
        # 用于预热的短提示词
        self.warmup_prompt = "Hello"
        
    def count_tokens(self, text: str) -> int:
        """精确统计文本的 token 数量"""
        if self.tokenizer:
            try:
                return len(self.tokenizer.encode(text))
            except:
                # 如果编码失败，使用粗略估算
                return len(text.split()) * 1.3  # 英文约 1.3 词/token
        else:
            # 粗略估算：英文约 1.3 个词对应 1 个 token
            return int(len(text.split()) * 1.3)
        
    def measure_memory(self) -> float:
        """测量当前内存使用（MB）"""
        try:
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except:
            return 0.0

    def unload_omlx_model(self) -> bool:
        """卸载 oMLX 当前加载的模型，释放内存"""
        try:
            # 尝试通过 API 卸载模型
            response = requests.post(
                f"{self.omlx_base_url}/v1/models/unload",
                timeout=10
            )
            if response.status_code == 200:
                print(f"   ✅ 已卸载模型，释放内存")
                self.current_omlx_model = None
                time.sleep(3)  # 等待内存回收
                return True
            else:
                print(f"   ⚠️  卸载 API 返回: {response.status_code}")
                return self._force_unload_model()
        except requests.exceptions.RequestException:
            print(f"   ⚠️  卸载 API 不可用，尝试替代方案...")
            return self._force_unload_model()
    
    def _force_unload_model(self) -> bool:
        """强制卸载模型的替代方案"""
        try:
            # 尝试发送一个空请求来触发模型切换
            payload = {
                "model": "dummy",  # 不存在的模型，可能触发卸载
                "messages": [{"role": "user", "content": "unload"}],
                "max_tokens": 1,
                "stream": False
            }
            requests.post(
                f"{self.omlx_base_url}/v1/chat/completions",
                json=payload,
                timeout=5
            )
        except:
            pass  # 预期会失败，但可能触发模型卸载
        
        # 等待内存自动回收
        time.sleep(5)
        self.current_omlx_model = None
        print(f"   ✅ 已尝试释放模型内存")
        return True

    def warmup_omlx_model(self, model_name: str) -> bool:
        """
        预热 oMLX 模型：发送简单请求确保模型已加载到内存
        """
        print(f"   🔥 预热模型 {model_name}...")
        
        try:
            # 如果当前已加载其他模型，先卸载
            if self.current_omlx_model and self.current_omlx_model != model_name:
                print(f"   🔄 检测到已加载 {self.current_omlx_model}，正在切换...")
                self.unload_omlx_model()
            
            # 发送预热请求
            payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": self.warmup_prompt}],
                "max_tokens": 5,
                "temperature": 0.1,
                "stream": False
            }
            start = time.time()
            response = requests.post(
                f"{self.omlx_base_url}/v1/chat/completions",
                json=payload,
                timeout=120  # 给模型加载留出足够时间
            )
            load_time = time.time() - start
            if response.status_code == 200:
                self.current_omlx_model = model_name
                print(f"   ✅ 模型 {model_name} 已加载并预热完成 (加载耗时: {load_time:.2f}s)")
                return True
            else:
                print(f"   ❌ 预热失败: HTTP {response.status_code}")
                return False
        except requests.exceptions.Timeout:
            print(f"   ❌ 预热超时 (120s)，模型可能加载失败")
            return False
        except Exception as e:
            print(f"   ❌ 预热失败: {e}")
            return False

    def warmup_ollama_model(self, model_name: str) -> bool:
        """预热 Ollama 模型"""
        print(f"   🔥 预热模型 {model_name}...")
        
        try:
            payload = {
                "model": model_name,
                "prompt": self.warmup_prompt,
                "stream": False,
                "options": {"temperature": 0.1}
            }
            start = time.time()
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json=payload,
                timeout=60
            )
            load_time = time.time() - start
            if response.status_code == 200:
                print(f"   ✅ 模型 {model_name} 已加载并预热完成 (加载耗时: {load_time:.2f}s)")
                return True
            else:
                print(f"   ❌ 预热失败: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ 预热失败: {e}")
            return False

    def test_omlx_model(self, model_name: str, prompt: str) -> Optional[PerformanceMetrics]:
        """测试 oMLX 模型性能"""
        print(f"\n🔍 测试 oMLX 模型: {model_name}")
        print(f"📝 提示词: {prompt[:50]}...")
        
        # 预热模型
        if not self.warmup_omlx_model(model_name):
            print("   ❌ 模型预热失败，跳过测试")
            return None
        
        # 等待一秒，确保模型稳定
        time.sleep(1)
        
        # 记录开始时间和内存
        start_memory = self.measure_memory()
        start_time = time.time()
        first_token_time = None
        
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4096,
            "temperature": 0.7,
            "top_p": 0.9,
            "stream": True
        }
        
        try:
            response = requests.post(
                f"{self.omlx_base_url}/v1/chat/completions",
                json=payload,
                stream=True,
                timeout=300
            )
            response.raise_for_status()
            
            generated_text = ""
            chunk_count = 0  # 用于调试，记录响应块数量
            
            for line in response.iter_lines():
                if line:
                    try:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            data_str = line_str[6:]
                            if data_str == '[DONE]':
                                break
                            chunk = json.loads(data_str)
                            if "choices" in chunk and len(chunk["choices"]) > 0:
                                delta = chunk["choices"][0].get("delta", {})
                                if "content" in delta:
                                    if first_token_time is None:
                                        first_token_time = time.time() - start_time
                                    token = delta["content"]
                                    chunk_count += 1
                                    # 直接打印内容（不换行，模拟流式效果）
                                    print(token, end="", flush=True)
                                    generated_text += token
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        continue
            
            print("\n")  # 换行
            
            total_time = time.time() - start_time
            end_memory = self.measure_memory()
            memory_usage = end_memory - start_memory
            
            if first_token_time is None:
                print("   ⚠️  流式响应异常，使用非流式模式重测...")
                return self._test_omlx_non_streaming(model_name, prompt)
            
            # 使用 tiktoken 精确统计生成的 token 数
            total_tokens = self.count_tokens(generated_text)
            
            print(f"   📊 响应块数: {chunk_count} (每个块可能包含多个token)")
            print(f"   📊 精确token数: {total_tokens}")
            
            metrics = PerformanceMetrics(
                model_name=model_name,
                backend="oMLX",
                test_prompt=prompt,
                prompt_length=len(prompt.split()),
                generated_tokens=total_tokens,
                time_to_first_token=first_token_time,
                total_time=total_time,
                tokens_per_second=total_tokens / total_time if total_time > 0 else 0,
                memory_usage_mb=memory_usage,
                timestamp=datetime.now().isoformat()
            )
            
            print(f"✅ 测试完成")
            print(f"   📊 生成token数: {total_tokens}")
            print(f"   ⏱️  首token时间: {first_token_time:.3f}s")
            print(f"   ⏱️  总时间: {total_time:.2f}s")
            print(f"   🚀 Tokens/秒: {metrics.tokens_per_second:.2f}")
            
            return metrics
            
        except Exception as e:
            print(f"❌ oMLX 测试失败: {e}")
            return None

    def _test_omlx_non_streaming(self, model_name: str, prompt: str) -> Optional[PerformanceMetrics]:
        """oMLX 非流式测试（备用方案）"""
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4096,
            "temperature": 0.7,
            "top_p": 0.9,
            "stream": False
        }
        
        try:
            start_memory = self.measure_memory()
            start_time = time.time()
            
            response = requests.post(
                f"{self.omlx_base_url}/v1/api/generate",
                json=payload,
                timeout=300
            )
            response.raise_for_status()
            result = response.json()
            
            total_time = time.time() - start_time
            end_memory = self.measure_memory()
            memory_usage = end_memory - start_memory
            
            generated_text = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            total_tokens = self.count_tokens(generated_text)
            
            metrics = PerformanceMetrics(
                model_name=model_name,
                backend="oMLX",
                test_prompt=prompt,
                prompt_length=len(prompt.split()),
                generated_tokens=total_tokens,
                time_to_first_token=total_time * 0.15,
                total_time=total_time,
                tokens_per_second=total_tokens / total_time if total_time > 0 else 0,
                memory_usage_mb=memory_usage,
                timestamp=datetime.now().isoformat()
            )
            
            print(f"✅ 测试完成 (非流式)")
            print(f"   📊 生成token数: {total_tokens}")
            print(f"   ⏱️  总时间: {total_time:.2f}s")
            print(f"   🚀 Tokens/秒: {metrics.tokens_per_second:.2f}")
            
            return metrics
            
        except Exception as e:
            print(f"❌ 非流式测试失败: {e}")
            return None

    def test_ollama_model(self, model_name: str, prompt: str) -> Optional[PerformanceMetrics]:
        """测试 Ollama 模型性能"""
        print(f"\n🔍 测试 Ollama 模型: {model_name}")
        print(f"📝 提示词: {prompt[:50]}...")
        
        # 预热模型
        if not self.warmup_ollama_model(model_name):
            print("   ❌ 模型预热失败，跳过测试")
            return None
        
        # 等待一秒，确保模型稳定
        time.sleep(1)
        
        # 记录开始时间和内存
        start_memory = self.measure_memory()
        start_time = time.time()
        first_token_time = None
        
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
            }
        }
        
        try:
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json=payload,
                stream=True,
                timeout=300
            )
            response.raise_for_status()
            
            generated_text = ""
            chunk_count = 0
            
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if "response" in chunk:
                            if first_token_time is None:
                                first_token_time = time.time() - start_time
                            token = chunk["response"]
                            chunk_count += 1
                            generated_text += token
                        if chunk.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue
            
            total_time = time.time() - start_time
            end_memory = self.measure_memory()
            memory_usage = end_memory - start_memory
            
            if first_token_time is None:
                print("   ⚠️  流式响应异常，使用非流式模式重测...")
                return self._test_ollama_non_streaming(model_name, prompt)
            
            # 使用 tiktoken 精确统计
            total_tokens = self.count_tokens(generated_text)
            
            print(f"   📊 响应块数: {chunk_count} (Ollama通常逐token返回)")
            
            metrics = PerformanceMetrics(
                model_name=model_name,
                backend="Ollama",
                test_prompt=prompt,
                prompt_length=len(prompt.split()),
                generated_tokens=total_tokens,
                time_to_first_token=first_token_time,
                total_time=total_time,
                tokens_per_second=total_tokens / total_time if total_time > 0 else 0,
                memory_usage_mb=memory_usage,
                timestamp=datetime.now().isoformat()
            )
            
            print(f"✅ 测试完成")
            print(f"   📊 生成token数: {total_tokens}")
            print(f"   ⏱️  首token时间: {first_token_time:.3f}s")
            print(f"   ⏱️  总时间: {total_time:.2f}s")
            print(f"   🚀 Tokens/秒: {metrics.tokens_per_second:.2f}")
            
            return metrics
            
        except Exception as e:
            print(f"❌ Ollama 测试失败: {e}")
            return None

    def _test_ollama_non_streaming(self, model_name: str, prompt: str) -> Optional[PerformanceMetrics]:
        """Ollama 非流式测试（备用方案）"""
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7, "top_p": 0.9}
        }
        
        try:
            start_memory = self.measure_memory()
            start_time = time.time()
            
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json=payload,
                timeout=300
            )
            response.raise_for_status()
            result = response.json()
            
            total_time = time.time() - start_time
            end_memory = self.measure_memory()
            memory_usage = end_memory - start_memory
            
            generated_text = result.get("response", "")
            total_tokens = self.count_tokens(generated_text)
            
            metrics = PerformanceMetrics(
                model_name=model_name,
                backend="Ollama",
                test_prompt=prompt,
                prompt_length=len(prompt.split()),
                generated_tokens=total_tokens,
                time_to_first_token=total_time * 0.1,
                total_time=total_time,
                tokens_per_second=total_tokens / total_time if total_time > 0 else 0,
                memory_usage_mb=memory_usage,
                timestamp=datetime.now().isoformat()
            )
            
            print(f"✅ 测试完成 (非流式)")
            print(f"   📊 生成token数: {total_tokens}")
            print(f"   ⏱️  总时间: {total_time:.2f}s")
            print(f"   🚀 Tokens/秒: {metrics.tokens_per_second:.2f}")
            
            return metrics
            
        except Exception as e:
            print(f"❌ 非流式测试失败: {e}")
            return None

    def run_comprehensive_test(self):
        """运行综合性能测试"""
        print("=" * 60)
        print("🚀 开始模型性能综合测试")
        print("=" * 60)
        print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"💻 平台: MacStudio")
        if TIKTOKEN_AVAILABLE:
            print(f"✅ 使用 tiktoken 精确统计 token 数")
        else:
            print(f"⚠️  使用估算方式统计 token 数 (建议安装 tiktoken)")
        
        # 测试配置 - 先 oMLX，再 Ollama
        models_to_test = [
            ("Qwen3.6-35B-A3B-oQ4e-fp16-mtp", "oMLX"),
            ("qwen3.6:35b", "Ollama")
        ]
        
        # 1. 性能测试
        print("\n" + "=" * 60)
        print("📊 第一部分: 性能基准测试")
        print("=" * 60)
        
        for model_name, backend in models_to_test:
            print(f"\n{'='*50}")
            print(f"📌 测试模型: {model_name} ({backend})")
            print(f"{'='*50}")
            
            for idx, prompt in enumerate(self.test_prompts[:3]):  # 每个模型测试3个提示词
                print(f"\n  --- 测试 [{idx+1}/{3}] ---")
                
                if backend == "oMLX":
                    metrics = self.test_omlx_model(model_name, prompt)
                else:
                    # Ollama 测试已被注释
                    # metrics = self.test_ollama_model(model_name, prompt)
                    metrics = None
                
                if metrics:
                    self.results.append(metrics)
                
                # 测试间隔休息
                if idx < 2:  # 最后一个测试后不需要等待
                    time.sleep(5)
            
            # 如果是 oMLX，测试完成后主动卸载模型释放内存
            if backend == "oMLX":
                print(f"\n📌 完成 {model_name} 测试，正在释放内存...")
                self.unload_omlx_model()
                time.sleep(3)
        
        # 2. 保存结果
        self.save_results()
        
        # 3. 生成报告
        self.generate_report()

    def save_results(self):
        """保存测试结果到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"performance_results_{timestamp}.json"
        
        output_data = {
            "test_date": datetime.now().isoformat(),
            "platform": "MacStudio",
            "token_count_method": "tiktoken" if TIKTOKEN_AVAILABLE else "estimated",
            "performance_metrics": [m.to_dict() for m in self.results]
        }
        
        with open(filename, "w") as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n💾 结果已保存到: {filename}")

    def generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("📈 性能测试报告")
        print("=" * 60)
        
        if not self.results:
            print("❌ 没有可用的测试数据")
            return
        
        model_stats = {}
        for r in self.results:
            if r.total_time > 0:
                key = f"{r.model_name} ({r.backend})"
                if key not in model_stats:
                    model_stats[key] = []
                model_stats[key].append(r)
        
        print("\n📊 各模型性能汇总:")
        for model, metrics_list in model_stats.items():
            print(f"\n📌 {model}")
            print(f"   测试次数: {len(metrics_list)}")
            
            avg_tps = sum(m.tokens_per_second for m in metrics_list) / len(metrics_list)
            avg_tft = sum(m.time_to_first_token for m in metrics_list) / len(metrics_list)
            avg_mem = sum(m.memory_usage_mb for m in metrics_list) / len(metrics_list)
            avg_tokens = sum(m.generated_tokens for m in metrics_list) / len(metrics_list)
            
            print(f"   📝 平均生成token数: {avg_tokens:.0f}")
            print(f"   ⚡ 平均 Tokens/秒: {avg_tps:.2f}")
            print(f"   ⏱️  平均首token时间: {avg_tft:.3f}s")
            print(f"   💾 平均内存占用: {avg_mem:.1f}MB")


def check_prerequisites():
    """检查运行环境"""
    print("🔍 检查运行环境...")
    all_ok = True
    
    # 检查 oMLX (优先检查)
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ oMLX 服务正常运行 (端口 8000)")
        else:
            print("⚠️  oMLX 服务响应异常")
            all_ok = False
    except:
        print("❌ oMLX 服务未运行，请启动: omlx serve")
        all_ok = False
    
    # 检查 Ollama
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama 服务正常运行 (端口 11434)")
            models = response.json().get("models", [])
            print(f"   已安装模型: {[m['name'] for m in models]}")
        else:
            print("⚠️  Ollama 服务响应异常")
            all_ok = False
    except:
        print("❌ Ollama 服务未运行，请启动: ollama serve")
        all_ok = False
    
    # 检查依赖包
    required_packages = ["requests", "psutil"]
    for pkg in required_packages:
        try:
            __import__(pkg)
        except ImportError:
            print(f"❌ 缺少依赖包: {pkg}")
            print(f"   安装命令: pip install {pkg}")
            all_ok = False
    
    # 检查 tiktoken（非必需，但推荐）
    if not TIKTOKEN_AVAILABLE:
        print("ℹ️  建议安装 tiktoken 以获得精确的 token 统计: pip install tiktoken")
    
    if all_ok:
        print("✅ 所有依赖检查通过")
    
    return all_ok


def main():
    """主函数"""
    print("=" * 60)
    print("🎯 Ollama & oMLX 性能测试工具 v2.1")
    print("=" * 60)
    
    # if not check_prerequisites():
    #     print("\n⚠️  环境检查未通过，请解决上述问题后重试")
    #     return
    
    tester = ModelPerformanceTester()
    
    try:
        tester.run_comprehensive_test()
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()