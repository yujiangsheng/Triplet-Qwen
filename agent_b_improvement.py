"""
智能体B自我改进框架
提供持续的验证规则优化、错误学习和性能提升机制

核心模块:
1. ContinuousImprovement - 主控改进循环
2. ValidationRuleLibrary - 可扩展的验证规则库
3. ErrorAnalyzer - 错误模式识别和分析
4. PerformanceTracker - 性能指标追踪
5. FeedbackOptimizer - 智能反馈优化
"""

import json
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re


class ValidationRuleLibrary:
    """
    验证规则库 - 管理和动态优化验证规则
    
    特点:
    - 16个语义角色的完整覆盖
    - 论元完整性检查
    - 修饰语准确性验证
    - 可扩展的自定义规则
    """
    
    def __init__(self):
        """初始化验证规则库"""
        
        # 核心语义角色定义
        self.semantic_roles = {
            'subject': {'name': 'Subject (ARG0)', 'type': 'core'},
            'object': {'name': 'Object (ARG1)', 'type': 'core'},
            'time': {'name': 'Time (ArgM-TMP)', 'type': 'modifier'},
            'location': {'name': 'Location (ArgM-LOC)', 'type': 'modifier'},
            'manner': {'name': 'Manner (ArgM-MNR)', 'type': 'modifier'},
            'cause': {'name': 'Cause (ArgM-CAU)', 'type': 'modifier'},
            'purpose': {'name': 'Purpose (ArgM-PRP)', 'type': 'modifier'},
            'tool': {'name': 'Tool (ArgM-TLS)', 'type': 'modifier'},
            'direction': {'name': 'Direction (ArgM-DIR)', 'type': 'modifier'},
            'destination': {'name': 'Destination (ArgM-GOL)', 'type': 'modifier'},
            'source': {'name': 'Source (ArgM-SRC)', 'type': 'modifier'},
            'attribute': {'name': 'Attribute (ARG-ATT)', 'type': 'modifier'},
            'modal': {'name': 'Modal (ArgM-MOD)', 'type': 'modifier'},
            'negation': {'name': 'Negation (ArgM-NEG)', 'type': 'modifier'},
            'frequency': {'name': 'Frequency (ArgM-FRQ)', 'type': 'modifier'},
            'degree': {'name': 'Degree (ArgM-EXT)', 'type': 'modifier'},
        }
        
        # 关键词匹配规则
        self.keyword_patterns = {
            'time': [
                '每', '每天', '每月', '每年', '早上', '晚上', '昨天', '今天', '明天',
                '今年', '去年', '明年', '上午', '下午', '夜间', '中午', '时刻', '点钟',
                '周', '月', '年', '日', '小时', '分钟', '秒', '一直', '持续', '过程'
            ],
            'location': [
                '在', '地', '处', '里', '上', '下', '前', '后', '左', '右', '中',
                '北', '南', '东', '西', '内', '外', '间', '边', '旁', '头', '尾',
                '远方', '山上', '公园', '学校', '医院', '办公室', '家', '门口'
            ],
            'manner': [
                '仔细', '快速', '慢慢', '轻轻', '大声', '小声', '好好', '充分',
                '完全', '彻底', '深入', '浅显', '友好', '敌意', '谨慎', '大胆',
                '地', '地', '地', '方式', '态度', '风格'
            ],
            'cause': [
                '由于', '因为', '受', '影响', '导致', '造成', '起因', '根源',
                '原因', '是因为', '所以', '因此', '结果'
            ],
            'purpose': [
                '为了', '以便', '目的', '想要', '打算', '计划', '目标',
                '为', '为了能', '为了能够', '希望', '企图'
            ],
            'tool': [
                '用', '通过', '借助', '利用', '凭', '靠', '工具', '手段',
                '办法', '方法', '渠道', '途径', '介质', '媒介'
            ],
            'direction': [
                '向', '朝', '往', '去', '到', '离', '从', '来自',
                '东', '西', '南', '北', '左', '右', '上', '下', '前', '后'
            ],
            'negation': [
                '不', '没有', '无法', '不能', '不会', '不是', '没', '无',
                '非', '别', '莫', '勿', '绝', '永远不'
            ],
            'modal': [
                '可能', '应该', '必须', '可以', '能', '要', '会', '想',
                '得', '着', '了', '过', '着', '应当', '必然', '势必'
            ],
            'frequency': [
                '每', '经常', '有时', '从不', '很少', '总是', '频繁',
                '常常', '有的时候', '间或', '屡次', '多次', '几次'
            ],
            'degree': [
                '很', '非常', '极其', '特别', '太', '特', '相当', '比较',
                '略', '稍', '微', '有点', '一点', '完全', '绝对', '彻底'
            ],
            'attribute': [
                '高大', '漂亮', '新的', '旧的', '红色', '蓝色', '大的', '小的',
                '美丽', '丑陋', '聪明', '愚蠢', '快速', '缓慢', '真的', '假的'
            ]
        }
        
        # 论元完整性检查规则 (关键改进: 来自Message 9的correction)
        self.argument_integrity_rules = {
            'subject_modifiers': [
                # 对Subject的修饰语应该保留在Subject中，不作为mods
                # 例: "高大的男人" - "高大的"不应作为mods，应在Subject中
                {
                    'pattern': r'(形容词|描述性词汇).*?(名词)',
                    'rule': '对主语的形容词修饰应保留在Subject中',
                    'severity': 'high'
                }
            ],
            'object_modifiers': [
                # 对Object的修饰语应该保留在Object中
                # 例: "一只鸟" - "一只"不应作为mods
                {
                    'pattern': r'(数词|量词).*?(名词)',
                    'rule': '对宾语的修饰符应保留在Object中',
                    'severity': 'high'
                }
            ],
            'modifier_completeness': [
                # 修饰语应该完整，不应简化
                # 例: "在远方的山上" 应该完整提取，不应简化为"在山上"
                {
                    'rule': '修饰语应该包含所有关键信息，不应简化或截断',
                    'severity': 'high'
                }
            ]
        }
        
        # 验证规则权重 (用于反馈优先级)
        self.rule_weights = {
            'structure': 1.0,      # 结构完整性
            'argument_integrity': 1.5,  # 论元完整性 (高优先级)
            'semantic_completeness': 1.2,  # 语义完整性
            'recoverability': 1.1,  # 可恢复性
        }
        
        # 可学习的规则 (会根据错误历史动态调整)
        self.learned_rules = {}
    
    def get_expected_modifiers(self, sentence: str, predicate: str) -> List[str]:
        """
        根据句子和谓词预测期望的修饰语类型
        
        Args:
            sentence: 原始句子
            predicate: 抽取的谓词
            
        Returns:
            期望的修饰语列表
        """
        expected = []
        
        # 扫描句子中的关键词
        for role, keywords in self.keyword_patterns.items():
            for keyword in keywords:
                if keyword in sentence:
                    expected.append(role)
                    break
        
        return list(set(expected))
    
    def check_argument_integrity(self, triplet: Dict) -> Tuple[bool, List[str]]:
        """
        检查论元完整性 (来自Message 9的critical fix)
        
        返回: (is_valid, issues)
        
        关键规则:
        1. Subject应包含所有修饰Subject的词汇
        2. Object应包含所有修饰Object的词汇
        3. 修饰语应完整，不应截断关键信息
        """
        issues = []
        
        subject = triplet.get('subject', '')
        obj = triplet.get('object', '')
        mods = triplet.get('mods', {})
        
        # 规则1: 检查Subject中是否有被错误提取为mods的修饰语
        # 错误例: {attribute="高大的"} 看到(男人, 一只鸟)
        # 正确例: {location="在远方的山上"} 看到(高大的男人, 一只鸟)
        for mod_key, mod_value in mods.items():
            # 检查修饰语是否应该是Subject或Object的一部分
            if mod_key == 'attribute':
                # 属性修饰语应该在Subject/Object中，而非单独提取
                if mod_value and not ('在' in mod_value or '从' in mod_value):
                    issues.append(
                        f"属性修饰'{mod_value}'可能应该保留在Subject/Object中而非作为mods"
                    )
        
        # 规则2: 检查location修饰语的完整性
        if 'location' in mods:
            location = mods['location']
            # 检查是否包含完整的方位信息
            if location and ('的' in location or '上' in location or '中' in location):
                # 完整的位置表达 (如"在远方的山上")
                pass
            elif location and any(x in location for x in ['山', '树', '门', '房', '地']):
                # 检查是否有遗漏的修饰词
                if '在' not in location:
                    issues.append(f"location修饰语'{location}'缺失预置词")
        
        # 规则3: 检查Object是否包含所有必要的量词或修饰词
        if obj:
            # 如果Object是"鸟"，应该看是否有量词如"一只"
            if ('一' not in obj and '这' not in obj and '那' not in obj and 
                any(x in sentence for x in ['一', '这', '那']) if 'sentence' in locals() else False):
                pass  # 允许Object中没有量词
        
        return len(issues) == 0, issues
    
    def validate_with_learned_rules(self, triplet: Dict, sentence: str) -> Dict[str, Any]:
        """
        使用学习到的规则进行验证
        
        包括从历史错误中学习的动态规则
        """
        validation_result = {
            'structure_valid': True,
            'argument_integrity_valid': True,
            'semantic_valid': True,
            'issues': [],
            'suggestions': []
        }
        
        # 检查论元完整性
        integrity_valid, integrity_issues = self.check_argument_integrity(triplet)
        validation_result['argument_integrity_valid'] = integrity_valid
        validation_result['issues'].extend(integrity_issues)
        
        # 检查期望的修饰语
        predicate = triplet.get('predicate', '')
        expected_mods = self.get_expected_modifiers(sentence, predicate)
        actual_mods = list(triplet.get('mods', {}).keys())
        
        missing_mods = set(expected_mods) - set(actual_mods)
        if missing_mods:
            validation_result['issues'].append(
                f"缺失期望的修饰语: {', '.join(missing_mods)}"
            )
        
        return validation_result


