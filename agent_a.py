"""
智能体A - 语义三元组抽取器

根据FrameNet和PropBank的语义角色标注规范，从中英文自然语言句子中抽取扩展三元组。
形式: {mods} Predicate(Subject, Object)

核心特性:
1. 支持单句和多句批量三元组抽取
2. 遵循PropBank和FrameNet的语义角色标准
3. 详细捕获语义修饰信息(时间、地点、方式、原因、目的、工具等)
4. 支持多轮迭代修订，与智能体B协作改进结果

使用示例:
    >>> agent = AgentA(model, tokenizer, device)
    
    # 单句抽取
    >>> triplet = agent.extract_triplets("小明每天早上在公园跑步。")
    >>> print(agent.format_output(triplet))
    {time="每天早上", location="在公园"} 跑步(小明, null)
    
    # 多句抽取
    >>> sentences = ["她仔细地阅读了那本书。", "张三在北京工作。"]
    >>> triplets = agent.extract_triplets_batch(sentences)
    >>> for triplet in triplets:
    ...     print(agent.format_output(triplet))
    {manner="仔细"} 阅读(她, 那本书)
    {} 工作(张三, null)
"""

import json
import re
from typing import Dict, List, Any, Union
from model_loader import generate_response


class AgentA:
    """
    语义三元组抽取智能体 (Semantic Triplet Extraction Agent)
    
    = 三元组形式 =
    {mods} Predicate(Subject, Object)
    
    其中:
    - mods: 语义修饰语 (可选), 形如 {key1="value1", key2="value2", ...}
    - Predicate: 谓词/动作 (必需)
    - Subject: 主语/施事者 (可选, 若无则为null)
    - Object: 宾语/受事者 (可选, 若无则为null)
    
    = 语义角色定义 =
    
    核心论元 (PropBank ARG0-ARG1, FrameNet Core Roles):
    - ARG0 (Agent/Subject): 施事者、主语
      例: 在"小明踢球"中，小明是ARG0
    - ARG1 (Patient/Theme/Object): 受事者、主题
      例: 在"张三建造房子"中，房子是ARG1
    
    扩展论元 (Adjuncts/修饰语):
    - time (ARG/ArgM-TMP): 时间信息
      例: "每天"、"昨天下午"、"明年夏天"
    - location (ARG/ArgM-LOC): 地点信息
      例: "在公园"、"北京"、"办公室里"
    - manner (ArgM-MNR): 方式/方法
      例: "快速地"、"仔细"、"轻声地"
    - cause (ArgM-CAU): 原因/理由
      例: "由于下雨"、"因为累了"
    - purpose (ArgM-PRP): 目的/意图
      例: "为了学习"、"以便休息"
    - tool (ArgM-TLS): 工具/手段
      例: "用笔"、"通过电话"、"借助软件"
    - direction (ArgM-DIR): 方向
      例: "向东"、"从北到南"
    - destination (ArgM-GOL): 目的地
      例: "到北京"、"去医院"
    - source (ArgM-SRC): 来源
      例: "从家里"、"来自日本"
    - attribute (ArgM-ATT): 属性/特征
      例: "很大的"、"蓝色的"
    - modal (ArgM-MOD): 情态/可能性
      例: "可能"、"应该"、"必定"
    - negation (ArgM-NEG): 否定
      例: "没有"、"不"
    - frequency (ArgM-FRQ): 频率
      例: "经常"、"每次"、"从不"
    - degree (ArgM-EXT): 程度/范围
      例: "非常"、"一点点"、"很"
    
    = 使用示例 =
    
    >>> agent = AgentA(model, tokenizer, device)
    
    # 单句抽取
    >>> result = agent.extract_triplets("小明每天早上在公园跑步。")
    >>> print(result['triplet'])
    {
        'sentence': '小明每天早上在公园跑步。',
        'mods': {'time': '每天早上', 'location': '在公园'},
        'predicate': '跑步',
        'subject': '小明',
        'object': None,
        ...
    }
    
    # 多句批量抽取
    >>> sentences = [
    ...     "她用钉子钉住了这块木板。",
    ...     "我每个周末都在图书馆学习。",
    ...     "由于天气原因，比赛被延期了。"
    ... ]
    >>> results = agent.extract_triplets_batch(sentences)
    >>> for res in results:
    ...     print(agent.format_output(res['triplet']))
    {tool="用钉子"} 钉住(她, 这块木板)
    {frequency="每个周末", location="在图书馆"} 学习(我, null)
    {cause="由于天气原因"} 延期(比赛, null)
    
    # 根据反馈修订
    >>> feedback = "缺少受事者信息"
    >>> revised = agent.revise_triplet(feedback, result)
    """
    
    def __init__(self, model, tokenizer, device):
        """
        初始化智能体A
        
        Args:
            model: Qwen2.5-0.5B-instruct 模型
            tokenizer: 对应的分词器
            device: 计算设备 (优先级: GPU > MPS > CPU)
        """
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.extraction_history = []  # 记录抽取历史，用于追踪修订过程
    
    def extract_triplets(self, sentence: Union[str, List[str]], max_retries: int = 1) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        从句子（单句或多句）中抽取语义三元组
        
        支持两种用法:
        (1) 单句模式: 输入单个字符串，返回单个三元组字典
        (2) 多句模式: 输入字符串列表，返回三元组字典列表
        
        Args:
            sentence (Union[str, List[str]]): 
                - 单句: 字符串，如 "小明在公园跑步。"
                - 多句: 列表，如 ["句子1。", "句子2。", "句子3。"]
            max_retries: 最大重试次数 (暂未使用，保留接口)
            
        Returns:
            Union[Dict, List[Dict]]: 
                - 单句模式返回: 包含三元组信息的字典
                - 多句模式返回: 三元组字典列表
                
        示例:
            >>> # 单句
            >>> result = agent.extract_triplets("她在图书馆学习。")
            >>> print(result['triplet']['predicate'])  # '学习'
            
            >>> # 多句
            >>> results = agent.extract_triplets(["句子1。", "句子2。"])
            >>> print(len(results))  # 2
            >>> for r in results:
            ...     print(r['triplet']['predicate'])
        """
        # 判断是多句还是单句
        if isinstance(sentence, list):
            # 多句批量处理
            return self.extract_triplets_batch(sentence)
        else:
            # 单句处理
            return self._extract_single_triplet(sentence, max_retries)
    
    def _extract_single_triplet(self, sentence: str, max_retries: int = 1) -> Dict[str, Any]:
        """
        内部方法: 从单个句子中抽取语义三元组
        
        Args:
            sentence (str): 单个输入句子
            max_retries (int): 最大重试次数
            
        Returns:
            Dict[str, Any]: 包含以下键的字典:
                - sentence: 原始句子
                - triplet: 抽取的三元组 (包含mods, predicate, subject, object等)
                - raw_response: 模型的原始输出
                - attempt: 第几次尝试
                - error: 如果出错，记录错误信息
        """
        print(f"\n[智能体A] 开始分析句子: {sentence}")
        
        extraction_prompt = self._build_extraction_prompt(sentence)
        
        try:
            response = generate_response(
                self.model,
                self.tokenizer,
                extraction_prompt,
                self.device,
                max_new_tokens=256,
                temperature=0.3,  # 降低温度以获得更一致的结果
            )
            
            triplet = self._parse_triplet_response(response, sentence)
            triplet['raw_response'] = response
            triplet['attempt'] = 1
            
            self.extraction_history.append({
                'sentence': sentence,
                'triplet': triplet,
                'attempt': 1
            })
            
            return {
                'sentence': sentence,
                'triplet': triplet,
                'raw_response': response,
                'attempt': 1
            }
            
        except Exception as e:
            print(f"✗ 抽取失败: {e}")
            return {
                'error': str(e),
                'sentence': sentence,
                'triplet': None,
                'attempt': 1
            }
    
    def extract_triplets_batch(self, sentences: List[str]) -> List[Dict[str, Any]]:
        """
        批量抽取多个句子的语义三元组
        
        此方法适合处理多个句子或段落的场景，返回每个句子对应的三元组。
        
        Args:
            sentences (List[str]): 句子列表
                示例: ["小明跑步。", "她读书。", "我们学习。"]
            
        Returns:
            List[Dict[str, Any]]: 三元组字典列表，顺序与输入对应
                每个字典包含:
                - sentence: 原始句子
                - triplet: 抽取的三元组
                - raw_response: 模型原始输出
                - attempt: 尝试次数
                - error: 错误信息 (如果有)
                
        示例:
            >>> sentences = [
            ...     "小明每天在公园跑步。",
            ...     "她用笔仔细地写字。",
            ...     "我们必须按时完成任务。"
            ... ]
            >>> results = agent.extract_triplets_batch(sentences)
            >>> for res in results:
            ...     if 'triplet' in res and res['triplet']:
            ...         print(agent.format_output(res['triplet']))
            {time="每天", location="在公园"} 跑步(小明, null)
            {tool="用笔", manner="仔细"} 写字(她, null)
            {modal="必须", frequency="按时"} 完成(我们, 任务)
        """
        print(f"\n[智能体A] 批量处理 {len(sentences)} 个句子")
        
        results = []
        for idx, sentence in enumerate(sentences, 1):
            print(f"  [{idx}/{len(sentences)}] 处理: {sentence}")
            result = self._extract_single_triplet(sentence)
            results.append(result)
        
        return results
    
    def revise_triplet(self, feedback: str, original_triplet: Dict) -> Dict[str, Any]:
        """
        根据智能体B的反馈修订三元组
        
        这是双智能体协作流程中的关键步骤:
        1. 智能体A提取初始三元组
        2. 智能体B进行语义验证并提出反馈
        3. 智能体A根据反馈修订三元组
        4. 重复2-3步直到没有错误
        
        Args:
            feedback (str): 智能体B提出的反馈
                示例: "缺少'地点'修饰语", "Subject应该是'他们'而不是'他'"
            original_triplet (Dict): 原始三元组结果，应包含:
                - sentence: 原始句子
                - triplet: 上一版本的三元组
                - attempt: 当前尝试次数
            
        Returns:
            Dict[str, Any]: 修订后的三元组，包含:
                - sentence: 原始句子
                - triplet: 修订后的三元组
                - raw_response: 模型原始输出
                - attempt: 尝试次数 (当前attempt + 1)
                - feedback: 收到的反馈
                
        使用示例:
            >>> # 初始抽取
            >>> result = agent.extract_triplets("张三用刀切割了木头。")
            >>> print(agent.format_output(result['triplet']))
            {} 切割(张三, 木头)
            
            >>> # 智能体B发现缺少工具信息，给出反馈
            >>> feedback = "缺少'工具'修饰语，应该包含'用刀'"
            >>> revised = agent.revise_triplet(feedback, result)
            >>> print(agent.format_output(revised['triplet']))
            {tool="用刀"} 切割(张三, 木头)
        """
        print(f"\n[智能体A] 第 {original_triplet.get('attempt', 1) + 1} 轮修订")
        print(f"  原反馈: {feedback}")
        
        revision_prompt = self._build_revision_prompt(
            original_triplet['sentence'],
            original_triplet['triplet'],
            feedback
        )
        
        try:
            response = generate_response(
                self.model,
                self.tokenizer,
                revision_prompt,
                self.device,
                max_new_tokens=256,
                temperature=0.3,
            )
            
            revised_triplet = self._parse_triplet_response(
                response,
                original_triplet['sentence']
            )
            revised_triplet['raw_response'] = response
            revised_triplet['attempt'] = original_triplet.get('attempt', 1) + 1
            
            self.extraction_history.append({
                'sentence': original_triplet['sentence'],
                'triplet': revised_triplet,
                'attempt': revised_triplet['attempt'],
                'feedback': feedback
            })
            
            return {
                'sentence': original_triplet['sentence'],
                'triplet': revised_triplet,
                'raw_response': response,
                'attempt': revised_triplet['attempt'],
                'feedback': feedback
            }
            
        except Exception as e:
            print(f"✗ 修订失败: {e}")
            return original_triplet
    
    def _build_extraction_prompt(self, sentence: str) -> str:
        """
        构建三元组抽取提示词（Prompt Engineering）
        
        采用few-shot学习策略，通过多个例子引导模型学习正确的抽取方式。
        
        Args:
            sentence: 待分析的输入句子
            
        Returns:
            完整的提示词，包含任务说明、语义角色定义和示例
        """
        
        prompt = f"""你是一个专业的NLP语义分析专家，精通PropBank和FrameNet语义角色标注体系。

