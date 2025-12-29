# 📚 文档索引和快速导航

## 🎯 按需求快速找到你需要的信息

### 我是第一次使用

**推荐路径:** 5分钟快速上手

1. **先读这个**: [QUICKSTART.md](QUICKSTART.md)
   - 30秒快速开始
   - 基本概念说明
   - 常见问题解答

2. **再运行这个**:
   ```bash
   python main.py
   ```
   观察系统工作流程

3. **试试这个**:
   ```bash
   python interactive.py
   ```
   自己输入句子测试

---

### 我想深入理解系统

**推荐路径:** 30分钟完全理解

1. **阅读架构** → [ARCHITECTURE.md](ARCHITECTURE.md)
   - 系统整体设计
   - 技术亮点
   - 性能指标

2. **查看代码** → 核心模块
   - [model_loader.py](model_loader.py) - 模型管理
   - [agent_a.py](agent_a.py) - 三元组抽取
   - [agent_b.py](agent_b.py) - 三元组验证
   - [dual_agent_system.py](dual_agent_system.py) - 协作框架

3. **运行验证** → 系统检查
   ```bash
   python verify.py
   ```

---

### 我想进行实际应用

**推荐路径:** 完整的使用教程

1. **查看详细指南** → [USAGE_GUIDE.md](USAGE_GUIDE.md)
   - 安装和配置
   - 详细使用方法
   - 性能优化
   - 扩展开发

