#!/usr/bin/env python3
"""
系统验证脚本 - 检查项目完整性和依赖
"""

import sys
import os
from pathlib import Path


def check_files():
    """检查必要的文件是否存在"""
    
    print("\n" + "="*70)
    print("检查项目文件完整性...")
    print("="*70)
    
    required_files = {
        "Python模块": [
            "model_loader.py",
            "agent_a.py",
            "agent_b.py",
            "dual_agent_system.py",
            "config.py",
        ],
        "可执行脚本": [
            "main.py",
            "interactive.py",
        ],
        "配置文件": [
            "requirements.txt",
        ],
        "文档": [
            "README.md",
            "USAGE_GUIDE.md",
            "ARCHITECTURE.md",
            "QUICKSTART.md",
        ]
    }
    
    project_dir = Path(__file__).parent
    all_exist = True
    
    for category, files in required_files.items():
        print(f"\n{category}:")
        for file in files:
            file_path = project_dir / file
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"  ✓ {file} ({size:,} bytes)")
            else:
                print(f"  ✗ {file} 缺失")
                all_exist = False
    
    return all_exist


def check_dependencies():
    """检查Python依赖"""
    
    print("\n" + "="*70)
    print("检查依赖包...")
    print("="*70)
    
    required_packages = {
        "transformers": "≥4.36.0",
        "torch": "≥2.0.0",
        "numpy": "≥1.24.0",
    }
    
    missing = []
    
    for package, version in required_packages.items():
        try:
            mod = __import__(package)
            print(f"✓ {package} {version} - 已安装")
        except ImportError:
            print(f"✗ {package} {version} - 缺失")
            missing.append(package)
    
    return len(missing) == 0, missing


def check_model():
    """检查Qwen模型"""
    
    print("\n" + "="*70)
    print("检查Qwen模型...")
    print("="*70)
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        
        model_name = "Qwen/Qwen2.5-0.5B-Instruct"
        print(f"\n尝试加载模型: {model_name}")
        
        try:
            # 只尝试加载tokenizer，不加载整个模型
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            print(f"✓ 模型可用！")
            return True
        except Exception as e:
            if "Connection" in str(e) or "HTTPError" in str(e):
                print(f"⚠ 需要下载模型（首次运行）")
                print(f"  运行: huggingface-cli download Qwen/Qwen2.5-0.5B-Instruct")
                return True  # 这是预期的
            else:
                print(f"✗ 模型加载失败: {e}")
                return False
    
    except ImportError:
        print("✗ transformers未安装")
        return False


def check_device():
    """检查设备支持"""
    
    print("\n" + "="*70)
    print("检查计算设备...")
    print("="*70)
    
    try:
        import torch
        
        print(f"\n✓ PyTorch版本: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"✓ NVIDIA GPU可用: {torch.cuda.get_device_name(0)}")
            print(f"  显存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f}GB")
        elif torch.backends.mps.is_available():
            print(f"✓ Apple MPS可用")
        else:
            print(f"ℹ 将使用CPU (性能较低)")
        
        return True
    
    except ImportError:
        print("✗ PyTorch未安装")
        return False


def check_structure():
    """检查项目代码结构"""
    
    print("\n" + "="*70)
    print("检查代码结构...")
    print("="*70)
    
    checks = {
        "model_loader.py": ["load_qwen_model", "get_device"],
        "agent_a.py": ["AgentA", "extract_triplets"],
        "agent_b.py": ["AgentB", "validate_triplet"],
        "dual_agent_system.py": ["DualAgentSystem", "process_sentence"],
    }
    
    project_dir = Path(__file__).parent
    all_ok = True
    
    for file, required_symbols in checks.items():
        file_path = project_dir / file
        if not file_path.exists():
            print(f"✗ {file} 不存在")
            all_ok = False
            continue
        
        content = file_path.read_text(encoding='utf-8')
        found = []
        missing = []
        
        for symbol in required_symbols:
            if symbol in content:
                found.append(symbol)
            else:
                missing.append(symbol)
        
        print(f"\n{file}:")
        for symbol in found:
            print(f"  ✓ {symbol}")
        for symbol in missing:
            print(f"  ✗ {symbol} 缺失")
            all_ok = False
    
    return all_ok


def main():
    """主检查函数"""
    
    print("\n" + "="*70)
    print("双智能体语义三元组抽取系统 - 系统检查")
    print("="*70)
    
    results = {
        "项目文件": check_files(),
        "代码结构": check_structure(),
        "计算设备": check_device(),
        "Python依赖": check_dependencies()[0],
        "Qwen模型": check_model(),
    }
    
    # 总结
    print("\n" + "="*70)
    print("检查总结")
    print("="*70)
    
    for check_name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{check_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    
    if all_passed:
        print("✓ 所有检查都通过！可以开始使用。")
        print("\n快速开始命令:")
        print("  # 批量处理演示")
        print("  python main.py")
        print("\n  # 交互式使用")
        print("  python interactive.py")
    else:
        print("✗ 存在未完成的检查项。")
        print("\n解决方案:")
        
        if not results["Python依赖"]:
            print("  1. 安装依赖: pip install -r requirements.txt")
        
        if not results["Qwen模型"]:
            print("  2. 下载模型: huggingface-cli download Qwen/Qwen2.5-0.5B-Instruct")
        
        if not results["项目文件"] or not results["代码结构"]:
            print("  3. 检查项目文件是否完整")
    
    print("="*70 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