class ErrorAnalyzer:
    """
    错误分析器 - 识别和分类验证中的错误模式
    
    功能:
    1. 错误模式识别 (论元完整性、修饰语准确性、语义遗漏等)
    2. 错误频率统计
    3. 错误根本原因分析
    4. 错误优先级排序
    """
    
    def __init__(self):
        """初始化错误分析器"""
        self.error_patterns = defaultdict(int)
        self.error_history = []
        self.error_categories = {
            'argument_integrity': '论元完整性错误',
            'missing_modifier': '缺失修饰语',
            'incorrect_modifier': '修饰语错误',
            'semantic_loss': '语义遗漏',
            'format_error': '格式错误',
            'predicate_error': '谓词识别错误',
        }
    
    def analyze_error(self, sentence: str, triplet: Dict, feedback: str) -> Dict[str, Any]:
        """
        分析单个验证失败的错误
        
        Args:
            sentence: 原始句子
            triplet: 提取的三元组
            feedback: Agent B的反馈
            
        Returns:
            错误分析结果
        """
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'sentence': sentence,
            'triplet': triplet,
            'feedback': feedback,
            'categories': [],
            'root_cause': None,
            'severity': 'medium'
        }
        
        # 分析错误类别
        if '论元' in feedback or 'argument' in feedback.lower():
            error_info['categories'].append('argument_integrity')
            error_info['severity'] = 'high'  # 论元错误是严重的
        
        if '修饰语' in feedback or 'modifier' in feedback.lower():
            error_info['categories'].append('missing_modifier')
        
        if '缺失' in feedback or 'missing' in feedback.lower():
            error_info['categories'].append('semantic_loss')
        
        if '格式' in feedback or 'format' in feedback.lower():
            error_info['categories'].append('format_error')
        
        # 统计错误模式
        for category in error_info['categories']:
            self.error_patterns[category] += 1
        
        # 分析根本原因
        error_info['root_cause'] = self._analyze_root_cause(
            sentence, triplet, feedback
        )
        
        self.error_history.append(error_info)
        return error_info
    
    def _analyze_root_cause(self, sentence: str, triplet: Dict, feedback: str) -> str:
        """
        分析错误的根本原因
        """
        # 如果是关于Subject/Object的错误
        if '主语' in feedback or '宾语' in feedback or 'subject' in feedback.lower():
            return "主要参与者识别不准确"
        
        # 如果是关于修饰语的错误
        if '修饰' in feedback or 'modifier' in feedback.lower():
            return "修饰语提取或分类不准确"
        
        # 如果是关于完整性的错误
        if '完整' in feedback or 'complete' in feedback.lower():
            return "未充分捕获原句的语义信息"
        
        return "多因素组合导致的验证失败"
    
    def get_error_distribution(self) -> Dict[str, int]:
        """获取错误分布统计"""
        return dict(self.error_patterns)
    
    def get_top_errors(self, top_n: int = 5) -> List[Tuple[str, int]]:
        """获取最常见的错误类型"""
        return self.error_patterns.most_common(top_n)
    
    def get_errors_by_category(self, category: str) -> List[Dict]:
        """获取特定类别的所有错误"""
        return [e for e in self.error_history if category in e.get('categories', [])]


