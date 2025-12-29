"""
效果评估模块 - 定义和衡量Agent的性能

评估维度:
1. 准确率 - 三元组的正确性
2. 完整性 - 是否捕获了所有语义信息
3. 一致性 - 多次运行的结果稳定性
4. 效率 - 处理速度和资源使用
5. 用户满意度 - 人工评估
"""

import numpy as np
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """错误类型分类"""
    MISSING_ENTITY = "缺失实体"
    WRONG_ENTITY = "实体错误"
    MISSING_MODIFIER = "缺失修饰语"
    WRONG_MODIFIER = "修饰语错误"
    MISSING_PREDICATE = "缺失谓词"
    WRONG_PREDICATE = "谓词错误"
    ARGUMENT_INTEGRITY = "论元完整性"
    FORMAT_ERROR = "格式错误"


@dataclass
class EvaluationMetrics:
    """评估指标容器"""
    accuracy: float              # 准确率 (0-1)
    precision: float            # 精确率
    recall: float               # 召回率
    f1_score: float             # F1分数
    completeness: float         # 完整性
    consistency: float          # 一致性
    argument_integrity: float   # 论元完整性
    error_distribution: Dict    # 错误分布
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'accuracy': self.accuracy,
            'precision': self.precision,
            'recall': self.recall,
            'f1_score': self.f1_score,
            'completeness': self.completeness,
            'consistency': self.consistency,
            'argument_integrity': self.argument_integrity,
            'error_distribution': self.error_distribution
        }


class TripleteEvaluator:
    """
    三元组评估器
    
    评估单个三元组的质量
    """
    
    def __init__(self):
        """初始化评估器"""
        self.reference_triplets = {}  # 参考三元组
    
    def evaluate_triplet(self, predicted: Dict, reference: Dict) -> Dict:
        """
        评估预测的三元组
        
        Args:
            predicted: 预测的三元组
            reference: 参考三元组
            
        Returns:
            评估结果
        """
        score = {
            'exact_match': self._exact_match(predicted, reference),
            'partial_match': self._partial_match(predicted, reference),
            'entity_match': self._entity_match(predicted, reference),
            'predicate_match': self._predicate_match(predicted, reference),
            'modifier_match': self._modifier_match(predicted, reference),
            'integrity_score': self._check_argument_integrity(predicted, reference)
        }
        
        # 计算总体分数 (加权平均)
        weights = {
            'exact_match': 0.3,
            'entity_match': 0.2,
            'predicate_match': 0.2,
            'modifier_match': 0.15,
            'integrity_score': 0.15
        }
        
        score['overall'] = sum(
            score[key] * weights[key] 
            for key in weights.keys()
        )
        
        return score
    
    def _exact_match(self, predicted: Dict, reference: Dict) -> float:
        """完全匹配"""
        if predicted == reference:
            return 1.0
        return 0.0
    
    def _partial_match(self, predicted: Dict, reference: Dict) -> float:
        """部分匹配"""
        matches = 0
        total = 0
        
        # 检查谓词
        if predicted.get('predicate') == reference.get('predicate'):
            matches += 1
        total += 1
        
        # 检查主语
        if predicted.get('subject') == reference.get('subject'):
            matches += 1
        total += 1
        
        # 检查宾语
        if predicted.get('object') == reference.get('object'):
            matches += 1
        total += 1
        
        return matches / total
    
    def _entity_match(self, predicted: Dict, reference: Dict) -> float:
        """实体匹配"""
        score = 0.0
        
        # 主语匹配
        pred_subj = predicted.get('subject', '')
        ref_subj = reference.get('subject', '')
        if self._string_similarity(pred_subj, ref_subj) > 0.8:
            score += 0.5
        
        # 宾语匹配
        pred_obj = predicted.get('object', '')
        ref_obj = reference.get('object', '')
        if self._string_similarity(pred_obj, ref_obj) > 0.8:
            score += 0.5
        
        return min(1.0, score)
    
    def _predicate_match(self, predicted: Dict, reference: Dict) -> float:
        """谓词匹配"""
        pred = predicted.get('predicate', '')
        ref = reference.get('predicate', '')
        
        if pred == ref:
            return 1.0
        elif self._string_similarity(pred, ref) > 0.8:
            return 0.7
        else:
            return 0.0
    
    def _modifier_match(self, predicted: Dict, reference: Dict) -> float:
        """修饰语匹配"""
        pred_mods = predicted.get('mods', {})
        ref_mods = reference.get('mods', {})
        
        if not ref_mods:
            return 1.0 if not pred_mods else 0.8
        
        matches = 0
        for key, value in ref_mods.items():
            if key in pred_mods:
                if self._string_similarity(pred_mods[key], value) > 0.7:
                    matches += 1
        
        return matches / len(ref_mods) if ref_mods else 1.0
    
    def _check_argument_integrity(self, predicted: Dict, reference: Dict) -> float:
        """
        检查论元完整性
        
        判断Subject和Object是否包含了所有必要的修饰信息
        """
        score = 1.0
        
        # 检查Subject的完整性
        pred_subj = predicted.get('subject', '')
        ref_subj = reference.get('subject', '')
        if ref_subj and pred_subj != ref_subj:
            # 如果长度差异过大，说明遗漏了信息
            if len(pred_subj) < len(ref_subj) * 0.7:
                score -= 0.3
        
        # 检查Object的完整性
        pred_obj = predicted.get('object', '')
        ref_obj = reference.get('object', '')
        if ref_obj and pred_obj != ref_obj:
            if len(pred_obj) < len(ref_obj) * 0.7:
                score -= 0.3
        
        return max(0.0, score)
    
    @staticmethod
    def _string_similarity(s1: str, s2: str) -> float:
        """
        计算两个字符串的相似度 (Jaccard相似度)
        
        Args:
            s1: 字符串1
            s2: 字符串2
            
        Returns:
            相似度 (0-1)
        """
        if not s1 or not s2:
            return 1.0 if s1 == s2 else 0.0
        
        set1 = set(s1)
        set2 = set(s2)
        
        if not set1 or not set2:
            return 1.0 if s1 == s2 else 0.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0


