"""
完整演化系统使用指南和示例

这个脚本演示如何：
1. 初始化和配置演化系统
2. 集成Agent A和Agent B
3. 运行自动演化过程
4. 监测性能和收集反馈
5. 获取演化结果
"""

import logging
from typing import Dict, List
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# 示例 1: 基础演化 - 默认配置
# ============================================================================

def example_basic_evolution():
    """
    示例 1: 使用默认配置运行基础演化
    
    这是最简单的使用方式，适合快速测试
    """
    print("\n" + "=" * 70)
    print("示例 1: 基础演化（默认配置）")
    print("=" * 70)
    
    try:
        from agent_a import TripletsExtractionAgent
        from agent_b import TripletsValidationAgent
        from integrated_evolution import IntegratedEvolutionSystem, EvolutionConfig
        
        # 初始化Agent
        print("初始化Agent A (提取器)...")
        agent_a = TripletsExtractionAgent()
        
        print("初始化Agent B (验证器)...")
        agent_b = TripletsValidationAgent()
        
        # 创建默认配置
        config = EvolutionConfig(
            max_iterations=10,
            target_accuracy=0.80,
            optimization_patience=5
        )
        
        print(f"演化配置: {config.to_dict()}")
        
        # 创建演化系统
        system = IntegratedEvolutionSystem(agent_a, agent_b, config)
        
        # 运行演化
        print("\n启动演化过程...")
        report = system.start_evolution()
        
        # 显示结果
        print("\n演化完成！")
        print(f"最佳准确率: {report.best_metrics.accuracy:.4f}")
        print(f"最佳轮数: {report.best_iteration}")
        print(f"总轮数: {report.total_iterations}")
        print(f"收敛状态: {report.convergence_achieved}")
        
        return report
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保所有依赖模块都已创建")
        return None


# ============================================================================
# 示例 2: 自定义配置 - 高级演化
# ============================================================================

def example_advanced_evolution():
    """
    示例 2: 使用自定义配置运行高级演化
    
    演示如何调整参数以获得更好的结果
    """
    print("\n" + "=" * 70)
    print("示例 2: 高级演化（自定义配置）")
    print("=" * 70)
    
    try:
        from agent_a import TripletsExtractionAgent
        from agent_b import TripletsValidationAgent
        from integrated_evolution import IntegratedEvolutionSystem, EvolutionConfig
        from data_crawler import Sentence
        
        # 初始化Agent
        agent_a = TripletsExtractionAgent()
        agent_b = TripletsValidationAgent()
        
        # 自定义配置 - 追求更高准确率
        config = EvolutionConfig(
            max_iterations=30,              # 更多迭代
            convergence_threshold=0.01,     # 更严格的收敛条件
            target_accuracy=0.90,           # 更高的目标
            min_data_size=100,
            crawl_frequency=3,              # 更频繁地爬取新数据
            quality_threshold=0.75,         # 更宽松的质量要求
            optimization_patience=15,       # 更多的耐心
        )
        
        print("自定义配置:")
        for key, value in config.to_dict().items():
            print(f"  {key}: {value}")
        
        # 创建演化系统
        system = IntegratedEvolutionSystem(agent_a, agent_b, config)
        
        # 准备初始数据（可选）
        print("\n准备初始数据集...")
        initial_data = [
            Sentence(
                text="李明是一个优秀的程序员",
                source="example",
                domain="professional",
                quality_score=0.9
            ),
            Sentence(
                text="这个项目需要高效的算法",
                source="example",
                domain="technical",
                quality_score=0.85
            ),
        ]
        
        # 运行演化
        print("\n启动高级演化过程...")
        report = system.start_evolution(initial_data)
        
        # 显示详细结果
        print("\n演化完成！")
        print(f"总迭代数: {report.total_iterations}")
        print(f"最佳准确率: {report.best_metrics.accuracy:.4f}")
        print(f"最佳完整性: {report.best_metrics.completeness:.4f}")
        print(f"最佳轮数: {report.best_iteration}")
        print(f"总耗时: {report.time_elapsed:.1f}秒")
        print(f"是否收敛: {report.convergence_achieved}")
        
        return report
        
    except ImportError as e:
        print(f"导入错误: {e}")
        return None


# ============================================================================
# 示例 3: 用户反馈集成 - 迭代改进
# ============================================================================

