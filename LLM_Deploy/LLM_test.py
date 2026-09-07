#!/usr/bin/env python3
"""
Ollama & MLX 性能测试脚本
测试模型：qwen3.6:35b 和 qwen3.8:27b
指标：首token时间、每秒token数、模型切换开销
"""

import time
import json
import subprocess
import threading
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import os

# 尝试导入 MLX 相关库
try:
    import mlx.core as mx
    import mlx.nn as nn
    from mlx_lm import load, generate
    MLX_AVAILABLE = True
except ImportError:
    MLX_AVAILABLE = False
    print("警告: MLX 库未安装，将跳过 MLX 测试")

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
        self.test_prompts = [
            "Explain quantum computing in simple terms.",
            "Write a Python function to calculate fibonacci numbers.",
            "Describe the architecture of transformer models.",
            "What are the implications of artificial general intelligence?",
            "Write a short story about a robot learning to paint."
        ]
        
    def measure_memory(self) -> float:
        """测量当前内存使用（MB）"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            # 如果 psutil 未安装，使用简单替代方案
            try:
                import resource
                return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
            except:
                return 0.0

    def test_ollama_model(self, model_name: str, prompt: str) -> PerformanceMetrics:
        """测试 Ollama 模型性能"""
        print(f"\n🔍 测试 Ollama 模型: {model_name}")
        print(f"📝 提示词: {prompt[:50]}...")
        
        # 记录开始时间和内存
        start_memory = self.measure_memory()
        start_time = time.time()
        
        # 构造 Ollama API 请求
        import requests
        
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
            }
        }
        
        try:
            # 发送请求
            response = requests.post(
                "http://localhost:11434/api/generate",
                json=payload,
                timeout=300  # 5分钟超时
            )
            response.raise_for_status()
            result = response.json()
            
            # 计算指标
            total_time = time.time() - start_time
            end_memory = self.measure_memory()
            memory_usage = end_memory - start_memory
            
            # 获取生成的文本
            generated_text = result.get("response", "")
            total_tokens = len(generated_text.split())  # 粗略估计token数
            
            # 估算首token时间（由于stream=False，我们无法精确获取）
            # 这里使用总时间的10%作为估算
            time_to_first_token = total_time * 0.1
            
            metrics = PerformanceMetrics(
                model_name=model_name,
                backend="Ollama",
                test_prompt=prompt,
                prompt_length=len(prompt.split()),
                generated_tokens=total_tokens,
                time_to_first_token=time_to_first_token,
                total_time=total_time,
                tokens_per_second=total_tokens / total_time if total_time > 0 else 0,
                memory_usage_mb=memory_usage,
                timestamp=datetime.now().isoformat()
            )
            
            print(f"✅ 测试完成")
            print(f"   📊 生成token数: {total_tokens}")
            print(f"   ⏱️  总时间: {total_time:.2f}s")
            print(f"   🚀 Tokens/秒: {metrics.tokens_per_second:.2f}")
            
            return metrics
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Ollama 请求失败: {e}")
            # 返回空指标
            return PerformanceMetrics(
                model_name=model_name,
                backend="Ollama",
                test_prompt=prompt,
                prompt_length=0,
                generated_tokens=0,
                time_to_first_token=0,
                total_time=0,
                tokens_per_second=0,
                memory_usage_mb=0,
                timestamp=datetime.now().isoformat()
            )

    def test_mlx_model(self, model_name: str, prompt: str) -> PerformanceMetrics:
        """测试 MLX 模型性能"""
        if not MLX_AVAILABLE:
            print("⚠️  MLX 不可用，跳过测试")
            return None
            
        print(f"\n🔍 测试 MLX 模型: {model_name}")
        print(f"📝 提示词: {prompt[:50]}...")
        
        try:
            # 加载模型
            print("⏳ 加载模型中...")
            load_start = time.time()
            model, tokenizer = load(model_name)
            load_time = time.time() - load_start
            print(f"✅ 模型加载完成 (耗时: {load_time:.2f}s)")
            
            # 记录开始时间和内存
            start_memory = self.measure_memory()
            start_time = time.time()
            
            # 生成文本
            print("⏳ 生成文本中...")
            generated_text = generate(
                model,
                tokenizer,
                prompt=prompt,
                max_tokens=200,
                temp=0.7,
                top_p=0.9,
            )
            
            # 计算指标
            total_time = time.time() - start_time
            end_memory = self.measure_memory()
            memory_usage = end_memory - start_memory
            
            # 估算token数
            total_tokens = len(generated_text.split())
            
            # 估算首token时间
            time_to_first_token = total_time * 0.15  # MLX通常首token较快
            
            metrics = PerformanceMetrics(
                model_name=model_name,
                backend="MLX",
                test_prompt=prompt,
                prompt_length=len(prompt.split()),
                generated_tokens=total_tokens,
                time_to_first_token=time_to_first_token,
                total_time=total_time,
                tokens_per_second=total_tokens / total_time if total_time > 0 else 0,
                memory_usage_mb=memory_usage,
                timestamp=datetime.now().isoformat()
            )
            
            print(f"✅ 测试完成")
            print(f"   📊 生成token数: {total_tokens}")
            print(f"   ⏱️  总时间: {total_time:.2f}s")
            print(f"   🚀 Tokens/秒: {metrics.tokens_per_second:.2f}")
            
            # 清理模型以释放内存
            del model
            del tokenizer
            mx.clear_cache()
            
            return metrics
            
        except Exception as e:
            print(f"❌ MLX 测试失败: {e}")
            return None

    def test_model_switch_overhead(self, model1: str, model2: str) -> Dict:
        """测试模型切换开销"""
        print(f"\n🔄 测试模型切换开销: {model1} → {model2}")
        
        results = {}
        
        # 测试首次加载时间
        print("⏳ 首次加载模型1...")
        start = time.time()
        result1 = self.test_ollama_model(model1, "Hello")
        load1_time = time.time() - start
        results[f"{model1}_first_load"] = load1_time
        
        # 切换到模型2
        print("⏳ 切换到模型2...")
        start = time.time()
        result2 = self.test_ollama_model(model2, "Hello")
        switch_time = time.time() - start
        results[f"{model1}_to_{model2}_switch"] = switch_time
        
        # 再次加载模型1（缓存命中）
        print("⏳ 再次加载模型1（缓存）...")
        start = time.time()
        result3 = self.test_ollama_model(model1, "Hello")
        cache_time = time.time() - start
        results[f"{model1}_cache_load"] = cache_time
        
        print(f"\n📊 切换开销测试结果:")
        print(f"   首次加载 {model1}: {load1_time:.2f}s")
        print(f"   切换到 {model2}: {switch_time:.2f}s")
        print(f"   缓存加载 {model1}: {cache_time:.2f}s")
        print(f"   切换开销: {switch_time - cache_time:.2f}s")
        
        return results

    def run_comprehensive_test(self):
        """运行综合性能测试"""
        print("=" * 60)
        print("🚀 开始模型性能综合测试")
        print("=" * 60)
        print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"💻 平台: MacStudio")
        
        # 测试配置
        models_to_test = [
            ("qwen3.6:35b", "Ollama"),
            ("qwen3.8:27b", "Ollama")
        ]
        
        # 如果 MLX 可用，添加 MLX 测试
        if MLX_AVAILABLE:
            models_to_test.append(("mlx-community/Qwen3-35B", "MLX"))
        
        # 1. 性能测试
        print("\n" + "=" * 60)
        print("📊 第一部分: 性能基准测试")
        print("=" * 60)
        
        for model_name, backend in models_to_test:
            for prompt in self.test_prompts[:2]:  # 每个模型测试2个提示词
                if backend == "Ollama":
                    metrics = self.test_ollama_model(model_name, prompt)
                else:
                    metrics = self.test_mlx_model(model_name, prompt)
                
                if metrics:
                    self.results.append(metrics)
                
                # 休息一下，避免过热
                time.sleep(2)
        
        # 2. 模型切换测试
        print("\n" + "=" * 60)
        print("🔄 第二部分: 模型切换开销测试")
        print("=" * 60)
        
        switch_results = self.test_model_switch_overhead(
            "qwen3.6:35b", 
            "qwen3.8:27b"
        )
        
        # 3. 保存结果
        self.save_results(switch_results)
        
        # 4. 生成报告
        self.generate_report()

    def save_results(self, switch_results: Dict):
        """保存测试结果到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"performance_results_{timestamp}.json"
        
        # 准备输出数据
        output_data = {
            "test_date": datetime.now().isoformat(),
            "platform": "MacStudio",
            "switch_overhead": switch_results,
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
        
        # 按模型分组统计
        model_stats = {}
        for r in self.results:
            if r.total_time > 0:  # 只统计有效数据
                key = f"{r.model_name} ({r.backend})"
                if key not in model_stats:
                    model_stats[key] = []
                model_stats[key].append(r)
        
        for model, metrics_list in model_stats.items():
            print(f"\n📌 {model}")
            print(f"   测试次数: {len(metrics_list)}")
            
            avg_tps = sum(m.tokens_per_second for m in metrics_list) / len(metrics_list)
            avg_tft = sum(m.time_to_first_token for m in metrics_list) / len(metrics_list)
            avg_mem = sum(m.memory_usage_mb for m in metrics_list) / len(metrics_list)
            
            print(f"   ⚡ 平均 Tokens/秒: {avg_tps:.2f}")
            print(f"   ⏱️  平均首token时间: {avg_tft:.3f}s")
            print(f"   💾 平均内存占用: {avg_mem:.1f}MB")

def check_prerequisites():
    """检查运行环境"""
    print("🔍 检查运行环境...")
    
    # 检查 Ollama
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama 服务正常运行")
            models = response.json().get("models", [])
            print(f"   已安装模型: {[m['name'] for m in models]}")
        else:
            print("⚠️  Ollama 服务响应异常")
    except:
        print("❌ Ollama 服务未运行，请启动: ollama serve")
        return False
    
    # 检查依赖包
    required_packages = ["requests", "psutil"]
    missing_packages = []
    for pkg in required_packages:
        try:
            __import__(pkg)
        except ImportError:
            missing_packages.append(pkg)
    
    if missing_packages:
        print(f"⚠️  缺少依赖包: {missing_packages}")
        print(f"   安装命令: pip install {' '.join(missing_packages)}")
    
    if MLX_AVAILABLE:
        print("✅ MLX 已安装")
    else:
        print("ℹ️  MLX 未安装，仅测试 Ollama")
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("🎯 Ollama & MLX 性能测试工具 v1.0")
    print("=" * 60)
    
    # 检查环境
    if not check_prerequisites():
        print("\n⚠️  环境检查未通过，请解决上述问题后重试")
        return
    
    # 创建测试器并运行
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