=== 任务 ===
从中文或英文句子中准确地抽取语义三元组，格式为: {{mods}} Predicate(Subject, Object)

=== 核心论元定义 ===
- Subject (ARG0 in PropBank): 主语、施事者、主体
  例如："小明"在"小明跑步"中是施事者
- Object (ARG1 in PropBank): 宾语、受事者、主题、患者
  例如："书"在"我读书"中是受事者/主题

=== 语义修饰语定义 (ArgM in PropBank, Peripheral/Extra-thematic in FrameNet) ===

[时间相关 Temporal]
- time: 时间或时间段
  例: "每天", "昨天上午", "2024年", "周末"
- frequency: 频率、频次
  例: "经常", "有时", "从不", "每次"

[空间相关 Spatial]
- location: 地点、位置
  例: "在公园", "北京", "办公室里"
- source: 来源、起点
  例: "从家", "来自日本"
- destination: 目的地、终点
  例: "到医院", "去北京", "向东"
- direction: 方向
  例: "向北", "从东到西"

[方式手段 Manner & Means]
- manner: 做事的方式、态度、风格
  例: "仔细地", "快速", "轻轻地", "小心翼翼"
- tool: 使用的工具、手段、方式
  例: "用笔", "通过电话", "借助软件", "依靠"
- attribute: 属性、特征描述
  例: "很大的", "蓝色的", "新的"