class PerformanceTracker:
    """
    性能追踪器 - 监控Agent B的验证性能
    
    指标:
    1. 准确率 (Accuracy): 正确识别有效/无效三元组的比率
    2. 改进有效性 (Improvement Effectiveness): 反馈导致的实际改进率
    3. 平均修订轮数 (Avg Revision Rounds): 达到完美需要的轮数
    4. 检测率 (Detection Rate): 识别错误的能力
    """
    
    def __init__(self, window_size: int = 100):
        """
        初始化性能追踪器
        
        Args:
            window_size: 滑动窗口大小，用于计算趋势
        """
        self.window_size = window_size
        self.validation_results = []
        self.improvement_history = []
        self.daily_stats = defaultdict(lambda: {
            'total': 0,
            'correct': 0,
            'improved': 0,
            'failed': 0
        })
    
    def record_validation(
        self,
        is_valid: bool,
        sentence: str,
        triplet: Dict,
        feedback: str = None
    ) -> None:
        """记录验证结果"""
        
        today = datetime.now().date().isoformat()
        self.daily_stats[today]['total'] += 1
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'date': today,
            'is_valid': is_valid,
            'sentence': sentence,
            'triplet': triplet,
            'feedback': feedback
        }
        
        if is_valid:
            self.daily_stats[today]['correct'] += 1
        else:
            self.daily_stats[today]['failed'] += 1
        
        self.validation_results.append(result)
    
    def record_improvement(
        self,
        sentence: str,
        original_triplet: Dict,
        revised_triplet: Dict,
        improvement_rounds: int,
        was_successful: bool
    ) -> None:
        """记录改进结果"""
        
        today = datetime.now().date().isoformat()
        self.daily_stats[today]['improved'] += 1 if was_successful else 0
        
        improvement_record = {
            'timestamp': datetime.now().isoformat(),
            'sentence': sentence,
            'original_triplet': original_triplet,
            'revised_triplet': revised_triplet,
            'rounds': improvement_rounds,
            'successful': was_successful
        }
        
        self.improvement_history.append(improvement_record)
    
    def get_accuracy(self) -> float:
        """
        获取验证准确率
        
        Returns:
            0-1之间的准确率
        """
        if not self.validation_results:
            return 0.0
        
        # 使用滑动窗口计算最近的准确率
        recent = self.validation_results[-self.window_size:]
        correct = sum(1 for r in recent if r['is_valid'])
        return correct / len(recent)
    
    def get_improvement_effectiveness(self) -> float:
        """
        获取改进有效性
        
        Returns:
            成功改进的比率
        """
        if not self.improvement_history:
            return 0.0
        
        successful = sum(1 for r in self.improvement_history if r['successful'])
        return successful / len(self.improvement_history)
    
    def get_average_revision_rounds(self) -> float:
        """获取平均修订轮数"""
        if not self.improvement_history:
            return 0.0
        
        total_rounds = sum(r['rounds'] for r in self.improvement_history)
        return total_rounds / len(self.improvement_history)
    
    def get_detection_rate(self, category: str = None) -> float:
        """
        获取错误检测率
        
        Args:
            category: 特定类别的检测率，如'missing_modifier'
            
        Returns:
            检测率 (0-1)
        """
        if not self.validation_results:
            return 0.0
        
        invalid_count = sum(1 for r in self.validation_results if not r['is_valid'])
        return invalid_count / len(self.validation_results)
    
    def get_daily_report(self, date: str = None) -> Dict[str, Any]:
        """
        获取日报告
        
        Args:
            date: ISO格式日期，如'2025-01-01'，None表示今天
        """
        if date is None:
            date = datetime.now().date().isoformat()
        
        stats = self.daily_stats.get(date, {
            'total': 0, 'correct': 0, 'improved': 0, 'failed': 0
        })
        
        return {
            'date': date,
            'total_validations': stats['total'],
            'correct_validations': stats['correct'],
            'failed_validations': stats['failed'],
            'successful_improvements': stats['improved'],
            'accuracy': stats['correct'] / stats['total'] if stats['total'] > 0 else 0.0
        }
    
    def get_trend_analysis(self, days: int = 7) -> Dict[str, Any]:
        """
        获取趋势分析 (最近N天)
        
        Args:
            days: 分析的天数
            
        Returns:
            趋势数据和建议
        """
        if not self.daily_stats:
            return {'trend': 'insufficient_data'}
        
        recent_days = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).date().isoformat()
            if date in self.daily_stats:
                recent_days.append(date)
        
        if not recent_days:
            return {'trend': 'no_data'}
        
        recent_days = sorted(recent_days)
        accuracies = [
            self.daily_stats[date]['correct'] / self.daily_stats[date]['total']
            if self.daily_stats[date]['total'] > 0 else 0
            for date in recent_days
        ]
        
        # 判断趋势
        if len(accuracies) >= 2:
            trend = 'improving' if accuracies[-1] > accuracies[0] else 'declining'
        else:
            trend = 'unknown'
        
        return {
            'trend': trend,
            'recent_accuracies': dict(zip(recent_days, accuracies)),
            'average_accuracy': sum(accuracies) / len(accuracies),
            'highest_accuracy': max(accuracies),
            'lowest_accuracy': min(accuracies)
        }


