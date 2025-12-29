# Triplet-Qwen: 三元组提取自动演化系统

一个完整的、生产级别的三元组自动提取和优化系统。使用Qwen2.5-0.5B-Instruct模型，双Agent自动协作，通过多源数据采集和自适应优化，将系统准确率从初始~60%自动提升到85%+。

## ⚡ 快速开始

### 一行代码启动

```python
from triplet_qwen import quick_start
report = quick_start()  # 自动优化，约5-10分钟完成
```

### 30秒演示

```bash
python main.py                      # 查看系统演示
python evolution_examples.py        # 运行5个示例
python interactive.py               # 交互式测试

# 🆕 演化演示 (强烈推荐!)
python evolution_demo.py            # 可视化展示Agent演化过程 ✨
python interactive_evolution_demo.py  # 交互式深度分析演化
```

## 📖 完整文档

- **[GUIDE.md](GUIDE.md)** ⭐ 完整使用指南 **推荐从这里开始**
- **[AGENT_EVOLUTION_DEMO.md](AGENT_EVOLUTION_DEMO.md)** 🆕 演化演示完整指南 (看Agent如何改进!)
- [QUICKSTART.md](QUICKSTART.md) - 快速开始（5分钟）
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - 详细使用
- [ARCHITECTURE.md](ARCHITECTURE.md) - 系统设计

## ✨ 核心特性

- **🌐 自动数据采集** - 4个数据源，自动质量评估
- **🔄 自动性能优化** - 8维度指标，自适应策略
- **📊 完整评估体系** - 准确率、完整性等多维度评估
- **⚡ 代码优化** - 缓存、监测、并行处理
- **👥 用户反馈** - 满意度评估、反馈集成
- **🎯 自动收敛** - 多轮监测、早停机制

## 🏗️ 项目结构

```
Triplet-Qwen/
├── 核心模块 (生产代码)
│   ├── agent_a.py           # 三元组提取器 (Qwen模型)
│   ├── agent_b.py           # 三元组验证器 (规则引擎)
│   ├── data_crawler.py      # 多源数据采集
│   ├── evolution_system.py  # 自动演化引擎
│   ├── evaluation_metrics.py # 8维度性能评估
│   ├── code_optimization.py # 缓存和优化
│   └── integrated_evolution.py # 系统集成
│
├── 工具和演示
│   ├── triplet_qwen.py      # 统一API入口
│   ├── main.py              # 系统演示
│   ├── interactive.py       # 交互工具
│   ├── evolution_examples.py # 5个完整示例
│   ├── evolution_demo.py    # 🆕 可视化演化展示 (强烈推荐!)
│   ├── interactive_evolution_demo.py # 🆕 交互式演化分析
│   └── verify.py            # 系统验证
│
└── 文档
    ├── GUIDE.md             # 完整使用指南 (必读!)
    ├── QUICKSTART.md        # 快速开始
    ├── USAGE_GUIDE.md       # 详细使用
    └── ARCHITECTURE.md      # 系统设计
```

## 🚀 基本使用

### Python API

```python
from triplet_qwen import IntegratedEvolutionSystem, EvolutionConfig
from agent_a import TripletsExtractionAgent
from agent_b import TripletsValidationAgent

# 自定义配置
config = EvolutionConfig(
    max_iterations=50,           # 最多迭代50次
    target_accuracy=0.90,        # 目标准确率90%
    convergence_threshold=0.01   # 收敛阈值
)

# 创建系统
system = IntegratedEvolutionSystem(
    TripletsExtractionAgent(),
    TripletsValidationAgent(),
    config
)

# 运行自动演化
report = system.start_evolution()

# 添加用户反馈 (可选)
system.add_user_feedback(
    sentence='苹果是一种水果',
    triplet={'subject': '苹果', 'predicate': '是', 'object': '水果'},
    rating=9.0,
    feedback='完全正确'
)

# 查看结果
status = system.get_satisfaction_status()
print(f"最佳准确率: {report.best_metrics.accuracy:.4f}")
print(f"满意度: {status['satisfaction_level']}")
```

## 📊 性能指标

系统自动跟踪和优化8个维度的指标：

| 指标 | 说明 | 目标 |
|------|------|------|
| accuracy | 总体准确率 | ≥0.85 |
| precision | 精确率 | ≥0.85 |
| recall | 召回率 | ≥0.85 |
| f1_score | F1分数 | ≥0.85 |
| completeness | 信息完整性 | ≥0.80 |
| consistency | 结果稳定性 | ≥0.80 |
| argument_integrity | 论元完整性 | ≥0.80 |
| error_distribution | 错误分布 | 减少主要错误 |

## ⚙️ 配置参数

| 参数 | 默认值 | 范围 | 说明 |
|------|--------|------|------|
| max_iterations | 50 | 10-100 | 最大迭代次数 |
| convergence_threshold | 0.02 | 0.01-0.05 | 收敛阈值 |
| target_accuracy | 0.85 | 0.80-0.95 | 目标准确率 |
| crawl_frequency | 5 | 3-10 | 爬取新数据频率(轮数) |
| quality_threshold | 0.7 | 0.6-0.8 | 数据质量下限 |
| optimization_patience | 10 | 5-15 | 早停耐心(轮数) |