2. **代码集成** → 在你的项目中使用
   ```python
   from dual_agent_system import DualAgentSystem
   ```
   查看[USAGE_GUIDE.md#编程调用](USAGE_GUIDE.md)中的示例

3. **自定义配置** → 修改 [config.py](config.py)

---

### 我遇到了问题

**问题排查指南:**

1. **运行系统检查**:
   ```bash
   python verify.py
   ```

2. **查看常见问题**:
   - [QUICKSTART.md#常见问题](QUICKSTART.md)
   - [USAGE_GUIDE.md#常见问题](USAGE_GUIDE.md)

3. **检查代码注释**:
   - 所有模块都有详细的中英文注释
   - 查看相关的.py文件

4. **阅读完整文档**:
   - [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 项目完成总结

---

### 我想扩展或改进系统

**开发者指南:**

1. **理解架构** → [ARCHITECTURE.md#扩展功能](ARCHITECTURE.md)

2. **学习扩展方法** → [USAGE_GUIDE.md#扩展开发](USAGE_GUIDE.md)

3. **修改配置** → [config.py](config.py)
   - 添加新的语义角色
   - 调整生成参数

4. **自定义验证规则** → [agent_b.py](agent_b.py)
   - 添加新的检查方法
   - 集成知识库

---

## 📖 完整文档列表

### 核心文档

| 文档 | 内容 | 阅读时间 | 适合人群 |
|------|------|--------|--------|
| [QUICKSTART.md](QUICKSTART.md) | 30秒快速开始 | 5分钟 | 所有人 |
| [README.md](README.md) | 项目介绍 | 10分钟 | 初学者 |
| [ARCHITECTURE.md](ARCHITECTURE.md) | 架构设计详解 | 20分钟 | 开发者 |
| [USAGE_GUIDE.md](USAGE_GUIDE.md) | 完整使用教程 | 30分钟 | 实际应用 |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 项目完成总结 | 15分钟 | 了解全貌 |

### 代码模块

| 文件 | 功能 | 行数 | 复杂度 |
|------|------|------|--------|
| [model_loader.py](model_loader.py) | 模型加载和设备管理 | 90 | ⭐ |
| [agent_a.py](agent_a.py) | 语义三元组抽取 | 265 | ⭐⭐⭐ |
| [agent_b.py](agent_b.py) | 三元组验证和反馈 | 330 | ⭐⭐⭐ |
| [dual_agent_system.py](dual_agent_system.py) | 双智能体协作框架 | 220 | ⭐⭐ |
| [config.py](config.py) | 系统配置 | 95 | ⭐ |

### 可执行脚本

| 脚本 | 用途 | 使用场景 |
|------|------|--------|
| [main.py](main.py) | 批量演示 | 查看系统效果 |
| [interactive.py](interactive.py) | 交互式使用 | 手动测试 |
| [verify.py](verify.py) | 系统验证 | 问题排查 |

---

## 🔍 按功能查找

### 想了解"三元组格式"

- 快速答案 → [QUICKSTART.md#核心概念](QUICKSTART.md)
- 详细说明 → [README.md#三元组形式说明](README.md)
- 完整例子 → [USAGE_GUIDE.md#三元组形式详解](USAGE_GUIDE.md)

### 想了解"智能体A"的工作原理

- 代码 → [agent_a.py](agent_a.py)
- 文档 → [ARCHITECTURE.md#智能体A](ARCHITECTURE.md)
- 示例 → [USAGE_GUIDE.md#工作流示例](USAGE_GUIDE.md)

### 想了解"智能体B"的验证流程

- 代码 → [agent_b.py](agent_b.py)
- 文档 → [ARCHITECTURE.md#智能体B](ARCHITECTURE.md)
- 详解 → [USAGE_GUIDE.md#验证过程详解](USAGE_GUIDE.md)

### 想了解"设备选择"

- 代码 → [model_loader.py#get_device](model_loader.py)
- 说明 → [README.md#设备支持](README.md)
- 配置 → [ARCHITECTURE.md#设备优化](ARCHITECTURE.md)

### 想了解"语义角色标注规范"

- 基本定义 → [README.md#语义角色标注规范](README.md)
- 详细规范 → [ARCHITECTURE.md#语义角色标注规范](ARCHITECTURE.md)
- 配置定制 → [config.py#SEMANTIC_ROLES](config.py)

---

## 🚀 快速命令参考

### 安装和初始化

```bash
# 1. 进入项目目录
cd /Users/jiangshengyu/Documents/program/python/Triplet-Qwen

# 2. 安装依赖
pip install -r requirements.txt

# 3. 下载模型 (首次)
huggingface-cli download Qwen/Qwen2.5-0.5B-Instruct
```

### 运行程序

```bash
# 系统验证 (检查完整性)
python verify.py

# 批量演示 (看效果)
python main.py

# 交互式使用 (自己测试)
python interactive.py

# 批量演示模式
python interactive.py batch
```

### 在Python中使用

```python
# 导入
from model_loader import load_qwen_model
from agent_a import AgentA
from agent_b import AgentB
from dual_agent_system import DualAgentSystem

# 初始化
model, tokenizer, device = load_qwen_model()
system = DualAgentSystem(
    AgentA(model, tokenizer, device),
    AgentB(model, tokenizer, device)
)

# 处理
result = system.process_sentence("你的句子")
```

---

## 📊 项目统计

```
总代码行数: ~1,500行
总文档行数: ~1,500行
核心模块: 5个
可执行脚本: 3个
文档数量: 5份
总文件数: 13个
```

---

## 🎓 学习路线图

### 🔵 初级 (了解系统)

```
1. 阅读 QUICKSTART.md (5分钟)
   ↓
2. 运行 main.py (2分钟)
   ↓
3. 试用 interactive.py (5分钟)
   ↓
✓ 完成 (12分钟) - 了解系统基本功能
```

### 🟡 中级 (使用系统)

```
1. 阅读 README.md (10分钟)
   ↓
2. 阅读 ARCHITECTURE.md (20分钟)
   ↓
3. 修改 config.py (5分钟)
   ↓
4. 运行 verify.py (2分钟)
   ↓
✓ 完成 (37分钟) - 能独立使用和配置
```

### 🔴 高级 (扩展系统)

```
1. 学习 USAGE_GUIDE.md (30分钟)
   ↓
2. 阅读代码注释 (30分钟)
   ↓
3. 修改提示词 (15分钟)
   ↓
4. 添加自定义规则 (30分钟)
   ↓
5. 集成知识库 (60分钟)
   ↓
✓ 完成 (165分钟) - 能扩展和定制系统
```

---

## 💡 常用查询表

### "怎样...?" 快速查询

| 问题 | 查看位置 |
|------|---------|
| 怎样安装? | [QUICKSTART.md](QUICKSTART.md) 或 [USAGE_GUIDE.md](USAGE_GUIDE.md) |
| 怎样运行? | [QUICKSTART.md](QUICKSTART.md) 或 [main.py](main.py) |
| 怎样修改参数? | [config.py](config.py) 或 [USAGE_GUIDE.md](USAGE_GUIDE.md) |
| 怎样自定义? | [USAGE_GUIDE.md#扩展开发](USAGE_GUIDE.md) |
| 怎样排查问题? | [QUICKSTART.md#常见问题](QUICKSTART.md) 或 [USAGE_GUIDE.md#常见问题](USAGE_GUIDE.md) |
| 怎样提高性能? | [USAGE_GUIDE.md#性能优化建议](USAGE_GUIDE.md) |
| 怎样处理批量数据? | [USAGE_GUIDE.md#批量处理](USAGE_GUIDE.md) |

### "是什么...?" 快速查询

| 问题 | 查看位置 |
|------|---------|
| 三元组是什么? | [README.md](README.md) 或 [QUICKSTART.md](QUICKSTART.md) |
| 智能体A是什么? | [ARCHITECTURE.md#智能体A](ARCHITECTURE.md) |
| 智能体B是什么? | [ARCHITECTURE.md#智能体B](ARCHITECTURE.md) |
| PropBank是什么? | [ARCHITECTURE.md](ARCHITECTURE.md) 或 [README.md](README.md) |
| FrameNet是什么? | [ARCHITECTURE.md](ARCHITECTURE.md) 或 [README.md](README.md) |
| 修饰语是什么? | [USAGE_GUIDE.md](USAGE_GUIDE.md) |

---

## 🔗 内部链接速查

### 主要概念
- [设备选择](ARCHITECTURE.md#设备优化)
- [三元组格式](QUICKSTART.md#核心概念)
- [语义角色](ARCHITECTURE.md#语义角色标注规范)
- [验证流程](USAGE_GUIDE.md#验证过程详解)

### 使用指南
- [快速开始](QUICKSTART.md)
- [安装步骤](USAGE_GUIDE.md#安装和使用)
- [配置调整](USAGE_GUIDE.md#参数调优)
- [常见问题](QUICKSTART.md#常见问题)

### 扩展资料
- [扩展开发](USAGE_GUIDE.md#扩展开发)
- [性能优化](USAGE_GUIDE.md#性能优化建议)
- [问题排查](USAGE_GUIDE.md#常见问题)

### 外部资源
- [PropBank官网](https://propbank.github.io/)
- [FrameNet官网](https://framenet.icsi.berkeley.edu/)
- [Qwen GitHub](https://github.com/QwenLM/Qwen)
- [Hugging Face](https://huggingface.co/)

---

## 📞 获取帮助

### 第一步: 自助查阅

1. 浏览本页的[快速查询](#-常用查询表)
2. 搜索相关关键词在各文档中
3. 查看代码注释

### 第二步: 系统诊断

```bash
# 运行系统检查
python verify.py

# 查看输出，根据失败项目进行排查
```

### 第三步: 深度学习

1. 阅读[ARCHITECTURE.md](ARCHITECTURE.md)
2. 研究相关代码
3. 尝试修改和测试

---

## 🌟 项目亮点快速导航

| 亮点 | 详见 |
|------|------|
| 双智能体设计 | [ARCHITECTURE.md](ARCHITECTURE.md) |
| 多层验证机制 | [USAGE_GUIDE.md#验证过程详解](USAGE_GUIDE.md) |
| 自动迭代改进 | [QUICKSTART.md](QUICKSTART.md) |
| GPU/MPS/CPU自动选择 | [model_loader.py](model_loader.py) |
| 中英文完全支持 | [README.md](README.md) |
| 规范的语义标注 | [config.py](config.py) |

---

**提示**: 本文档可作为快速参考指南，建议收藏！

最后更新: 2025-12-28
