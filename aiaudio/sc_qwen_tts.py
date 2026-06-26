import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

# 加载已安装的模型
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    device_map="cuda:0",
    dtype=torch.bfloat16,
)

# 生成保留原音色的中文音频
wavs, sr = model.generate_custom_voice(
    text="你翻译好的中文文本",
    language="Chinese",
    ref_audio_path="./HC.mp3"
)

# 导出结果
sf.write("output_chinese.wav", wavs, sr)
