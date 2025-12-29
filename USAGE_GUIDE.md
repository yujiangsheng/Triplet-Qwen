# 详细使用指南

## 快速开始

### 1. 环境安装

```bash
# 进入项目目录
cd /Users/jiangshengyu/Documents/program/python/Triplet-Qwen

# 安装依赖
pip install -r requirements.txt

# 下载Qwen模型（首次运行）
huggingface-cli download Qwen/Qwen2.5-0.5B-Instruct
```

### 2. 运行程序

#### 方案A: 批量处理（推荐演示用）

```bash
python main.py
```

这将处理预设的10个测试句子（中英文混合），自动抽取三元组、验证并修订。

#### 方案B: 交互式使用

```bash
# 交互模式
python interactive.py

# 批量模式
python interactive.py batch
```

#### 方案C: Python脚本中使用

```python
from model_loader import load_qwen_model
from agent_a import AgentA
from agent_b import AgentB
from dual_agent_system import DualAgentSystem

# 1. 加载模型
model, tokenizer, device = load_qwen_model()

# 2. 创建智能体
agent_a = AgentA(model, tokenizer, device)
agent_b = AgentB(model, tokenizer, device)

# 3. 创建系统
system = DualAgentSystem(agent_a, agent_b, max_iterations=3)

# 4. 处理句子
result = system.process_sentence("小明每天早上在公园跑步。")

# 5. 查看结果
print(f"三元组: {system._format_triplet_for_output(result['final_triplet'])}")
print(f"验证: {'通过' if result['is_valid'] else '失败'}")
```

## 系统架构

```
┌─────────────────────────────────────────┐
│        输入: 自然语言句子                  │
└────────────────────┬────────────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │  智能体A: 三元组抽取    │
         │  (AgentA)              │
         └────────────┬───────────┘
                      │
                      ▼ 初始三元组
         ┌────────────────────────┐
         │  智能体B: 三元组验证    │
         │  (AgentB)              │
         └────────────┬───────────┘
                      │
          ┌───────────┴────────────┐
          │                        │
      通过 │                    不通过
          │                        │
          │                        ▼
          │                ┌─────────────────┐
          │                │ 生成改进反馈     │
          │                └────────┬────────┘
          │                         │
          │                         ▼ 反馈
          │                ┌────────────────┐
          │                │ 智能体A修订    │
          │                │ 新三元组       │
          │                └────────┬───────┘
          │                         │
          │                  重复验证 ◀────┐
          │                         │     │
          └────────────────┬────────┘  (max_iter)
                           │
                           ▼
            ┌──────────────────────────┐
            │  输出: 最终三元组         │
            │  + 验证结果 + 迭代记录    │
            └──────────────────────────┘
```

## 输出说明

### 控制台输出

程序会实时输出处理过程：

```
======================================================================
开始处理句子: 小明每天早上在公园跑步。
======================================================================

[第1步] 智能体A进行初始三元组抽取...
[智能体A] 开始分析句子: 小明每天早上在公园跑步。
✓ 初始三元组: {time="每天早上", location="在公园"} 跑步(小明, null)

[第2步] 智能体B进行验证...
[智能体B] 开始验证三元组

============================================================
验证结果: ✓ 通过
============================================================
综合反馈: ✓ 三元组完整且正确，无需修改
============================================================
```

### 结果文件 (results.json)

```json
[
  {
    "sentence": "小明每天早上在公园跑步。",
    "final_triplet": "{time=\"每天早上\", location=\"在公园\"} 跑步(小明, null)",
    "is_valid": true,
    "iterations": 1,
    "status": "success"
  },
  {
    "sentence": "她很仔细地阅读了这本有趣的书。",
    "final_triplet": "{manner=\"很仔细\"} 阅读(她, 这本有趣的书)",
    "is_valid": true,
    "iterations": 1,
    "status": "success"
  }
]
```

## 三元组形式详解

### 完整形式

```
{mod1="value1", mod2="value2", ...} Predicate(Subject, Object)
```

### 组成部分

1. **修饰语 (Modifiers)**
   ```
   {time="每天早上", location="在公园"}
   ```
   - 格式: `key="value"`，多个用逗号分隔
   - 常见key: time, location, manner, cause, purpose
   - 可选（如果没有修饰语可省略）

2. **谓词 (Predicate)**
   ```
   跑步 / 阅读 / runs / reads
   ```
   - 动作或关系
   - 必须存在
   - 通常是动词

3. **主语 (Subject)**
   ```
   小明 / 她 / John / She
   ```
   - 施事者或经历者
   - ARG0在PropBank中
   - 必须存在，如果原句中无明确主语则为null

4. **宾语 (Object)**
   ```
   null / 这本书 / the book
   ```
   - 受事者或主题
   - ARG1在PropBank中
   - 可选，不存在时为null

### 真实示例

#### 例1: 时间和地点修饰
```
句子: "小明每天早上在公园跑步。"
分析:
  - Subject: 小明 (ARG0-Agent)
  - Predicate: 跑步 (行动)
  - Object: null (没有直接受事者)
  - Time: 每天早上
  - Location: 在公园
三元组: {time="每天早上", location="在公园"} 跑步(小明, null)
```

#### 例2: 方式修饰
```
句子: "她很仔细地阅读了这本有趣的书。"
分析:
  - Subject: 她 (ARG0-Experiencer)
  - Predicate: 阅读 (行动)
  - Object: 这本有趣的书 (ARG1-Patient)
  - Manner: 很仔细
三元组: {manner="很仔细"} 阅读(她, 这本有趣的书)
```

