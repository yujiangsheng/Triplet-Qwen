# Triplet-Qwen 完整指南

本文档包含所有必需的信息。

## 目录

1. [快速开始](#快速开始)
2. [项目结构](#项目结构)
3. [核心概念](#核心概念)
4. [使用教程](#使用教程)
5. [配置参数](#配置参数)
6. [常见问题](#常见问题)
7. [API参考](#api参考)

---

## 快速开始

### 30秒入门

```bash
# 1. 查看演示
python main.py

# 2. 运行示例
python evolution_examples.py

# 3. 交互式测试
python interactive.py
```

### 代码示例

最简单的使用方式：

```python
from triplet_qwen import quick_start

# 一行代码启动完整的演化
report = quick_start(max_iterations=30, target_accuracy=0.85)

# 查看结果
print(f"最佳准确率: {report.best_metrics.accuracy:.4f}")
print(f"满意度: {report.convergence_achieved}")
```

### 高级使用

```python
from triplet_qwen import (
    IntegratedEvolutionSystem,
    EvolutionConfig,
    TripletsExtractionAgent,
    TripletsValidationAgent
)

# 自定义配置
config = EvolutionConfig(
    max_iterations=50,           # 最多迭代50次
    target_accuracy=0.90,        # 目标准确率90%
    convergence_threshold=0.01,  # 收敛阈值
    crawl_frequency=3            # 每3轮爬取新数据
)

# 创建系统
system = IntegratedEvolutionSystem(
    TripletsExtractionAgent(),
    TripletsValidationAgent(),
    config
)

# 运行演化
report = system.start_evolution()

# 添加用户反馈
system.add_user_feedback(
    sentence='示例句子',
    triplet={'subject': 'S', 'predicate': 'P', 'object': 'O'},
    rating=9.0
)

# 查看满意度
status = system.get_satisfaction_status()
print(f"满意度等级: {status['satisfaction_level']}")
```

---

## 项目结构

```
Triplet-Qwen/
├── core/                    # 核心模块
│   ├── agent_a.py          # 三元组提取器
│   ├── agent_b.py          # 三元组验证器
│   ├── data_crawler.py     # 数据采集
│   ├── evolution_system.py # 演化引擎
│   ├── evaluation_metrics.py # 性能评估
│   ├── code_optimization.py # 代码优化
│   └── integrated_evolution.py # 系统集成
│
├── examples/
│   └── evolution_examples.py  # 5个完整示例
│
├── tests/
│   └── test_integration.py    # 集成测试
│
├── triplet_qwen.py           # 统一API入口
├── main.py                   # 系统演示
├── interactive.py            # 交互式工具
├── verify.py                 # 系统验证
└── config.py                # 配置文件
```

---

## 核心概念

### Agent A: 三元组提取器

负责从句子中提取三元组 (Subject, Predicate, Object, Modifiers)。

```python
agent = TripletsExtractionAgent()
triplet = agent.extract_triplets("苹果是一种水果")
# 返回: {
#   'subject': '苹果',
#   'predicate': '是',
#   'object': '水果',
#   'mods': {}
# }
```

### Agent B: 三元组验证器

验证提取的三元组是否正确和完整。

```python
agent = TripletsValidationAgent()
result = agent.validate_triplet(sentence, triplet)
# 返回: {'is_valid': True, 'confidence': 0.95, ...}
```

### 演化系统

自动优化Agent A和B的性能，通过：
1. 定期数据采集（4个来源）
2. 性能评估（8维度指标）
3. 自动优化（自适应策略）
4. 收敛检测（自动停止）

### 评估指标

系统评估8个维度：

| 指标 | 说明 |
|------|------|
| accuracy | 总体准确率 |
| precision | 精确率 |
| recall | 召回率 |
| f1_score | F1分数 |
| completeness | 信息完整性 |
| consistency | 结果稳定性 |
| argument_integrity | 论元完整性 |
| error_distribution | 错误分布 |

---

## 使用教程

### 教程1：基础演化（5分钟）

```bash
python evolution_examples.py
```

选择 "5. 完整端到端演化流程"，观察系统自动优化的过程。

### 教程2：自定义参数（10分钟）

修改配置参数以获得最佳结果：

```python
from triplet_qwen import quick_start

# 追求更高准确率
report = quick_start(
    max_iterations=100,        # 更多迭代
    target_accuracy=0.95,      # 更高目标
    convergence_threshold=0.005, # 更严格收敛
    crawl_frequency=2          # 更频繁爬取
)
```

### 教程3：添加用户反馈（5分钟）

```python
from triplet_qwen import IntegratedEvolutionSystem, EvolutionConfig
from agent_a import TripletsExtractionAgent
from agent_b import TripletsValidationAgent

system = IntegratedEvolutionSystem(
    TripletsExtractionAgent(),
    TripletsValidationAgent(),
    EvolutionConfig(use_user_feedback=True)
)

# 运行部分演化
for i in range(5):
    # ... 演化过程
    pass

# 添加反馈
system.add_user_feedback(
    sentence='示例句子',
    triplet={'subject': 'S', 'predicate': 'P', 'object': 'O'},
    rating=8.5,
    feedback='基本正确'
)

# 检查满意度
status = system.get_satisfaction_status()
print(status)
```

---

## 配置参数

### EvolutionConfig 参数

```python
from triplet_qwen import EvolutionConfig

config = EvolutionConfig(
    # 演化控制
    max_iterations=50,              # 最大迭代次数 (10-100)
    convergence_threshold=0.02,     # 收敛阈值 (0.01-0.05)
    target_accuracy=0.85,           # 目标准确率 (0.80-0.95)
    
    # 数据管理
    min_data_size=50,               # 最小数据集大小
    validation_ratio=0.2,           # 验证集比例
    crawl_frequency=5,              # 爬取频率(轮数) (3-10)
    quality_threshold=0.7,          # 数据质量下限 (0.6-0.8)
    
    # 优化策略
    use_user_feedback=True,         # 使用用户反馈
    optimization_patience=10        # 早停耐心(轮数) (5-15)
)
```

### 参数说明

| 参数 | 作用 | 调整指南 |
|------|------|---------|
| max_iterations | 控制演化时间和效果 | 增加可能获得更好结果 |
| convergence_threshold | 判断何时停止演化 | 降低会更严格 |
| target_accuracy | 演化目标 | 更高需要更多时间 |
| crawl_frequency | 数据更新频率 | 降低可加速收敛 |
| quality_threshold | 数据质量要求 | 降低可包含更多数据 |
| optimization_patience | 无改进时停止 | 增加给优化更多机会 |

---

## 常见问题

### Q: 演化需要多长时间？

**A:** 取决于max_iterations和你的计算机：
- 10次迭代: 1-2分钟
- 30次迭代: 3-5分钟
- 50次迭代: 5-10分钟

### Q: 如何获得更好的结果？

**A:** 几个方法：
1. 增加 `max_iterations` (30-100)
2. 降低 `quality_threshold` (0.6-0.7)
3. 增加 `crawl_frequency` (3-5)
4. 添加用户反馈 (通过add_user_feedback)
5. 多次运行并选择最佳结果

### Q: 内存占用过高怎么办？

**A:**
1. 减少 `max_iterations`
2. 增加 `validation_ratio` 使用更小的验证集
3. 减少 `min_data_size`

### Q: 为什么收敛很慢？

**A:**
1. 降低 `convergence_threshold` (使收敛标准宽松)
2. 提高 `quality_threshold` (使用更优质的数据)
3. 减少 `optimization_patience` (提前停止)

### Q: 如何评估效果是否"令人满意"？

**A:** 查看以下指标：
- accuracy >= 0.85 ✓
- completeness >= 0.80 ✓
- argument_integrity >= 0.80 ✓
- satisfaction_level == '满意' 或 '非常满意' ✓

### Q: 可以在自己的数据上运行吗？

**A:** 可以。修改 `data_crawler.py` 或在 `IntegratedEvolutionSystem` 中传递自己的数据。

---

## API参考

### IntegratedEvolutionSystem

主系统类。

```python
system = IntegratedEvolutionSystem(agent_a, agent_b, config)

# 启动演化
report = system.start_evolution(initial_data)

# 添加用户反馈
system.add_user_feedback(sentence, triplet, rating, feedback)

# 获取满意度
status = system.get_satisfaction_status()

# 保存报告
system.save_report('output.json')
```

### EvolutionConfig

配置类，所有参数都可选。

```python
config = EvolutionConfig(
    max_iterations=50,
    target_accuracy=0.85,
    # ... 其他参数
)

# 转换为字典
config_dict = config.to_dict()
```

### EvolutionReport

演化结果报告。

```python
report.best_metrics.accuracy      # 最佳准确率
report.best_iteration             # 最佳迭代次数
report.total_iterations           # 总迭代次数
report.convergence_achieved       # 是否已收敛
report.metrics_history            # 所有迭代的指标
```

### 快速函数

```python
from triplet_qwen import quick_start

# 一行代码启动
report = quick_start(max_iterations=30)
```

---

## 更多资源

- **源代码**: 查看各个 `.py` 文件的注释
- **示例**: 运行 `python evolution_examples.py`
- **测试**: 运行 `python test_integration.py`
- **验证**: 运行 `python verify.py`

---

**祝你使用愉快！** 🚀

如有问题，请查看源代码注释或运行相关的示例。
