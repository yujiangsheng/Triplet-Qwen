#!/usr/bin/env python3
"""
主程序 - 双智能体系统演示

演示中英文语义三元组的抽取和验证
"""

from model_loader import load_qwen_model
from agent_a import AgentA
from agent_b import AgentB
from dual_agent_system import DualAgentSystem
import sys


def main():
    """主程序入口"""
    
    print("\n" + "="*70)
    print("基于Qwen2.5-0.5B的双智能体语义三元组抽取系统")
    print("="*70)
    
    # 加载模型
    print("\n[步骤1] 加载Qwen2.5-0.5B-Instruct模型...")
    try:
        model, tokenizer, device = load_qwen_model()
    except Exception as e:
        print(f"✗ 模型加载失败，请确保网络连接或模型文件可用")
        print(f"  错误: {e}")
        print(f"\n建议:")
        print(f"  1. 检查网络连接")
        print(f"  2. 运行 huggingface-cli download Qwen/Qwen2.5-0.5B-Instruct")
        print(f"  3. 或设置 HUGGINGFACE_HUB_CACHE 指向本地模型")
        sys.exit(1)
    
    # 初始化智能体
    print("\n[步骤2] 初始化双智能体系统...")
    agent_a = AgentA(model, tokenizer, device)
    agent_b = AgentB(model, tokenizer, device)
    dual_system = DualAgentSystem(agent_a, agent_b, max_iterations=3)
    print("✓ 智能体A (三元组抽取) 和 智能体B (三元组验证) 已初始化")
    
    # 测试句子
    test_sentences = [
        # 中文示例
        "小明每天早上在公园跑步。",
        "她很仔细地阅读了这本有趣的书。",
        "王老师在课堂上用粉笔给学生讲解数学题。",
        # 英文示例
        "John runs quickly in the park every morning.",
        "She carefully studied the book yesterday at home.",
    ]
    
    # 处理句子
    print("\n[步骤3] 开始处理句子...")
    results = dual_system.process_batch(test_sentences, save_results=True)
    
    # 打印总结
    dual_system.print_summary(results)


if __name__ == "__main__":
    main()