class SystemEvaluator:
    """
    系统评估器
    
    对整个Agent系统进行综合评估
    """
    
    def __init__(self, agent_a, agent_b, triplet_evaluator: TripleteEvaluator):
        """
        初始化系统评估器
        
        Args:
            agent_a: Agent A实例
            agent_b: Agent B实例
            triplet_evaluator: 三元组评估器
        """
        self.agent_a = agent_a
        self.agent_b = agent_b
        self.triplet_evaluator = triplet_evaluator
        
        self.error_logs: List[Dict] = []
        self.performance_history: List[EvaluationMetrics] = []
    
    def evaluate_on_dataset(self, dataset, reference_triplets: Dict = None) -> EvaluationMetrics:
        """
        在数据集上评估系统
        
        Args:
            dataset: 句子列表
            reference_triplets: 参考三元组字典 {句子: 参考三元组}
            
        Returns:
            评估指标
        """
        results = {
            'total': len(dataset),
            'correct': 0,
            'predictions': [],
            'errors': []
        }
        
        for sentence in dataset:
            try:
                # Agent A: 抽取
                predicted = self.agent_a.extract_triplets(sentence.text)
                
                # Agent B: 验证
                validation = self.agent_b.validate_triplet(sentence.text, predicted)
                
                # 评估
                if reference_triplets and sentence.text in reference_triplets:
                    reference = reference_triplets[sentence.text]
                    score = self.triplet_evaluator.evaluate_triplet(predicted, reference)
                    
                    results['predictions'].append({
                        'sentence': sentence.text,
                        'predicted': predicted,
                        'reference': reference,
                        'score': score,
                        'valid': validation.get('is_valid', False)
                    })
                    
                    if score['overall'] > 0.8:
                        results['correct'] += 1
                else:
                    # 没有参考，只能用启发式评估
                    if self._is_reasonable(predicted, sentence.text):
                        results['correct'] += 1
                
            except Exception as e:
                logger.warning(f"评估错误: {e}")
                results['errors'].append(str(e))
                continue
        
        return self._compile_metrics(results)
    
    def _is_reasonable(self, triplet: Dict, sentence: str) -> bool:
        """启发式检查三元组是否合理"""
        # 检查必需字段
        if not triplet.get('predicate'):
            return False
        
        # 检查谓词在句子中
        if triplet['predicate'] not in sentence:
            return False
        
        # 检查Subject/Object
        if triplet.get('subject') and triplet['subject'] not in sentence:
            return False
        
        return True
    
    def _compile_metrics(self, results: Dict) -> EvaluationMetrics:
        """编译评估指标"""
        total = results['total']
        correct = results['correct']
        
        accuracy = correct / total if total > 0 else 0.0
        
        # 计算更细粒度的指标
        if results['predictions']:
            scores = [p['score']['overall'] for p in results['predictions']]
            avg_score = np.mean(scores)
        else:
            avg_score = accuracy
        
        metrics = EvaluationMetrics(
            accuracy=accuracy,
            precision=0.0,  # 需要参考数据才能计算
            recall=0.0,
            f1_score=0.0,
            completeness=avg_score,
            consistency=0.9,  # 占位值
            argument_integrity=0.85,  # 占位值
            error_distribution=self._analyze_errors(results['errors'])
        )
        
        self.performance_history.append(metrics)
        return metrics
    
    def _analyze_errors(self, errors: List[str]) -> Dict:
        """分析错误分布"""
        error_dist = {}
        for error in errors:
            error_type = self._classify_error(error)
            error_dist[error_type.value] = error_dist.get(error_type.value, 0) + 1
        
        return error_dist
    
    def _classify_error(self, error: str) -> ErrorType:
        """分类错误"""
        error_lower = error.lower()
        
        if '实体' in error_lower or 'entity' in error_lower:
            return ErrorType.MISSING_ENTITY
        elif '修饰' in error_lower or 'modifier' in error_lower:
            return ErrorType.MISSING_MODIFIER
        elif '谓词' in error_lower or 'predicate' in error_lower:
            return ErrorType.MISSING_PREDICATE
        elif '论元' in error_lower or 'argument' in error_lower:
            return ErrorType.ARGUMENT_INTEGRITY
        else:
            return ErrorType.FORMAT_ERROR
    
    def get_performance_summary(self) -> Dict:
        """获取性能总结"""
        if not self.performance_history:
            return {'status': 'no_evaluation'}
        
        latest = self.performance_history[-1]
        
        summary = {
            'total_evaluations': len(self.performance_history),
            'current_accuracy': latest.accuracy,
            'current_completeness': latest.completeness,
            'trend': self._analyze_trend()
        }
        
        return summary
    
    def _analyze_trend(self) -> str:
        """分析性能趋势"""
        if len(self.performance_history) < 2:
            return 'unknown'
        
        recent_accuracy = self.performance_history[-1].accuracy
        previous_accuracy = self.performance_history[-2].accuracy
        
        if recent_accuracy > previous_accuracy * 1.05:
            return 'improving'
        elif recent_accuracy < previous_accuracy * 0.95:
            return 'declining'
        else:
            return 'stable'