class FeedbackOptimizer:
    """
    反馈优化器 - 根据历史学习优化反馈生成
    
    功能:
    1. 自适应反馈生成 (基于错误历史调整反馈)
    2. 反馈有效性评估
    3. 优化反馈措辞
    4. 针对性建议生成
    """
    
    def __init__(self):
        """初始化反馈优化器"""
        self.feedback_templates = {
            'argument_integrity': {
                'issue': '论元完整性问题',
                'suggestions': [
                    '确保Subject包含所有修饰Subject的词汇（如形容词）',
                    '确保Object包含所有修饰Object的词汇（如量词）',
                    '不要将Subject/Object的属性提取为单独的修饰语'
                ]
            },
            'missing_modifier': {
                'issue': '缺失重要修饰语',
                'suggestions': [
                    '检查句子中的时间信息（如"每天"、"昨天"）',
                    '检查句子中的地点信息（如"在..."）',
                    '检查句子中的方式信息（如"仔细"、"快速"）',
                    '检查句子中的原因（如"因为"、"由于"）',
                    '检查句子中的目的（如"为了"）'
                ]
            },
            'semantic_loss': {
                'issue': '语义信息遗漏',
                'suggestions': [
                    '确保修饰语完整，不应截断关键信息',
                    '检查是否有复合修饰语（如"在...的..."）',
                    '验证能否从三元组恢复原句的完整含义'
                ]
            },
            'format_error': {
                'issue': '三元组格式错误',
                'suggestions': [
                    '使用正确的格式: {key1="value1", ...} Predicate(Subject, Object)',
                    '确保所有修饰语都在mods字典中',
                    '检查JSON格式的正确性'
                ]
            }
        }
        
        # 反馈有效性记录
        self.feedback_effectiveness = defaultdict(list)
    
    def generate_adaptive_feedback(
        self,
        issues: List[str],
        error_history: List[Dict],
        rule_library: ValidationRuleLibrary
    ) -> Dict[str, Any]:
        """
        生成自适应反馈
        
        Args:
            issues: 检测到的问题列表
            error_history: 错误历史
            rule_library: 验证规则库
            
        Returns:
            优化的反馈
        """
        feedback = {
            'primary_issues': issues,
            'suggestions': [],
            'priority': 'high' if len(issues) > 2 else 'medium',
            'confidence': 0.8
        }
        
        # 根据历史错误生成针对性建议
        if error_history:
            most_common_error = self._get_most_common_error(error_history)
            if most_common_error:
                template = self.feedback_templates.get(most_common_error, {})
                feedback['suggestions'].extend(
                    template.get('suggestions', [])
                )
        
        # 添加通用建议
        for issue in issues:
            for key, template in self.feedback_templates.items():
                if key in issue.lower():
                    feedback['suggestions'].extend(
                        template.get('suggestions', [])
                    )
        
        return feedback
    
    def _get_most_common_error(self, error_history: List[Dict]) -> Optional[str]:
        """获取最常见的错误类型"""
        if not error_history:
            return None
        
        error_counts = Counter()
        for error in error_history[-20:]:  # 查看最近20个错误
            for category in error.get('categories', []):
                error_counts[category] += 1
        
        if error_counts:
            return error_counts.most_common(1)[0][0]
        
        return None
    
    def evaluate_feedback_effectiveness(
        self,
        feedback: str,
        was_improvement_successful: bool
    ) -> float:
        """
        评估反馈的有效性 (0-1)
        
        如果反馈导致了成功的改进，则有效性高
        """
        effectiveness = 0.8 if was_improvement_successful else 0.3
        self.feedback_effectiveness[feedback].append(effectiveness)
        return effectiveness