def example_with_user_feedback():
    """
    示例 3: 集成用户反馈的演化
    
    演示如何在演化过程中收集和使用用户反馈
    """
    print("\n" + "=" * 70)
    print("示例 3: 集成用户反馈的演化")
    print("=" * 70)
    
    try:
        from agent_a import TripletsExtractionAgent
        from agent_b import TripletsValidationAgent
        from integrated_evolution import IntegratedEvolutionSystem, EvolutionConfig
        
        # 初始化Agent
        agent_a = TripletsExtractionAgent()
        agent_b = TripletsValidationAgent()
        
        config = EvolutionConfig(
            max_iterations=15,
            target_accuracy=0.85,
            use_user_feedback=True,
            optimization_patience=8
        )
        
        # 创建系统
        system = IntegratedEvolutionSystem(agent_a, agent_b, config)
        
        # 模拟用户反馈
        print("\n收集用户反馈...")
        
        test_cases = [
            {
                'sentence': '苹果是一种营养丰富的水果',
                'triplet': {
                    'subject': '苹果',
                    'predicate': '是',
                    'object': '水果',
                    'mods': {'quality': '营养丰富'}
                },
                'rating': 9.0,
                'feedback': '完全正确'
            },
            {
                'sentence': '张三昨天在图书馆看了整个下午的书',
                'triplet': {
                    'subject': '张三',
                    'predicate': '看书',
                    'object': '书',
                    'mods': {'time': '昨天', 'place': '图书馆'}
                },
                'rating': 8.0,
                'feedback': '基本正确，时间和地点识别良好'
            },
            {
                'sentence': '这家公司的新产品在市场上很受欢迎',
                'triplet': {
                    'subject': '新产品',
                    'predicate': '受欢迎',
                    'object': '市场',
                    'mods': {'agent': '这家公司'}
                },
                'rating': 7.0,
                'feedback': '漏掉了一些修饰信息'
            }
        ]
        
        for case in test_cases:
            system.add_user_feedback(
                case['sentence'],
                case['triplet'],
                case['rating'],
                case['feedback']
            )
            print(f"✓ 添加反馈: {case['sentence'][:30]}... (评分: {case['rating']})")
        
        # 运行演化
        print("\n启动演化过程（考虑用户反馈）...")
        report = system.start_evolution()
        
        # 显示满意度状态
        print("\n用户满意度评估:")
        satisfaction = system.get_satisfaction_status()
        print(f"  平均评分: {satisfaction['average_rating']:.1f}/10")
        print(f"  满意度: {satisfaction['satisfaction_level']}")
        print(f"  反馈数量: {satisfaction['total_feedback']}")
        print(f"  系统准确率: {satisfaction['system_accuracy']:.4f}")
        
        return report
        
    except ImportError as e:
        print(f"导入错误: {e}")
        return None


# ============================================================================
# 示例 4: 代码优化 - 性能提升
# ============================================================================

def example_with_optimization():
    """
    示例 4: 启用代码优化的演化
    
    演示如何优化系统性能
    """
    print("\n" + "=" * 70)
    print("示例 4: 启用代码优化的演化")
    print("=" * 70)
    
    try:
        from agent_a import TripletsExtractionAgent
        from agent_b import TripletsValidationAgent
        from code_optimization import optimize_system, global_monitor
        from integrated_evolution import IntegratedEvolutionSystem, EvolutionConfig
        
        # 初始化Agent
        print("初始化Agent...")
        agent_a = TripletsExtractionAgent()
        agent_b = TripletsValidationAgent()
        
        # 优化系统
        print("\n执行代码优化...")
        opt_report = optimize_system(agent_a, agent_b)
        print(f"优化结果: {opt_report}")
        
        # 创建配置
        config = EvolutionConfig(
            max_iterations=10,
            target_accuracy=0.85
        )
        
        # 创建系统
        system = IntegratedEvolutionSystem(agent_a, agent_b, config)
        
        # 运行演化（将使用优化后的Agent）
        print("\n运行演化（使用优化后的代码）...")
        report = system.start_evolution()
        
        # 显示性能数据
        print("\n性能监测数据:")
        if hasattr(agent_a, '_monitor'):
            print("Agent A 性能:")
            a_stats = agent_a._monitor.get_stats()
            for op, timing in a_stats.get('timings', {}).items():
                print(f"  {op}: {timing['average']:.3f}s")
        
        if hasattr(agent_b, '_monitor'):
            print("Agent B 性能:")
            b_stats = agent_b._monitor.get_stats()
            for op, timing in b_stats.get('timings', {}).items():
                print(f"  {op}: {timing['average']:.3f}s")
        
        print(f"\n全局缓存命中率: {global_monitor.get_hit_rate():.2%}")
        
        return report
        
    except ImportError as e:
        print(f"导入错误: {e}")
        return None


# ============================================================================
# 示例 5: 完整流程 - 端到端演化
# ============================================================================

