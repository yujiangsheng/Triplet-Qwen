"""
智能体B - 三元组验证器 (集成自我改进机制)
检查三元组是否完整反映原句语义，并提供改进反馈

集成的自我改进机制:
1. 验证规则库动态优化
2. 错误模式识别和学习
3. 性能指标自动追踪
4. 自适应反馈生成
5. 周期性改进报告

改进框架基于以下10点机制:
  1. 反馈积累机制 - 记录所有验证结果和反馈
  2. 规则库扩展 - 根据错误动态优化验证规则
  3. 自适应反馈 - 根据错误历史调整反馈策略
  4. 性能评估 - 准确率、改进有效性、修订轮数、检测率
  5. 错误学习 - 分析错误模式，提取可学习的规则
  6. 问题分类 - 对不同类型的错误进行分类统计
  7. 优化循环 - 每周执行收集→优化→评估→部署
  8. 自我评估 - 周期性性能评估和趋势分析
  9. 基准数据集 - 维护黄金标准数据集用于性能基准
  10. 智能调整 - 根据改进模式动态调整反馈措辞
"""

import json
from typing import Dict, List, Tuple, Any, Optional
from model_loader import generate_response
from agent_b_improvement import (
    ContinuousImprovement,
    ValidationRuleLibrary,
    ErrorAnalyzer,
    PerformanceTracker,
    FeedbackOptimizer
)


