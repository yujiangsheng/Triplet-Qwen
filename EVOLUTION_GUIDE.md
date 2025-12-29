"""
三元组提取Agent 自动演化系统 - 完整使用指南

概述
====
本系统实现了一个完整的自动演化框架，可以：
1. 自动从网络爬取例句数据
2. 通过多种渠道持续改进Agent A和B
3. 自动评估系统性能
4. 支持用户反馈集成
5. 一键启动完整演化过程

快速开始
========

1. 基本使用（3行代码）
------------------------

from agent_a import TripletsExtractionAgent
from agent_b import TripletsValidationAgent
from integrated_evolution import IntegratedEvolutionSystem

agent_a = TripletsExtractionAgent()
agent_b = TripletsValidationAgent()
system = IntegratedEvolutionSystem(agent_a, agent_b)
report = system.start_evolution()


2. 自定义配置
------------------------

from integrated_evolution import EvolutionConfig

config = EvolutionConfig(
    max_iterations=30,              # 最多迭代30次
    target_accuracy=0.90,           # 目标准确率90%
    convergence_threshold=0.01,     # 更严格的收敛条件
    crawl_frequency=3,              # 每3轮爬取新数据
    quality_threshold=0.75,         # 数据质量下限
)

system = IntegratedEvolutionSystem(agent_a, agent_b, config)
report = system.start_evolution()


核心模块说明
============

1. data_crawler.py (数据爬取)
   
   功能:
   - 从4个源爬取例句 (新闻、文学、百科、社交)
   - 自动质量评估和过滤
   - 数据版本管理
   
   使用:
   from data_crawler import DataCrawler, DataManager
   
   crawler = DataCrawler()
   sentences = crawler.crawl_all_sources()
   filtered = crawler.filter_by_quality(sentences, threshold=0.7)
   
   manager = DataManager()
   manager.create_training_set(filtered)


2. evolution_system.py (演化引擎)
   
   功能:
   - 主演化循环 (验证→优化→更新)
   - 收敛检测
   - 自适应优化策略
   
   使用:
   from evolution_system import EvolutionSystem
   
   evo = EvolutionSystem(agent_a, agent_b)
   evo.start_evolution(max_iterations=50)


3. evaluation_metrics.py (性能评估)
   
   功能:
   - 三元组准确率评估
   - 系统综合评估
   - 用户反馈收集
   
   使用:
   from evaluation_metrics import SystemEvaluator, UserStudy
   
   evaluator = SystemEvaluator(agent_a, agent_b)
   metrics = evaluator.evaluate_on_dataset(test_data)
   
   study = UserStudy()
   study.add_annotation(sentence, triplet, rating=8.5)


4. code_optimization.py (代码优化)
   
   功能:
   - 缓存管理
   - 性能监测
   - 算法优化
   
   使用:
   from code_optimization import optimize_system, global_monitor
   
   optimize_system(agent_a, agent_b)
   stats = global_monitor.get_stats()


5. integrated_evolution.py (完整集成)
   
   功能:
   - 协调所有子系统
   - 完整演化流程
   - 结果报告和保存
   
   使用:
   from integrated_evolution import IntegratedEvolutionSystem
   
   system = IntegratedEvolutionSystem(agent_a, agent_b, config)
   report = system.start_evolution()


配置参数详解
============

EvolutionConfig 参数:

  max_iterations (int): 
    - 最大迭代次数，默认50
    - 影响总演化时间和最终效果
    - 建议: 10-100

  convergence_threshold (float):
    - 收敛条件阈值，默认0.02
    - 连续两轮改进小于此值则收敛
    - 建议: 0.01-0.05

  target_accuracy (float):
    - 目标准确率，默认0.85
    - 达到此准确率则停止
    - 建议: 0.80-0.95

  min_data_size (int):
    - 最小数据集大小，默认50
    - 保证演化数据充足
    - 建议: 30-100

  validation_ratio (float):
    - 验证集比例，默认0.2
    - 用于评估的数据占比
    - 建议: 0.1-0.3

  crawl_frequency (int):
    - 爬取新数据的频率，默认5轮一次
    - 数值越小爬取越频繁
    - 建议: 3-10

  quality_threshold (float):
    - 数据质量阈值，默认0.7
    - 低于此分数的数据被过滤
    - 建议: 0.6-0.8

  use_user_feedback (bool):
    - 是否使用用户反馈，默认True
    - 启用可提高针对性

  optimization_patience (int):
    - 早停耐心，默认10轮
    - N轮无改进后停止
    - 建议: 5-15


演化流程详解
============

演化系统遵循以下流程:

第1步: 初始化
  - 创建Agent A和B实例
  - 初始化数据爬取器
  - 加载初始数据集（如果提供）

第2步: 代码优化（可选）
  - 启用缓存层
  - 启用性能监测
  - 优化算法

第3步: 主演化循环 (for each iteration)
  
  3.1 评估当前性能
      - 在验证集上测试
      - 计算8维度指标
      - 更新最佳模型
  
  3.2 检查收敛条件
      - 性能是否停止改进
      - 是否达到目标准确率
      - 耐心是否耗尽
  
  3.3 优化Agent
      - 根据瓶颈选择优化策略
      - 调整学习率和采样比率
      - 改进语义规则或提取模式
  
  3.4 爬取新数据 (每N轮)
      - 从多个源爬取新句子
      - 进行质量评估和过滤
      - 追加到训练集

第4步: 生成报告
  - 汇总演化历史
  - 输出最佳模型指标
  - 保存演化过程


性能指标
========

系统评估使用8维度指标:

1. accuracy (准确率)
   - 定义: 正确预测的比例
   - 范围: 0.0 - 1.0
   - 权重: 核心指标

2. precision (精确率)
   - 定义: 预测正确的比例
   - 范围: 0.0 - 1.0

3. recall (召回率)
   - 定义: 检测到的正确比例
   - 范围: 0.0 - 1.0

4. f1_score (F1分数)
   - 定义: 精确率和召回率的调和平均
   - 范围: 0.0 - 1.0

5. completeness (完整性)
   - 定义: 信息捕获的完整程度
   - 范围: 0.0 - 1.0
   - 用途: 评估遗漏

6. consistency (一致性)
   - 定义: 多次运行的稳定性
   - 范围: 0.0 - 1.0
   - 用途: 评估可靠性

7. argument_integrity (论元完整性)
   - 定义: Subject和Object的完整性
   - 范围: 0.0 - 1.0
   - 用途: 评估修饰词捕获

8. error_distribution (错误分布)
   - 定义: 错误类型统计
   - 类型: 缺失实体、实体错误、论元不完整等


用户反馈集成
============

系统支持用户反馈以提高准确性:

# 添加用户反馈
system.add_user_feedback(
    sentence='苹果是一种水果',
    triplet={
        'subject': '苹果',
        'predicate': '是',
        'object': '水果'
    },
    rating=9.0,  # 10分制
    feedback='完全正确的三元组'
)

# 获取满意度状态
status = system.get_satisfaction_status()
print(f"平均评分: {status['average_rating']}")
print(f"满意度: {status['satisfaction_level']}")

满意度等级:
  >= 8.0: 非常满意
  6.0-8.0: 满意
  4.0-6.0: 一般
  < 4.0: 不满意


代码优化
========

系统提供内置的代码优化:

1. 缓存优化
   - 缓存LLM调用结果
   - 减少重复计算
   - 自动LRU清理

2. 性能监测
   - 记录各操作耗时
   - 统计执行次数
   - 生成性能报告

3. 批处理
   - 并行处理多条句子
   - 充分利用多核
   - 加速大规模处理

4. 算法优化
   - 快速字符串匹配
   - 优化去重
   - 改进模糊匹配

使用方式:

from code_optimization import optimize_system, global_monitor

# 优化系统
optimize_system(agent_a, agent_b)

# 查看性能统计
stats = global_monitor.get_stats()
print(f"缓存命中率: {stats.get('hit_rate', 0):.2%}")


常见问题 (FAQ)
==============

Q1: 演化需要多长时间?
A: 取决于max_iterations设置。默认50次迭代通常需要5-10分钟。

Q2: 如何获得更好的结果?
A: 
  - 增加max_iterations (30-100)
  - 降低quality_threshold (0.6)
  - 增加crawl_frequency
  - 添加用户反馈
  - 使用更高质量的初始数据

Q3: 内存占用过高怎么办?
A:
  - 减少max_iterations
  - 增加validation_ratio (使用更小的验证集)
  - 启用缓存清理

Q4: 为什么收敛很慢?
A:
  - 减小convergence_threshold (更容易收敛)
  - 提高quality_threshold (更优的数据)
  - 增加crawl_frequency (更频繁的数据更新)

Q5: 如何评估最终效果是否"令人满意"?
A: 查看以下指标:
  - accuracy > 0.85
  - completeness > 0.80
  - user_satisfaction >= 7.0 (如果有反馈)
  - 或 satisfaction_level == '满意' 或 '非常满意'


高级用法
========

1. 自定义数据源

from data_crawler import DataCrawler

class MyDataCrawler(DataCrawler):
    def crawl_from_custom_source(self):
        # 实现自定义爬取逻辑
        return sentences

2. 自定义评估指标

from evaluation_metrics import SystemEvaluator

class MyEvaluator(SystemEvaluator):
    def evaluate_triplet_custom(self, predicted, reference):
        # 实现自定义评估逻辑
        return score

3. 自定义优化策略

from code_optimization import AdaptiveOptimizer

class MyOptimizer(AdaptiveOptimizer):
    def custom_optimization(self, metrics):
        # 实现自定义优化逻辑
        pass


输出示例
========

演化过程中的输出示例:

============================================================
启动集成演化系统
============================================================

--- 第 1 轮 ---
步骤1: 评估性能...
步骤2: 检查收敛条件...
步骤3: 优化Agent...
学习率: 0.0100 -> 0.0105
采样比率: 0.70 -> 0.70
→ 优化完整性：改进语义规则
→ 执行语义规则优化...
性能: 准确率=0.6523, 完整性=0.6841

...

--- 第 20 轮 ---
步骤1: 评估性能...
步骤2: 检查收敛条件...
✓ 已收敛！

============================================================
演化完成！
============================================================
总轮数: 21
最佳准确率: 0.8734
最佳完整性: 0.8601
最佳轮数: 18
总耗时: 245.3秒
满意度: 满意


获取帮助
========

- 查看日志: 所有操作都会输出详细日志
- 运行示例: 执行 python evolution_examples.py
- 检查文档: 各模块的docstring包含详细说明
- 报告分析: 查看生成的JSON报告了解演化细节
"""

# 这是一个文档文件，不包含可执行的Python代码
# 请参考 evolution_examples.py 获取可运行的示例