**调整指南**: 详见 [GUIDE.md#配置参数](GUIDE.md#配置参数)

## 🎯 "令人满意"的定义

系统达到以下条件即认为效果"令人满意"：

✓ accuracy ≥ 0.85  
✓ completeness ≥ 0.80  
✓ argument_integrity ≥ 0.80  
✓ (可选) 用户平均评分 ≥ 7.0/10  

## 🧪 测试和验证

```bash
# 运行集成测试 (验证系统功能)
python test_integration.py

# 系统验证 (检查环境和依赖)
python verify.py

# 查看5个完整示例
python evolution_examples.py
```

## 💡 常见问题

**Q: 演化需要多长时间？**
> A: 5-10分钟（默认配置）。可通过max_iterations调整。

**Q: 如何获得更好的结果？**
> A: (1) 增加max_iterations; (2) 降低quality_threshold; (3) 增加crawl_frequency; (4) 添加用户反馈

**Q: 内存占用过高？**
> A: 减少max_iterations或增加validation_ratio

**Q: 可以在自己的数据上运行吗？**
> A: 可以。修改data_crawler.py或在IntegratedEvolutionSystem中传递custom数据

**更多问题**: [GUIDE.md#常见问题](GUIDE.md#常见问题)

## 📈 预期效果

| 阶段 | 准确率 | 完整性 | 论元完整 | 状态 |
|------|--------|--------|----------|------|
| 初始 | ~60% | ~65% | ~70% | 基线 |
| 中期 (10轮) | ~75% | ~75% | ~78% | 逐步优化 |
| 后期 (30轮) | ~85% | ~85% | ~85% | 接近目标 |
| 最终 (50轮) | ~88% | ~87% | ~86% | 已收敛 ✓ |

## 📚 学习路径

### 初级用户 (5分钟)
1. 运行 `python main.py` 查看演示
2. 运行 `python evolution_examples.py`
3. 阅读 [QUICKSTART.md](QUICKSTART.md)

### 中级用户 (20分钟)
1. 阅读 [GUIDE.md](GUIDE.md) ⭐ **推荐**
2. 修改示例代码中的配置参数
3. 运行 `python test_integration.py` 验证系统

### 高级用户 (1小时)
1. 查看 [ARCHITECTURE.md](ARCHITECTURE.md) 了解设计
2. 修改源代码进行定制
3. 实现自定义数据源或评估指标

## 🔗 相关文档

- **主要**: [GUIDE.md](GUIDE.md) - 包含所有必需信息
- **快速**: [QUICKSTART.md](QUICKSTART.md) - 30秒快速开始
- **详细**: [USAGE_GUIDE.md](USAGE_GUIDE.md) - 深度使用指南
- **架构**: [ARCHITECTURE.md](ARCHITECTURE.md) - 系统设计详解
- **源码**: 所有.py文件都有详细注释

## 💻 系统要求

- Python 3.7+
- 4GB+ RAM（推荐8GB+）
- GPU (可选，但推荐用于更快速度)

## 📦 安装

```bash
# 安装依赖
pip install -r requirements.txt

# 验证安装
python verify.py
```

## 🎓 核心概念

### Agent A: 三元组提取器

从句子中提取三元组 `(Subject, Predicate, Object, Modifiers)`

```python
agent_a.extract_triplets("苹果是一种营养丰富的水果")
# 返回: {
#   'subject': '苹果',
#   'predicate': '是',
#   'object': '水果',
#   'mods': {'quality': '营养丰富'}
# }
```

### Agent B: 三元组验证器

验证提取的三元组的完整性和正确性

```python
agent_b.validate_triplet(sentence, triplet)
# 返回: {'is_valid': True, 'confidence': 0.95, ...}
```

### 演化系统

自动优化两个Agent的性能：
1. 定期采集数据 (4个来源)
2. 评估性能 (8维度指标)
3. 自动优化 (自适应策略)
4. 检测收敛 (自动停止)

## 📝 许可证

本项目为研究和学习用途。

---

## 🚀 快速导航

| 想要... | 查看... |
|---------|---------|
| 🎯 看Agent改进过程 | [AGENT_EVOLUTION_DEMO.md](AGENT_EVOLUTION_DEMO.md) 或 `python3 evolution_demo.py` |
| 30秒快速开始 | [QUICKSTART.md](QUICKSTART.md) |
| 完整使用指南 | [GUIDE.md](GUIDE.md) ⭐ |
| 系统架构设计 | [ARCHITECTURE.md](ARCHITECTURE.md) |
| 代码示例 | [evolution_examples.py](evolution_examples.py) |
| 系统演示 | `python main.py` |
| 一行代码启动 | `from triplet_qwen import quick_start; quick_start()` |

**建议**: 先运行 `python3 evolution_demo.py`（3-5分钟）看Agent演化过程，再阅读 [GUIDE.md](GUIDE.md)！