def example_complete_workflow():
    """
    示例 5: 完整的端到端演化流程
    
    展示整个系统的完整使用方式
    """
    print("\n" + "=" * 70)
    print("示例 5: 完整端到端演化流程")
    print("=" * 70)
    
    try:
        from agent_a import TripletsExtractionAgent
        from agent_b import TripletsValidationAgent
        from code_optimization import optimize_system
        from integrated_evolution import IntegratedEvolutionSystem, EvolutionConfig
        from evaluation_metrics import SystemEvaluator, TripleteEvaluator
        import json
        from datetime import datetime
        
        print("\n第1步: 初始化系统")
        print("-" * 70)
        agent_a = TripletsExtractionAgent()
        agent_b = TripletsValidationAgent()
        
        print("✓ Agent A (提取器) 已初始化")
        print("✓ Agent B (验证器) 已初始化")
        
        print("\n第2步: 优化代码")
        print("-" * 70)
        optimize_system(agent_a, agent_b)
        print("✓ 代码优化完成")
        
        print("\n第3步: 配置演化参数")
        print("-" * 70)
        config = EvolutionConfig(
            max_iterations=20,
            convergence_threshold=0.02,
            target_accuracy=0.85,
            crawl_frequency=4,
            optimization_patience=10,
            use_user_feedback=True
        )
        print("演化配置:")
        for key, value in config.to_dict().items():
            print(f"  {key}: {value}")
        
        print("\n第4步: 创建演化系统")
        print("-" * 70)
        system = IntegratedEvolutionSystem(agent_a, agent_b, config)
        print("✓ 演化系统已创建")
        
        print("\n第5步: 添加用户反馈（可选）")
        print("-" * 70)
        print("（在实际应用中，这些反馈来自真实用户）")
        
        print("\n第6步: 启动自动演化")
        print("-" * 70)
        report = system.start_evolution()
        
        print("\n第7步: 分析结果")
        print("-" * 70)
        print(f"演化报告:")
        print(f"  总迭代数: {report.total_iterations}")
        print(f"  最佳准确率: {report.best_metrics.accuracy:.4f}")
        print(f"  最佳完整性: {report.best_metrics.completeness:.4f}")
        print(f"  最佳轮数: {report.best_iteration}")
        print(f"  总耗时: {report.time_elapsed:.1f}秒")
        print(f"  收敛状态: {report.convergence_achieved}")
        
        print("\n第8步: 获取系统评估")
        print("-" * 70)
        satisfaction = system.get_satisfaction_status()
        print(f"满意度评估:")
        print(f"  平均评分: {satisfaction['average_rating']:.1f}/10")
        print(f"  满意度等级: {satisfaction['satisfaction_level']}")
        print(f"  系统准确率: {satisfaction['system_accuracy']:.4f}")
        
        print("\n第9步: 保存结果")
        print("-" * 70)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f'/tmp/evolution_report_{timestamp}.json'
        system.save_report(report_file)
        print(f"✓ 报告已保存至: {report_file}")
        
        print("\n" + "=" * 70)
        print("完整演化流程完成！")
        print("=" * 70)
        
        return report
        
    except ImportError as e:
        print(f"导入错误: {e}")
        return None
    except Exception as e:
        logger.error(f"执行错误: {e}", exc_info=True)
        return None


# ============================================================================
# 主入口
# ============================================================================

def main():
    """
    主函数 - 运行所有示例
    """
    print("\n")
    print("=" * 70)
    print("三元组提取Agent 完整演化系统示例")
    print("=" * 70)
    
    examples = [
        ("基础演化", example_basic_evolution),
        ("高级演化", example_advanced_evolution),
        ("用户反馈", example_with_user_feedback),
        ("代码优化", example_with_optimization),
        ("完整流程", example_complete_workflow),
    ]
    
    # 交互式菜单
    while True:
        print("\n请选择要运行的示例:")
        for i, (name, _) in enumerate(examples, 1):
            print(f"  {i}. {name}")
        print("  0. 运行所有示例")
        print("  -1. 退出")
        
        try:
            choice = int(input("\n请输入选择 (0-5): "))
            
            if choice == -1:
                print("退出程序")
                break
            elif choice == 0:
                print("\n将运行所有示例...\n")
                for name, func in examples:
                    try:
                        func()
                    except Exception as e:
                        logger.error(f"示例 '{name}' 执行失败: {e}")
                    print("\n按Enter继续...")
                    input()
            elif 1 <= choice <= len(examples):
                name, func = examples[choice - 1]
                try:
                    func()
                except Exception as e:
                    logger.error(f"示例执行失败: {e}")
            else:
                print("无效的选择，请重试")
                
        except ValueError:
            print("请输入有效的数字")
        except KeyboardInterrupt:
            print("\n程序被中断")
            break


if __name__ == "__main__":
    main()