[因果目的 Causality & Purpose]
- cause: 原因、理由、触发因素
  例: "由于下雨", "因为累了", "受伤"
- purpose: 目的、意图、目标
  例: "为了学习", "以便休息", "为了赚钱"

[程度情态 Degree & Modality]
- degree: 程度、范围、强度
  例: "非常", "一点点", "很", "完全"
- modal: 情态、可能性、必要性
  例: "可能", "应该", "必须", "可以"
- negation: 否定
  例: "没有", "不", "无法"

=== 输出格式 ===
{{key1="value1", key2="value2", ...}} Predicate(Subject, Object)

说明:
- {{...}}: 包含所有识别的修饰语，如果没有则为空 {{}}
- Predicate: 谓词、动词、事件名称（必须）
- Subject: 主语，如果不存在则写 null
- Object: 宾语，如果不存在则写 null
- 修饰语的顺序: 时间 > 地点 > 方式 > 原因 > 目的 > 其他

=== 抽取示例 ===

例1: "小明每天早上在公园跑步。"
→ {{time="每天早上", location="在公园"}} 跑步(小明, null)
说明: time和location是修饰语；跑步是谓词；小明是施事者；没有受事者

例2: "她用钉子仔细地钉住了这块木板。"
→ {{tool="用钉子", manner="仔细"}} 钉住(她, 这块木板)
说明: 工具和方式是修饰语；钉住是谓词；她是施事者；木板是受事者

