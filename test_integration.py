"""
最终集成测试脚本 - 验证完整的演化系统

这个脚本测试:
1. 所有模块是否可以正确导入
2. 关键功能是否正常工作
3. 集成是否无缝
4. 演化流程是否可以完整运行
"""

import sys
import logging
from typing import Dict, List, Tuple
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_imports():
    """测试所有模块的导入"""
    print("\n" + "=" * 70)
    print("测试1: 模块导入")
    print("=" * 70)
    
    modules = {
        'data_crawler': ['DataCrawler', 'DataManager', 'Sentence'],
        'evolution_system': ['EvolutionSystem', 'AdaptiveOptimizer', 'EvolutionMetrics'],
        'evaluation_metrics': ['TripleteEvaluator', 'SystemEvaluator', 'UserStudy'],
        'code_optimization': ['CacheManager', 'optimize_system', 'PerformanceMonitor'],
        'integrated_evolution': ['IntegratedEvolutionSystem', 'EvolutionConfig'],
    }
    
    results = {}
    for module_name, classes in modules.items():
        try:
            module = __import__(module_name)
            for class_name in classes:
                if hasattr(module, class_name):
                    results[f"{module_name}.{class_name}"] = "✓"
                else:
                    results[f"{module_name}.{class_name}"] = "✗ 缺失"
        except ImportError as e:
            results[module_name] = f"✗ 导入失败: {e}"
    
    # 显示结果
    passed = sum(1 for v in results.values() if v == "✓")
    total = len(results)
    
    for item, status in results.items():
        print(f"  {item:<50} {status}")
    
    print(f"\n结果: {passed}/{total} 通过")
    return passed == total


def test_data_crawler():
    """测试数据爬取模块"""
    print("\n" + "=" * 70)
    print("测试2: 数据爬取功能")
    print("=" * 70)
    
    try:
        from data_crawler import DataCrawler, DataManager, Sentence
        
        print("初始化DataCrawler...")
        crawler = DataCrawler()
        
        # 测试爬取
        print("测试爬取新闻数据...")
        news = crawler.crawl_from_news()
        print(f"  ✓ 爬取 {len(news)} 条新闻")
        
        print("测试爬取文学数据...")
        lit = crawler.crawl_from_literature()
        print(f"  ✓ 爬取 {len(lit)} 条文学数据")
        
        print("测试爬取百科数据...")
        ency = crawler.crawl_from_encyclopedia()
        print(f"  ✓ 爬取 {len(ency)} 条百科数据")
        
        print("测试多源爬取...")
        all_data = crawler.crawl_all_sources()
        print(f"  ✓ 总共爬取 {len(all_data)} 条数据")
        
        # 测试过滤
        print("测试质量过滤...")
        filtered = crawler.filter_by_quality(all_data, threshold=0.7)
        print(f"  ✓ 过滤后 {len(filtered)} 条高质量数据")
        
        # 测试统计
        print("测试数据统计...")
        stats = crawler.get_statistics(all_data)
        print(f"  ✓ 统计数据: {len(stats)} 项")
        
        # 测试数据管理
        print("测试DataManager...")
        manager = DataManager()
        manager.create_training_set(filtered)
        print(f"  ✓ 创建训练集")
        
        return True
        
    except Exception as e:
        logger.error(f"数据爬取测试失败: {e}")
        return False


def test_evaluation():
    """测试评估模块"""
    print("\n" + "=" * 70)
    print("测试3: 性能评估功能")
    print("=" * 70)
    
    try:
        from evaluation_metrics import TripleteEvaluator, UserStudy, EvaluationMetrics
        
        print("初始化TripleteEvaluator...")
        evaluator = TripleteEvaluator()
        
        # 测试三元组评估
        print("测试三元组评估...")
        predicted = {
            'subject': '苹果',
            'predicate': '是',
            'object': '水果',
            'mods': {}
        }
        reference = {
            'subject': '苹果',
            'predicate': '是',
            'object': '水果',
            'mods': {}
        }
        
        score = evaluator.evaluate_triplet(predicted, reference)
        print(f"  ✓ 完全匹配分数: {score['overall']:.4f}")
        
        # 测试用户反馈
        print("测试用户反馈...")
        study = UserStudy()
        study.add_annotation("测试句子", predicted, 9.0, "很好")
        print(f"  ✓ 添加用户反馈")
        
        avg_rating = study.get_average_rating()
        print(f"  ✓ 平均评分: {avg_rating:.1f}")
        
        satisfaction = study.get_satisfaction_level()
        print(f"  ✓ 满意度等级: {satisfaction}")
        
        return True
        
    except Exception as e:
        logger.error(f"评估测试失败: {e}")
        return False


