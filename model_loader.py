"""
模型加载器 - 智能设备选择和Qwen2.5-0.5B模型初始化
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import Tuple
import os


def get_device():
    """
    设备优先次序：GPU -> MPS -> CPU
    """
    if torch.cuda.is_available():
        device = "cuda"
        print(f"✓ 使用 NVIDIA GPU: {torch.cuda.get_device_name(0)}")
    elif torch.backends.mps.is_available():
        device = "mps"
        print("✓ 使用 Apple MPS 加速")
    else:
        device = "cpu"
        print("✓ 使用 CPU (性能较低)")
    
    return device


def load_qwen_model(model_name: str = "Qwen/Qwen2.5-0.5B-Instruct") -> Tuple:
    """
    加载Qwen2.5-0.5B-Instruct模型
    
    Args:
        model_name: 模型名称/路径
        
    Returns:
        (model, tokenizer, device)
    """
    device = get_device()
    
    print(f"\n加载模型: {model_name}")
    
    # 设置模型加载选项
    torch_dtype = torch.float16 if device == "cuda" else torch.float32
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch_dtype,
            device_map=device if device == "cuda" else None,
        )
        
        if device != "cuda":
            model = model.to(device)
        
        model.eval()
        print("✓ 模型加载成功")
        
    except Exception as e:
        print(f"✗ 模型加载失败: {e}")
        print(f"  请确保模型已下载到本地或网络连接正常")
        raise
    
    return model, tokenizer, device


def generate_response(
    model,
    tokenizer,
    prompt: str,
    device: str,
    max_new_tokens: int = 512,
    temperature: float = 0.7,
    top_p: float = 0.9,
) -> str:
    """
    使用模型生成响应
    
    Args:
        model: 模型实例
        tokenizer: 分词器
        prompt: 输入提示词
        device: 设备
        max_new_tokens: 最大生成token数
        temperature: 温度参数
        top_p: top-p采样参数
        
    Returns:
        生成的文本
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # 移除输入部分，只返回生成的内容
    response = response[len(prompt):].strip()
    
    return response
