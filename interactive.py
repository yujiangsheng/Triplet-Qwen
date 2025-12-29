#!/usr/bin/env python3
"""
交互式演示程序 - 实时测试双智能体系统
"""

from model_loader import load_qwen_model
from agent_a import AgentA
from agent_b import AgentB
from dual_agent_system import DualAgentSystem
import sys


def interactive_demo():
    """交互式演示"""
    
    print("\n" + "="*70)
    print("基于Qwen2.5-0.5B的双智能体系统 - 交互式演示")
    print("="*70)
    
    # 加载模型
    print("\n正在加载模型...")
    try:
        model, tokenizer, device = load_qwen_model()
    except Exception as e:
        print(f"✗ 模型加载失败: {e}")
        return
    
    # 初始化智能体
    agent_a = AgentA(model, tokenizer, device)
    agent_b = AgentB(model, tokenizer, device)
    system = DualAgentSystem(agent_a, agent_b, max_iterations=3)
    
    print("\n✓ 系统已准备就绪！")
    print("\n使用说明:")
    print("  - 输入中文或英文句子进行语义三元组抽取")
    print("  - 输入 'examples' 查看示例")
    print("  - 输入 'quit' 或 'exit' 退出程序")
    print("  - 输入 'clear' 清空历史记录")
    
    results_history = []
    
    while True:
        try:
            sentence = input("\n请输入句子 (或命令): ").strip()
            
            if not sentence:
                continue
            
            if sentence.lower() in ['quit', 'exit', 'q']:
                print("\n感谢使用，再见！")
                break
            
            if sentence.lower() == 'examples':
                print("\n示例句子:")
                examples = [
                    "小明每天早上在公园跑步。",
                    "她很仔细地阅读了这本有趣的书。",
                    "王老师在课堂上用粉笔给学生讲解数学题。",
                    "John runs quickly in the park every morning.",
                    "She carefully studied the book yesterday at home.",
                ]
                for i, example in enumerate(examples, 1):
                    print(f"  {i}. {example}")
                continue
            
            if sentence.lower() == 'clear':
                results_history = []
                print("✓ 历史记录已清空")
                continue
            
            # 处理句子
            result = system.process_sentence(sentence)
            results_history.append(result)
            
            # 打印最终结果
            print(f"\n{'='*70}")
            print(f"最终结果:")
            print(f"{'='*70}")
            print(f"原始句子: {result['sentence']}")
            print(f"最终三元组: {system._format_triplet_for_output(result['final_triplet'])}")
            print(f"验证状态: {'✓ 通过' if result['is_valid'] else '✗ 未通过'}")
            print(f"迭代次数: {result['iterations']}")
            
            if not result['is_valid'] and 'final_validation' in result:
                print(f"反馈: {result['final_validation']['feedback']}")
            
            print(f"{'='*70}\n")
            
        except KeyboardInterrupt:
            print("\n\n程序已中断")
            break
        except Exception as e:
            print(f"✗ 出错: {e}")
            continue
    
    # 打印历史总结
    if results_history:
        print(f"\n{'='*70}")
        print(f"本次会话总结")
        print(f"{'='*70}")
        print(f"处理句子数: {len(results_history)}")
        valid_count = sum(1 for r in results_history if r['is_valid'])
        print(f"验证通过: {valid_count}/{len(results_history)}")
        print(f"{'='*70}\n")


def batch_processing_demo():
    """批量处理演示"""
    
    print("\n" + "="*70)
    print("双智能体系统 - 批量处理演示")
    print("="*70)
    
    # 加载模型
    print("\n正在加载模型...")
    try:
        model, tokenizer, device = load_qwen_model()
    except Exception as e:
        print(f"✗ 模型加载失败: {e}")
        return
    
    # 初始化智能体
    agent_a = AgentA(model, tokenizer, device)
    agent_b = AgentB(model, tokenizer, device)
    system = DualAgentSystem(agent_a, agent_b, max_iterations=3)
    
    # 测试句子
    test_sentences = [
        # 中文示例
        "小明每天早上在公园跑步。",
        "她很仔细地阅读了这本有趣的书。",
        "王老师在课堂上用粉笔给学生讲解数学题。",
        "他因为生病所以没有来上课。",
        "我们在公司的会议室讨论了这个项目的进展。",
        
        # 英文示例
        "John runs quickly in the park every morning.",
        "She carefully studied the book yesterday at home.",
        "The teacher explained the math problem using chalk.",
        "They will meet in the conference room tomorrow afternoon.",
        "He didn't come to class because he was sick.",
    ]
    
    # 批量处理
    results = system.process_batch(test_sentences, save_results=True)
    
    # 打印总结
    system.print_summary(results)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "batch":
        batch_processing_demo()
    else:
        interactive_demo()