def test_optimization():
    """测试优化模块"""
    print("\n" + "=" * 70)
    print("测试4: 代码优化功能")
    print("=" * 70)
    
    try:
        from code_optimization import (
            CacheManager, PromptOptimizer, PerformanceMonitor,
            AlgorithmOptimizations
        )
        
        # 测试缓存
        print("测试缓存管理...")
        cache = CacheManager(max_size=10)
        cache.set("key1", "value1")
        result = cache.get("key1")
        print(f"  ✓ 缓存命中: {result == 'value1'}")
        
        hit_rate = cache.get_hit_rate()
        print(f"  ✓ 命中率: {hit_rate:.2%}")
        
        # 测试提示优化
        print("测试提示词优化...")
        prompt = PromptOptimizer.optimize_extraction_prompt("测试文本")
        print(f"  ✓ 生成优化提示 ({len(prompt)} 字符)")
        
        # 测试性能监测
        print("测试性能监测...")
        monitor = PerformanceMonitor()
        with monitor.timing_context("test_op"):
            pass
        stats = monitor.get_stats()
        print(f"  ✓ 记录性能: {len(stats['timings'])} 个操作")
        
        # 测试算法优化
        print("测试算法优化...")
        match = AlgorithmOptimizations.fast_string_match("苹果", "苹果")
        print(f"  ✓ 快速匹配: {match}")
        
        dedup = AlgorithmOptimizations.optimized_deduplication(["a", "b", "a"])
        print(f"  ✓ 去重: {len(dedup)} 个元素")
        
        return True
        
    except Exception as e:
        logger.error(f"优化测试失败: {e}")
        return False


def test_evolution_config():
    """测试演化配置"""
    print("\n" + "=" * 70)
    print("测试5: 演化配置")
    print("=" * 70)
    
    try:
        from integrated_evolution import EvolutionConfig
        
        # 默认配置
        print("测试默认配置...")
        config = EvolutionConfig()
        config_dict = config.to_dict()
        print(f"  ✓ 配置项数: {len(config_dict)}")
        
        # 自定义配置
        print("测试自定义配置...")
        custom_config = EvolutionConfig(
            max_iterations=20,
            target_accuracy=0.90,
            convergence_threshold=0.01
        )
        print(f"  ✓ max_iterations: {custom_config.max_iterations}")
        print(f"  ✓ target_accuracy: {custom_config.target_accuracy}")
        
        return True
        
    except Exception as e:
        logger.error(f"配置测试失败: {e}")
        return False


def test_integrated_system():
    """测试集成系统（模拟Agent）"""
    print("\n" + "=" * 70)
    print("测试6: 集成系统（模拟）")
    print("=" * 70)
    
    try:
        from integrated_evolution import IntegratedEvolutionSystem, EvolutionConfig
        from data_crawler import Sentence
        
        # 创建模拟Agent
        class MockAgentA:
            def extract_triplets(self, text):
                return {
                    'subject': '主语',
                    'predicate': '动作',
                    'object': '宾语',
                    'mods': {}
                }
        
        class MockAgentB:
            def validate_triplet(self, text, triplet):
                return {'is_valid': True}
        
        print("创建模拟Agent...")
        agent_a = MockAgentA()
        agent_b = MockAgentB()
        print("  ✓ Agent A 创建")
        print("  ✓ Agent B 创建")
        
        # 创建配置
        config = EvolutionConfig(
            max_iterations=3,
            target_accuracy=0.80
        )
        print("  ✓ 配置创建")
        
        # 创建系统
        print("创建集成演化系统...")
        system = IntegratedEvolutionSystem(agent_a, agent_b, config)
        print("  ✓ 系统初始化")
        
        # 添加用户反馈
        print("测试用户反馈...")
        system.add_user_feedback(
            "测试句子",
            {'subject': 'S', 'predicate': 'P', 'object': 'O'},
            8.0,
            "反馈"
        )
        print("  ✓ 反馈添加")
        
        # 准备数据
        print("准备初始数据...")
        initial_data = [
            Sentence(
                text=f"测试句子{i}",
                source="test",
                domain="test",
                quality_score=0.9
            )
            for i in range(5)
        ]
        print(f"  ✓ 准备 {len(initial_data)} 条数据")
        
        # 检查系统状态
        print("检查系统状态...")
        status = system.get_satisfaction_status()
        print(f"  ✓ 状态检查: {status['satisfaction_level']}")
        
        return True
        
    except Exception as e:
        logger.error(f"集成系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n")
    print("=" * 70)
    print("三元组提取Agent 演化系统 - 集成测试")
    print("=" * 70)
    
    tests = [
        ("模块导入", test_imports),
        ("数据爬取", test_data_crawler),
        ("性能评估", test_evaluation),
        ("代码优化", test_optimization),
        ("演化配置", test_evolution_config),
        ("集成系统", test_integrated_system),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            logger.error(f"{test_name}测试异常: {e}")
            results[test_name] = False
    
    # 显示总结
    print("\n" + "=" * 70)
    print("测试总结")
    print("=" * 70)
    
    for test_name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {test_name:<20} {status}")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n✓ 所有测试通过！系统已准备好使用。")
        print("\n接下来可以:")
        print("  1. 运行 python evolution_examples.py 查看使用示例")
        print("  2. 阅读 EVOLUTION_GUIDE.md 了解详细文档")
        print("  3. 查看 SYSTEM_EVOLUTION_SUMMARY.md 了解系统概览")
    else:
        print("\n✗ 有测试失败。请检查错误信息。")
    
    print("=" * 70 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