class ContinuousImprovement:
    """
    Agent B自我改进的主控类
    
    工作流程:
    1. 每天收集验证数据
    2. 分析错误模式
    3. 更新验证规则
    4. 优化反馈策略
    5. 生成改进报告
    """
    
    def __init__(self):
        """初始化持续改进系统"""
        self.rule_library = ValidationRuleLibrary()
        self.error_analyzer = ErrorAnalyzer()
        self.performance_tracker = PerformanceTracker()
        self.feedback_optimizer = FeedbackOptimizer()
        
        # 优化周期
        self.optimization_cycle = {
            'collect': 'daily',
            'optimize': 'weekly',
            'evaluate': 'weekly',
            'deploy': 'weekly'
        }
        
        # 改进历史
        self.improvement_log = []
    
    def record_validation_cycle(
        self,
        sentence: str,
        original_triplet: Dict,
        validation_result: Dict
    ) -> None:
        """
        记录一个完整的验证周期
        
        Args:
            sentence: 原始句子
            original_triplet: 原始三元组
            validation_result: 验证结果
        """
        # 记录到性能追踪器
        self.performance_tracker.record_validation(
            is_valid=validation_result.get('is_valid', False),
            sentence=sentence,
            triplet=original_triplet,
            feedback=validation_result.get('feedback')
        )
        
        # 如果验证失败，分析错误
        if not validation_result.get('is_valid'):
            error_info = self.error_analyzer.analyze_error(
                sentence=sentence,
                triplet=original_triplet,
                feedback=validation_result.get('feedback', '')
            )
            
            # 生成自适应反馈
            adaptive_feedback = self.feedback_optimizer.generate_adaptive_feedback(
                issues=error_info.get('categories', []),
                error_history=self.error_analyzer.error_history,
                rule_library=self.rule_library
            )
    
    def record_improvement_result(
        self,
        sentence: str,
        original_triplet: Dict,
        revised_triplet: Dict,
        improvement_rounds: int,
        was_successful: bool
    ) -> None:
        """
        记录改进结果
        """
        self.performance_tracker.record_improvement(
            sentence=sentence,
            original_triplet=original_triplet,
            revised_triplet=revised_triplet,
            improvement_rounds=improvement_rounds,
            was_successful=was_successful
        )
    
    def generate_daily_report(self) -> Dict[str, Any]:
        """生成每日改进报告"""
        
        return {
            'timestamp': datetime.now().isoformat(),
            'daily_stats': self.performance_tracker.get_daily_report(),
            'accuracy': self.performance_tracker.get_accuracy(),
            'improvement_effectiveness': self.performance_tracker.get_improvement_effectiveness(),
            'average_revision_rounds': self.performance_tracker.get_average_revision_rounds(),
            'detection_rate': self.performance_tracker.get_detection_rate(),
            'top_errors': self.error_analyzer.get_top_errors(5),
            'error_distribution': self.error_analyzer.get_error_distribution()
        }
    
    def generate_weekly_report(self) -> Dict[str, Any]:
        """生成每周改进报告"""
        
        trend = self.performance_tracker.get_trend_analysis(days=7)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'period': 'weekly',
            'trend_analysis': trend,
            'accuracy_trend': trend.get('average_accuracy'),
            'most_common_errors': self.error_analyzer.get_top_errors(10),
            'recommendations': self._generate_recommendations(trend)
        }
    
    def _generate_recommendations(self, trend: Dict) -> List[str]:
        """根据趋势生成改进建议"""
        
        recommendations = []
        
        if trend.get('trend') == 'declining':
            recommendations.append(
                "准确率下降，需要审视验证规则库中的阈值"
            )
        
        if trend.get('trend') == 'improving':
            recommendations.append(
                "准确率上升，当前改进策略有效"
            )
        
        top_errors = self.error_analyzer.get_top_errors(3)
        if top_errors:
            errors = ', '.join(err[0] for err in top_errors)
            recommendations.append(
                f"重点关注最常见错误: {errors}"
            )
        
        accuracy = trend.get('average_accuracy', 0)
        if accuracy < 0.80:
            recommendations.append(
                "准确率低于80%，建议增强验证规则"
            )
        elif accuracy < 0.90:
            recommendations.append(
                "准确率在80-90%，目标是突破90%"
            )
        else:
            recommendations.append(
                "准确率优良，维持当前标准"
            )
        
        return recommendations
    
    def export_improvement_data(self, filepath: str) -> None:
        """
        导出改进数据用于分析
        
        Args:
            filepath: 导出文件路径
        """
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'error_history': self.error_analyzer.error_history,
            'validation_results': self.performance_tracker.validation_results,
            'improvement_history': self.performance_tracker.improvement_history,
            'daily_stats': dict(self.performance_tracker.daily_stats)
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    def get_improvement_status(self) -> Dict[str, Any]:
        """获取改进系统的当前状态"""
        
        return {
            'rule_library_size': len(self.rule_library.semantic_roles),
            'error_patterns_tracked': len(self.error_analyzer.error_patterns),
            'validation_count': len(self.performance_tracker.validation_results),
            'improvement_count': len(self.performance_tracker.improvement_history),
            'current_accuracy': self.performance_tracker.get_accuracy(),
            'improvement_effectiveness': self.performance_tracker.get_improvement_effectiveness(),
            'average_revision_rounds': self.performance_tracker.get_average_revision_rounds()
        }