例3: "我们必须为了赶上截止时间而加班工作。"
→ {{modal="必须", purpose="为了赶上截止时间"}} 工作(我们, null)
情态和目的修饰了工作这个动作

例4: "由于天气原因，明天的比赛被延期了。"
→ {{cause="由于天气原因", time="明天"}} 延期(比赛, null)
说明: 原因和时间修饰了延期；比赛是受事者（被动语态中的施事）

例5: "Tom quickly walked to the library yesterday."
→ {{manner="quickly", time="yesterday", destination="to the library"}} walked(Tom, null)
英文示例：manner(快速地)、time(昨天)、destination(目的地)

例6: "那个高大的男人在远方的山上看到了一只鸟。"
→ {{location="在远方的山上"}} 看到(高大的男人, 一只鸟)
说明: "高大的"修饰Subject中的"男人"，应该保留在Subject里，不作为修饰语
     "一只"修饰Object中的"鸟"，应该保留在Object里
     location应该完整保留"在远方的山上"，不应简化

=== 关键提示 ===
1. 只输出三元组信息，不需要解释或其他内容
2. 仔细识别所有语义修饰语，不要遗漏
3. 正确区分主语和宾语，保持其完整性
4. 对修饰语的值提取要完整准确，包括修饰主语/宾语的形容词
5. Subject和Object应该保持完整，包含对它们的所有形容词修饰
   例: "那个高大的男人" → Subject应该是 "高大的男人" 或 "那个高大的男人"，而不是简化为 "男人"
   例: "一本很厚的书" → Object应该保留 "一本很厚的书"，不简化为 "书"