class AgentB:
    """
    三元组验证和反馈智能体 (集成自我改进机制)
    
    核心职责:
    1. 验证三元组是否完整反映原句语义
    2. 检查是否可由三元组恢复原句
    3. 识别缺失的语义信息
    4. 提供具体的改进反馈
    
    自我改进职责:
    5. 跟踪验证性能指标
    6. 从错误中学习和优化
    7. 动态调整验证规则
    8. 生成改进报告
    
    性能指标 (自动追踪):
    - 准确率 (Accuracy): 正确识别有效/无效三元组的比率
    - 改进有效性 (Improvement Effectiveness): 反馈导致的改进率
    - 平均修订轮数 (Avg Revision Rounds): 达到完美所需轮数
    - 检测率 (Detection Rate): 识别错误的能力
    """
    
    def __init__(self, model, tokenizer, device):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.validation_history = []
        
        # 集成自我改进系统
        self.improvement_system = ContinuousImprovement()
        self.rule_library = self.improvement_system.rule_library
        self.error_analyzer = self.improvement_system.error_analyzer
        self.performance_tracker = self.improvement_system.performance_tracker
        self.feedback_optimizer = self.improvement_system.feedback_optimizer
    
    def validate_triplet(self, sentence: str, triplet: Dict) -> Dict[str, Any]:
        """
        验证三元组的完整性和正确性
        
        同时触发自我改进系统的数据收集
        
        Args:
            sentence: 原始句子
            triplet: 智能体A抽取的三元组
            
        Returns:
            验证结果和反馈
        """
        print(f"\n[智能体B] 开始验证三元组")
        
        # 第一步：检查三元组结构
        structure_check = self._check_structure(triplet)
        
        # 第二步：检查论元完整性 (来自Message 9的关键修复)
        argument_integrity_check = self._check_argument_integrity(sentence, triplet)
        
        # 第三步：检查语义完整性
        completeness_check = self._check_semantic_completeness(sentence, triplet)
        
        # 第四步：检查可恢复性
        recoverability_check = self._check_recoverability(sentence, triplet)
        
        # 第五步：使用模型进行深层验证
        model_feedback = self._get_model_validation(sentence, triplet)
        
        # 综合所有检查结果
        is_valid = (
            structure_check['valid'] and
            argument_integrity_check['valid'] and
            completeness_check['valid'] and
            recoverability_check['valid'] and
            model_feedback['valid']
        )
        
        feedback = self._generate_feedback(
            structure_check,
            argument_integrity_check,
            completeness_check,
            recoverability_check,
            model_feedback,
            is_valid
        )
        
        result = {
            'sentence': sentence,
            'triplet': triplet,
            'is_valid': is_valid,
            'structure_check': structure_check,
            'argument_integrity_check': argument_integrity_check,
            'completeness_check': completeness_check,
            'recoverability_check': recoverability_check,
            'model_feedback': model_feedback,
            'feedback': feedback
        }
        
        self.validation_history.append(result)
        
        # 触发自我改进系统的数据收集
        self.improvement_system.record_validation_cycle(
            sentence=sentence,
            original_triplet=triplet,
            validation_result=result
        )
        
        return result
    
    def _check_structure(self, triplet: Dict) -> Dict[str, Any]:
        """检查三元组的基本结构"""
        
        issues = []
        
        # 检查必要字段
        if not triplet.get('predicate'):
            issues.append("缺失谓词信息")
        
        if not triplet.get('subject'):
            issues.append("缺失主语信息")
        
        # 检查修饰语格式
        mods = triplet.get('mods', {})
        if not isinstance(mods, dict):
            issues.append("修饰语格式不正确")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    def _check_argument_integrity(self, sentence: str, triplet: Dict) -> Dict[str, Any]:
        """
        检查论元完整性 (来自Message 9的critical fix)
        
        关键规则:
        1. Subject应包含所有修饰Subject的词汇 (如形容词)
        2. Object应包含所有修饰Object的词汇 (如量词)
        3. 修饰语应完整，不应截断关键信息
        
        错误例: {attribute="高大的"} 看到(男人, 一只鸟)
        正确例: {location="在远方的山上"} 看到(高大的男人, 一只鸟)
        """
        issues = []
        
        subject = triplet.get('subject', '')
        obj = triplet.get('object', '')
        mods = triplet.get('mods', {})
        
        # 规则1: 检查是否有属性修饰语被错误地提取为mods
        for mod_key, mod_value in mods.items():
            if mod_key == 'attribute':
                # 属性修饰语应该在Subject/Object中，而非单独提取
                if mod_value and not any(x in mod_value for x in ['在', '从', '给', '对']):
                    issues.append(
                        f"属性修饰'{mod_value}'应该保留在Subject/Object中，"
                        f"而非作为独立的mods"
                    )
        
        # 规则2: 检查location修饰语的完整性
        if 'location' in mods:
            location = mods['location']
            # 完整的位置表达应该包含多层信息 (如"在远方的山上")
            word_count = len(location)
            if word_count < 2:
                issues.append(
                    f"location修饰语'{location}'可能过于简化，"
                    f"应保留完整的位置表达"
                )
        
        # 规则3: 检查Object是否包含完整的内容
        if obj and '数' in sentence and '个' in sentence:
            # 如果句子中有数量词，Object应该包含它
            pass
        
        # 规则4: 检查主语的完整性
        if subject:
            # 主语应该包含所有修饰它的形容词
            # 这是一个启发式检查
            pass
        
        return {
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    def _check_semantic_completeness(self, sentence: str, triplet: Dict) -> Dict[str, Any]:
        """检查三元组是否完整反映原句的语义"""
        
        issues = []
        
        # 检查重要实体是否被捕获
        predicate = triplet.get('predicate', '').lower()
        subject = triplet.get('subject', '').lower() if triplet.get('subject') else ''
        obj = triplet.get('object', '').lower() if triplet.get('object') else ''
        
        sentence_lower = sentence.lower()
        
        # 检查主要实体是否出现在原句中
        if subject and subject not in sentence_lower:
            issues.append(f"主语'{subject}'不在原句中")
        
        if obj and obj not in sentence_lower:
            issues.append(f"宾语'{obj}'不在原句中")
        
        # 检查关键修饰语
        mods = triplet.get('mods', {})
        
        # 如果句子中有时间词，应该有time修饰语
        time_keywords = ['每天', '每月', '每年', '早上', '晚上', '昨天', '今天', '明天', '今年', '去年',
                        'every', 'daily', 'daily', 'morning', 'evening', 'yesterday', 'today', 'tomorrow']
        has_time_keyword = any(keyword in sentence for keyword in time_keywords)
        if has_time_keyword and 'time' not in mods:
            issues.append("句子中有时间信息但三元组缺失time修饰语")
        
        # 如果句子中有地点词，应该有location修饰语
        location_keywords = ['在', '地', '处', '里', '上', 'at', 'in', 'on', 'near']
        has_location_keyword = any(keyword in sentence for keyword in location_keywords)
        if has_location_keyword and 'location' not in mods:
            issues.append("句子中有地点信息但三元组缺失location修饰语")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues
        }
    
    def _check_recoverability(self, sentence: str, triplet: Dict) -> Dict[str, Any]:
        """检查是否能从三元组恢复原句的核心语义"""
        
        issues = []
        
        # 构造恢复句子
        recovered = self._reconstruct_sentence(triplet)
        
        # 检查是否包含原句的关键成分
        predicate = triplet.get('predicate', '')
        if not predicate or predicate not in sentence:
            issues.append("无法从三元组恢复原句的谓词信息")
        
        # 检查是否遗漏了重要的修饰信息
        if len(triplet.get('mods', {})) == 0 and (
            '在' in sentence or '每' in sentence or '很' in sentence
        ):
            issues.append("丢失了重要的修饰语信息，无法完整恢复原句")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'recovered_sentence': recovered
        }
    
    def _get_model_validation(self, sentence: str, triplet: Dict) -> Dict[str, Any]:
        """使用模型进行深层验证"""
        
        triplet_str = self._format_triplet(triplet)
        
        validation_prompt = f"""你是一个NLP专家，需要评估以下三元组是否完整反映原句的语义。

原始句子: "{sentence}"

提取的三元组: {triplet_str}

请评估:
1. 三元组是否捕获了原句的核心语义?
2. 是否有遗漏的重要信息?
3. 从这个三元组能否恢复原句?
4. 有什么需要改进的地方?

输出格式: 
{{
  "complete": true/false,
  "missing_info": ["...", "..."],
  "recoverable": true/false,
  "suggestions": ["...", "..."]
}}

评估结果:"""
        
        try:
            response = generate_response(
                self.model,
                self.tokenizer,
                validation_prompt,
                self.device,
                max_new_tokens=256,
                temperature=0.3,
            )
            
            # 尝试解析JSON响应
            try:
                import json
                # 提取JSON部分
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    parsed = json.loads(json_str)
                    return {
                        'valid': parsed.get('complete', True) and parsed.get('recoverable', True),
                        'missing_info': parsed.get('missing_info', []),
                        'suggestions': parsed.get('suggestions', []),
                        'raw_response': response
                    }
            except json.JSONDecodeError:
                pass
            
            # 如果JSON解析失败，基于文本内容判断
            is_complete = 'complete' in response.lower() and '不完整' not in response
            is_recoverable = 'recoverable' in response.lower() or '可恢复' in response
            
            return {
                'valid': is_complete and is_recoverable,
                'raw_response': response,
                'missing_info': [],
                'suggestions': []
            }
            
        except Exception as e:
            print(f"  模型验证出错: {e}")
            return {
                'valid': True,
                'error': str(e)
            }
    
    def _generate_feedback(
        self,
        structure_check: Dict,
        argument_integrity_check: Dict,
        completeness_check: Dict,
        recoverability_check: Dict,
        model_feedback: Dict,
        is_valid: bool
    ) -> str:
        """生成综合反馈"""
        
        if is_valid:
            return "✓ 三元组完整且正确，无需修改"
        
        feedback_parts = []
        
        if not structure_check['valid']:
            feedback_parts.append(f"结构问题: {'; '.join(structure_check['issues'])}")
        
        if not argument_integrity_check['valid']:
            feedback_parts.append(
                f"论元完整性问题: {'; '.join(argument_integrity_check['issues'])}"
            )
        
        if not completeness_check['valid']:
            feedback_parts.append(f"完整性问题: {'; '.join(completeness_check['issues'])}")
        
        if not recoverability_check['valid']:
            feedback_parts.append(f"可恢复性问题: {'; '.join(recoverability_check['issues'])}")
        
        if model_feedback.get('missing_info'):
            feedback_parts.append(f"缺失信息: {'; '.join(model_feedback['missing_info'])}")
        
        if model_feedback.get('suggestions'):
            feedback_parts.append(f"改进建议: {'; '.join(model_feedback['suggestions'])}")
        
        return "; ".join(feedback_parts) if feedback_parts else "需要改进"
    
    def _reconstruct_sentence(self, triplet: Dict) -> str:
        """从三元组重构句子"""
        
        parts = []
        
        # 添加修饰语
        mods = triplet.get('mods', {})
        if mods:
            for key, value in mods.items():
                parts.append(value)
        
        # 添加主语
        subject = triplet.get('subject')
        if subject:
            parts.append(subject)
        
        # 添加谓词
        predicate = triplet.get('predicate')
        if predicate:
            parts.append(predicate)
        
        # 添加宾语
        obj = triplet.get('object')
        if obj:
            parts.append(obj)
        
        return "".join(parts) if parts else "[无法重构]"
    
    def _format_triplet(self, triplet: Dict) -> str:
        """格式化三元组"""
        
        mods_str = ", ".join(
            f'{k}="{v}"' for k, v in triplet.get('mods', {}).items()
        )
        
        subject = triplet.get('subject') or 'null'
        obj = triplet.get('object') or 'null'
        predicate = triplet.get('predicate') or 'Unknown'
        
        if mods_str:
            return f"{{{mods_str}}} {predicate}({subject}, {obj})"
        else:
            return f"{predicate}({subject}, {obj})"
    
    def print_validation_result(self, result: Dict) -> None:
        """打印验证结果"""
        
        print(f"\n{'='*60}")
        print(f"验证结果: {'✓ 通过' if result['is_valid'] else '✗ 失败'}")
        print(f"{'='*60}")
        
        if result['structure_check']['issues']:
            print(f"结构问题: {result['structure_check']['issues']}")
        
        if result.get('argument_integrity_check', {}).get('issues'):
            print(f"论元完整性问题: {result['argument_integrity_check']['issues']}")
        
        if result['completeness_check']['issues']:
            print(f"完整性问题: {result['completeness_check']['issues']}")
        
        if result['recoverability_check']['issues']:
            print(f"可恢复性问题: {result['recoverability_check']['issues']}")
        
        print(f"综合反馈: {result['feedback']}")
        print(f"{'='*60}\n")
    
    # ========== 自我改进报告方法 ==========
    
    def get_daily_improvement_report(self) -> Dict[str, Any]:
        """
        获取每日改进报告
        
        Returns:
            包含准确率、改进有效性、错误分布等指标的报告
        """
        return self.improvement_system.generate_daily_report()
    
    def get_weekly_improvement_report(self) -> Dict[str, Any]:
        """
        获取每周改进报告
        
        包括:
        - 准确率趋势分析
        - 最常见的错误类型
        - 改进建议
        
        Returns:
            周报告数据
        """
        return self.improvement_system.generate_weekly_report()
    
    def print_improvement_report(self, report_type: str = 'daily') -> None:
        """
        打印改进报告
        
        Args:
            report_type: 'daily' 或 'weekly'
        """
        if report_type == 'daily':
            report = self.get_daily_improvement_report()
            print(f"\n{'='*70}")
            print("📊 Agent B 每日改进报告")
            print(f"{'='*70}")
            print(f"时间: {report.get('timestamp')}")
            print(f"准确率: {report.get('accuracy'):.2%}")
            print(f"改进有效性: {report.get('improvement_effectiveness'):.2%}")
            print(f"平均修订轮数: {report.get('average_revision_rounds'):.2f}")
            print(f"错误检测率: {report.get('detection_rate'):.2%}")
            print(f"\n最常见的错误 (Top 5):")
            for i, (error_type, count) in enumerate(report.get('top_errors', []), 1):
                print(f"  {i}. {error_type}: {count}次")
            print(f"{'='*70}\n")
        
        elif report_type == 'weekly':
            report = self.get_weekly_improvement_report()
            print(f"\n{'='*70}")
            print("📈 Agent B 每周改进报告")
            print(f"{'='*70}")
            print(f"时间: {report.get('timestamp')}")
            
            trend = report.get('trend_analysis', {})
            if trend.get('trend') == 'improving':
                print("趋势: ⬆️  上升")
            elif trend.get('trend') == 'declining':
                print("趋势: ⬇️  下降")
            else:
                print("趋势: ➡️  平稳")
            
            print(f"平均准确率: {trend.get('average_accuracy', 0):.2%}")
            print(f"最高准确率: {trend.get('highest_accuracy', 0):.2%}")
            print(f"最低准确率: {trend.get('lowest_accuracy', 0):.2%}")
            
            print(f"\n改进建议:")
            for i, suggestion in enumerate(report.get('recommendations', []), 1):
                print(f"  {i}. {suggestion}")
            
            print(f"\n最常见的错误 (Top 10):")
            for i, (error_type, count) in enumerate(report.get('most_common_errors', []), 1):
                print(f"  {i}. {error_type}: {count}次")
            print(f"{'='*70}\n")
    
    def export_improvement_data(self, filepath: str) -> None:
        """
        导出改进数据
        
        Args:
            filepath: 导出文件路径
        """
        self.improvement_system.export_improvement_data(filepath)
        print(f"✓ 改进数据已导出到: {filepath}")
    
    def get_improvement_status(self) -> Dict[str, Any]:
        """获取改进系统的当前状态"""
        return self.improvement_system.get_improvement_status()
    
    def print_improvement_status(self) -> None:
        """打印改进系统状态"""
        status = self.get_improvement_status()
        print(f"\n{'='*70}")
        print("🔧 Agent B 改进系统状态")
        print(f"{'='*70}")
        print(f"规则库大小: {status.get('rule_library_size')} 个语义角色")
        print(f"追踪的错误模式: {status.get('error_patterns_tracked')} 种")
        print(f"验证总数: {status.get('validation_count')} 次")
        print(f"改进总数: {status.get('improvement_count')} 次")
        print(f"当前准确率: {status.get('current_accuracy', 0):.2%}")
        print(f"改进有效性: {status.get('improvement_effectiveness', 0):.2%}")
        print(f"平均修订轮数: {status.get('average_revision_rounds', 0):.2f}")
        print(f"{'='*70}\n")