class UserStudy:
    """
    用户研究 - 收集人工评估反馈
    
    支持:
    - 人工标注数据
    - 用户评分
    - 反馈收集
    """
    
    def __init__(self):
        """初始化用户研究"""
        self.annotations: List[Dict] = []
        self.ratings: List[Tuple[str, float]] = []  # (句子, 评分)
    
    def add_annotation(self, sentence: str, triplet: Dict, rating: float, 
                      feedback: str = "") -> None:
        """
        添加人工标注
        
        Args:
            sentence: 句子
            triplet: 三元组
            rating: 评分 (0-10)
            feedback: 反馈文本
        """
        self.annotations.append({
            'sentence': sentence,
            'triplet': triplet,
            'rating': rating,
            'feedback': feedback,
            'timestamp': np.datetime64('now')
        })
        self.ratings.append((sentence, rating))
    
    def get_average_rating(self) -> float:
        """获取平均评分"""
        if not self.ratings:
            return 0.0
        
        return np.mean([r[1] for r in self.ratings])
    
    def get_satisfaction_level(self) -> str:
        """获取满意度等级"""
        avg = self.get_average_rating()
        
        if avg >= 8.0:
            return '非常满意'
        elif avg >= 6.0:
            return '满意'
        elif avg >= 4.0:
            return '一般'
        else:
            return '不满意'