#### 例3: 工具修饰（英文）
```
句子: "The teacher explained the problem using chalk."
分析:
  - Subject: The teacher (ARG0-Agent)
  - Predicate: explained (动作)
  - Object: the problem (ARG1-Theme)
  - Instrument: using chalk
三元组: {instrument="using chalk"} explained(The teacher, the problem)
```

## 验证过程详解

智能体B进行四层验证：

### 第1层: 结构检查
```
✓ 检查项:
  - 是否有谓词
  - 是否有主语
  - 修饰语格式是否正确
```

### 第2层: 语义完整性检查
```
✓ 检查项:
  - 所有关键实体是否被捕获
  - 时间信息是否完整
  - 地点信息是否完整
  - 方式和其他修饰信息是否完整
```

### 第3层: 可恢复性检查
```
✓ 检查项:
  - 能否从三元组恢复原句的核心含义
  - 是否遗漏了重要的修饰信息
  - 信息是否充分
```

### 第4层: 模型深层验证
```
✓ 使用LLM验证:
  - 三元组是否完整反映语义
  - 是否有遗漏的重要信息
  - 从三元组是否能恢复原句
  - 具体改进建议
```

## 修订过程

当验证失败时，智能体A会根据反馈修订三元组：

```
初始三元组: {location="公园"} 跑步(小明, null)
验证反馈: 缺失time修饰语，原句中有"每天早上"
修订后: {time="每天早上", location="在公园"} 跑步(小明, null)
```

迭代过程会继续，直到：
1. ✓ 验证通过，或
2. ✓ 达到最大迭代次数（默认3次）

## 常见问题

### Q1: 模型输出不稳定

**解决方案:**
- 降低temperature参数（更确定的输出）
- 增加max_iterations进行更多轮修订
- 使用seed固定随机性

```python
# 在generate_response中修改
response = model.generate(
    ...,
    temperature=0.1,  # 更低的温度
    seed=42,  # 固定seed
)
```

### Q2: 某些句子验证失败

**原因分析:**
- 句子过于复杂，包含多个谓词
- 包含隐性的主语或宾语
- 包含特殊的语法结构

**解决方案:**
- 增加max_iterations
- 调整提示词的定义
- 对特殊句式预处理

### Q3: 英文句子处理效果不如中文

**原因:**
- Qwen2.5-0.5B的中文优化较好
- 可能需要调整提示词语言

**解决方案:**
- 在提示词中用英文示例
- 修改agent_a.py的_build_extraction_prompt方法

```python
# 添加更多英文示例
prompt = """...
Examples:
- "John runs in the park daily." → 
  {time="daily", location="in the park"} runs(John, null)
...
"""
```

### Q4: 显存占用过高

**解决方案:**
- 使用float16或int8量化
- 减小batch_size
- 使用CPU推理（虽然较慢）

```python
# 在model_loader.py中修改
torch_dtype = torch.float16  # 使用半精度
# 或
device_map = {"": "cpu"}  # 强制CPU
```

### Q5: 如何处理特定领域的语义角色

**方案:**
1. 修改config.py中的SEMANTIC_ROLES
2. 更新agent_a.py中的提示词
3. 添加领域特定的关键词

```python
# config.py
SEMANTIC_ROLES = {
    "AGENT": "ARG0",
    "PATIENT": "ARG1",
    "MEDICAL_INSTRUMENT": "ARG2",  # 医疗领域
    ...
}
```

## 性能优化建议

### 1. 批量处理
```python
# 批量处理多个句子，减少模型加载开销
sentences = [...]
results = system.process_batch(sentences, save_results=True)
```

### 2. 缓存机制
```python
# 为相似句子缓存结果
cache = {}
for sentence in sentences:
    if sentence not in cache:
        cache[sentence] = system.process_sentence(sentence)
```

### 3. 并行处理
```python
# 使用多进程处理
from concurrent.futures import ProcessPoolExecutor
with ProcessPoolExecutor(max_workers=4) as executor:
    results = executor.map(system.process_sentence, sentences)
```

### 4. 减少迭代
```python
# 如果准确性要求不极高，减少迭代
system = DualAgentSystem(agent_a, agent_b, max_iterations=1)
```

## 扩展开发

### 自定义语义角色

修改 `agent_a.py` 中的提示词：

```python
def _build_extraction_prompt(self, sentence: str) -> str:
    prompt = f"""...
    语义角色定义:
    - 自定义角色1: 说明
    - 自定义角色2: 说明
    ...
    """
    return prompt
```

### 添加新的验证规则

在 `agent_b.py` 中添加新的检查方法：

```python
def _check_custom_rule(self, sentence: str, triplet: Dict) -> Dict:
    issues = []
    # 自定义检查逻辑
    return {
        'valid': len(issues) == 0,
        'issues': issues
    }
```

### 集成知识库

```python
# 在validation中添加知识图谱检查
from my_knowledge_base import check_relation

def validate_against_kb(self, triplet):
    predicate = triplet['predicate']
    subject = triplet['subject']
    obj = triplet['object']
    
    is_valid = check_relation(predicate, subject, obj)
    return is_valid
```

## 许可证和引用

如在学术研究中使用，请引用：

```bibtex
@software{triplet_qwen_2025,
  title={Dual-Agent Semantic Triplet Extraction System with Qwen2.5-0.5B},
  author={Author},
  year={2025},
  url={https://github.com/...}
}
```

## 反馈和改进

欢迎提出建议和改进方向：
- 提高三元组抽取准确率
- 支持更多语言
- 集成更多语义角色标注规范
- 性能优化

---

**文档版本**: 1.0  
**最后更新**: 2025-12-28