6. 如果某个论元或修饰语不存在，不要强行添加

=== 待分析句子 ===
"{sentence}"

请按照上述格式输出三元组，只输出结果行，不需要其他说明:"""
        
        return prompt
    
    def _build_revision_prompt(self, sentence: str, triplet: Dict, feedback: str) -> str:
        """
        构建修订提示词
        
        当智能体B检测到三元组有问题时，引导智能体A进行改进。
        
        Args:
            sentence: 原始句子
            triplet: 前一版本的三元组
            feedback: 智能体B提出的具体反馈
            
        Returns:
            包含反馈信息的修订提示词
        """
        
        triplet_str = self._format_triplet(triplet)
        
        prompt = f"""你是一个NLP语义分析专家。现在需要根据验证反馈来改进你的抽取结果。

=== 原始句子 ===
"{sentence}"

=== 你之前的三元组 ===
{triplet_str}

=== 验证反馈 ===
{feedback}

=== 任务 ===
根据反馈，重新分析句子并修订三元组。确保修订后的三元组能够：
1. 完整地反映原句的所有语义信息
2. 正确识别所有语义修饰语（时间、地点、方式、原因、目的、工具等）
3. 准确提取主语和宾语
4. 可以通过三元组恢复原句的语义

=== 输出格式 ===
{{key1="value1", ...}} Predicate(Subject, Object)

请仔细分析反馈，修订并只输出新的三元组："""
        
        return prompt
    
    def _parse_triplet_response(self, response: str, sentence: str) -> Dict:
        """
        解析模型生成的三元组响应
        
        使用正则表达式从模型输出中精确抽取修饰语、谓词、主语和宾语。
        
        Args:
            response (str): 模型生成的原始文本
                期望格式: {time="...", location="..."} Predicate(Subject, Object)
            sentence (str): 原始输入句子
            
        Returns:
            Dict 包含以下键:
            - sentence: 原始句子
            - mods: 字典，存储所有识别的修饰语
                    键为语义角色名称 (time, location, manner等)
                    值为对应的文本
            - predicate: 谓词/动词
            - subject: 主语/施事者 (None如果不存在)
            - object: 宾语/受事者 (None如果不存在)
            - raw: 模型的原始输出文本
            
        示例:
            >>> response = '{time="每天"} 跑步(小明, null)'
            >>> parsed = agent._parse_triplet_response(response, "小明每天跑步。")
            >>> parsed['mods']  # {'time': '每天'}
            >>> parsed['predicate']  # '跑步'
            >>> parsed['subject']  # '小明'
            >>> parsed['object']  # None
        """
        result = {
            'sentence': sentence,
            'mods': {},        # 修饰语字典
            'predicate': None, # 谓词
            'subject': None,   # 主语
            'object': None,    # 宾语
            'raw': response.strip()
        }
        
        # ========== 第一步: 提取修饰语部分 {key="value", ...} ==========
        # 正则表达式: \{([^}]*)\}
        # 含义: 匹配花括号内的所有内容（非贪心）
        mods_pattern = r'\{([^}]*)\}'
        mods_match = re.search(mods_pattern, response)
        
        if mods_match:
            mods_str = mods_match.group(1)
            # 从字符串中提取所有 key="value" 对
            # 正则表达式: (\w+)="([^"]*)"
            # 含义: 捕获单词字符(键) 和 引号内的内容(值)
            mod_pairs = re.findall(r'(\w+)="([^"]*)"', mods_str)
            for key, value in mod_pairs:
                result['mods'][key] = value
        
        # ========== 第二步: 提取谓词和论元部分 Predicate(Subject, Object) ==========
        # 正则表达式: (\w+)\(([^,]*),\s*([^)]*)\)
        # 含义:
        #   (\w+) - 捕获谓词（一个或多个单词字符）
        #   \( - 左括号
        #   ([^,]*) - 捕获逗号前的所有内容（主语）
        #   , - 逗号
        #   \s* - 零个或多个空白字符
        #   ([^)]*) - 捕获右括号前的所有内容（宾语）
        #   \) - 右括号
        pred_pattern = r'(\w+)\(([^,]*),\s*([^)]*)\)'
        pred_match = re.search(pred_pattern, response)
        
        if pred_match:
            result['predicate'] = pred_match.group(1)
            
            # 清理主语：去除首尾空白，检查是否为"null"
            subject = pred_match.group(2).strip()
            result['subject'] = subject if subject and subject.lower() != 'null' else None
            
            # 清理宾语：同上
            obj = pred_match.group(3).strip()
            result['object'] = obj if obj and obj.lower() != 'null' else None
        
        return result
    
    def _format_triplet(self, triplet: Dict) -> str:
        """
        格式化三元组为标准字符串表示
        
        将三元组字典转换为标准格式: {mods} Predicate(Subject, Object)
        
        Args:
            triplet (Dict): 三元组字典，包含:
                - mods: 修饰语字典
                - predicate: 谓词
                - subject: 主语
                - object: 宾语
                
        Returns:
            str: 格式化后的三元组字符串
            
        示例:
            >>> triplet = {
            ...     'mods': {'time': '每天', 'location': '公园'},
            ...     'predicate': '跑步',
            ...     'subject': '小明',
            ...     'object': None
            ... }
            >>> agent._format_triplet(triplet)
            '{time="每天", location="公园"} 跑步(小明, null)'
        """
        
        # 格式化修饰语部分：{key1="value1", key2="value2", ...}
        mods_str = ", ".join(
            f'{k}="{v}"' for k, v in triplet.get('mods', {}).items()
        )
        
        # 使用null表示不存在的论元
        subject = triplet.get('subject') or 'null'
        obj = triplet.get('object') or 'null'
        predicate = triplet.get('predicate') or 'Unknown'
        
        # 组合成完整的三元组
        if mods_str:
            return f"{{{mods_str}}} {predicate}({subject}, {obj})"
        else:
            return f"{predicate}({subject}, {obj})"
    
    def format_output(self, triplet: Dict) -> str:
        """
        输出格式化的三元组（公开接口）
        
        这是用户友好的输出方法，用于显示最终的三元组结果。
        
        Args:
            triplet (Dict): 三元组字典
            
        Returns:
            str: 格式化后的三元组字符串
            
        示例:
            >>> result = agent.extract_triplets("她用手机拍照。")
            >>> print(agent.format_output(result['triplet']))
            {tool="用手机"} 拍照(她, null)
        """
        return self._format_triplet(triplet)
    
    def get_extraction_history(self) -> List[Dict]:
        """
        获取完整的抽取历史记录
        
        包含所有的抽取和修订过程，便于分析智能体的工作过程。
        
        Returns:
            List[Dict]: 历史记录列表，每条记录包含:
                - sentence: 原始句子
                - triplet: 该版本的三元组
                - attempt: 第几次尝试
                - feedback: 收到的反馈（如果有）
                
        示例:
            >>> history = agent.get_extraction_history()
            >>> for record in history:
            ...     print(f"第{record['attempt']}轮: {record['sentence']}")
            ...     if 'feedback' in record:
            ...         print(f"反馈: {record['feedback']}")
        """
        return self.extraction_history.copy()
    
    def clear_history(self) -> None:
        """
        清空抽取历史记录
        
        当开始处理新任务或重新初始化时调用。
        """
        self.extraction_history = []
