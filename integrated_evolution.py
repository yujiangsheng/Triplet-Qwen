"""
集成演化系统 - 连接所有组件的完整系统

流程：
1. 数据爬取 -> 质量过滤
2. 初始评估 -> 性能基线
3. 自动优化 -> 迭代改进
4. 收敛检测 -> 停止条件
5. 结果保存 -> 最佳模型
"""

import logging
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import time

from data_crawler import DataCrawler, DataManager, Sentence
from evolution_system import EvolutionSystem, EvolutionMetrics, AdaptiveOptimizer
from evaluation_metrics import SystemEvaluator, TripleteEvaluator, EvaluationMetrics, UserStudy

logger = logging.getLogger(__name__)


@dataclass
class EvolutionConfig:
    """演化配置"""
    max_iterations: int = 50              # 最大迭代次数
    convergence_threshold: float = 0.02   # 收敛阈值
    target_accuracy: float = 0.85         # 目标准确率
    min_data_size: int = 50               # 最小数据集大小
    validation_ratio: float = 0.2         # 验证集比例
    
    # 数据源配置
    crawl_frequency: int = 5              # 每5轮爬取一次新数据
    quality_threshold: float = 0.7        # 质量阈值
    
    # 优化配置
    use_user_feedback: bool = True        # 使用用户反馈
    optimization_patience: int = 10       # 多少轮无改进后停止
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'max_iterations': self.max_iterations,
            'convergence_threshold': self.convergence_threshold,
            'target_accuracy': self.target_accuracy,
            'min_data_size': self.min_data_size,
            'validation_ratio': self.validation_ratio,
            'crawl_frequency': self.crawl_frequency,
            'quality_threshold': self.quality_threshold,
            'use_user_feedback': self.use_user_feedback,
            'optimization_patience': self.optimization_patience
        }


@dataclass
class EvolutionReport:
    """演化报告"""
    config: EvolutionConfig
    total_iterations: int
    best_metrics: EvaluationMetrics
    best_iteration: int
    convergence_achieved: bool
    metrics_history: List[EvaluationMetrics]
    data_evolution: Dict
    time_elapsed: float
    timestamp: str
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'config': self.config.to_dict(),
            'total_iterations': self.total_iterations,
            'best_metrics': self.best_metrics.to_dict(),
            'best_iteration': self.best_iteration,
            'convergence_achieved': self.convergence_achieved,
            'metrics_history': [m.to_dict() for m in self.metrics_history],
            'data_evolution': self.data_evolution,
            'time_elapsed': self.time_elapsed,
            'timestamp': self.timestamp
        }


class IntegratedEvolutionSystem:
    """
    集成演化系统
    
    协调数据爬取、自动优化、性能评估的完整流程
    """
    
    def __init__(self, agent_a, agent_b, config: EvolutionConfig = None):
        """
        初始化集成演化系统
        
        Args:
            agent_a: Agent A (提取器)
            agent_b: Agent B (验证器)
            config: 演化配置
        """
        self.agent_a = agent_a
        self.agent_b = agent_b
        self.config = config or EvolutionConfig()
        
        # 初始化各子系统
        self.data_crawler = DataCrawler()
        self.data_manager = DataManager()
        self.evolution_system = EvolutionSystem(agent_a, agent_b, self.config)
        
        # 初始化评估系统
        self.triplet_evaluator = TripleteEvaluator()
        self.system_evaluator = SystemEvaluator(agent_a, agent_b, self.triplet_evaluator)
        self.user_study = UserStudy()
        
        # 优化器
        self.optimizer = AdaptiveOptimizer()
        
        # 状态
        self.iteration = 0
        self.metrics_history: List[EvaluationMetrics] = []
        self.best_metrics: Optional[EvaluationMetrics] = None
        self.best_iteration = 0
        self.no_improvement_count = 0
        self.dataset: List[Sentence] = []
        self.reference_triplets: Dict = {}
        
        logger.info("集成演化系统初始化完成")
    
    def start_evolution(self, initial_data: List[Sentence] = None) -> EvolutionReport:
        """
        启动完整的演化流程
        
        Args:
            initial_data: 初始数据集
            
        Returns:
            演化报告
        """
        start_time = time.time()
        
        logger.info("=" * 60)
        logger.info("启动集成演化系统")
        logger.info("=" * 60)
        
        # 初始化数据
        if initial_data:
            self.dataset = initial_data
        else:
            self._initialize_dataset()
        
        logger.info(f"初始数据集大小: {len(self.dataset)}")
        
        # 主演化循环
        converged = False
        for iteration in range(self.config.max_iterations):
            self.iteration = iteration
            
            logger.info(f"\n--- 第 {iteration + 1} 轮 ---")
            
            # 1. 评估当前性能
            logger.info("步骤1: 评估性能...")
            metrics = self._evaluate_current()
            self.metrics_history.append(metrics)
            
            # 2. 检查是否收敛
            logger.info("步骤2: 检查收敛条件...")
            if self._check_convergence(metrics):
                logger.info("✓ 已收敛！")
                converged = True
                break
            
            # 3. 检查目标达成
            if metrics.accuracy >= self.config.target_accuracy:
                logger.info(f"✓ 达到目标准确率 {self.config.target_accuracy}")
                converged = True
                break
            
            # 4. 优化Agent
            logger.info("步骤3: 优化Agent...")
            self._optimize_agents(metrics)
            
            # 5. 定期爬取新数据
            if iteration % self.config.crawl_frequency == 0 and iteration > 0:
                logger.info("步骤4: 爬取新数据...")
                self._fetch_new_data()
            
            # 6. 检查耐心（早停）
            if self._check_patience():
                logger.info("✓ 耐心已耗尽，停止优化")
                break
            
            logger.info(f"性能: 准确率={metrics.accuracy:.4f}, 完整性={metrics.completeness:.4f}")
        
        elapsed = time.time() - start_time
        
        # 生成报告
        report = self._generate_report(elapsed, converged)
        
        return report
    
    def _initialize_dataset(self) -> None:
        """初始化数据集"""
        logger.info("爬取初始数据集...")
        
        # 多源爬取
        self.dataset.extend(self.data_crawler.crawl_from_news())
        self.dataset.extend(self.data_crawler.crawl_from_literature())
        self.dataset.extend(self.data_crawler.crawl_from_encyclopedia())
        
        # 质量过滤
        self.dataset = [
            s for s in self.dataset 
            if s.quality_score >= self.config.quality_threshold
        ]
        
        logger.info(f"初始数据集: {len(self.dataset)} 条高质量句子")
    
    def _evaluate_current(self) -> EvaluationMetrics:
        """评估当前性能"""
        # 分割训练/验证集
        val_size = max(1, int(len(self.dataset) * self.config.validation_ratio))
        val_data = self.dataset[-val_size:]
        
        # 评估
        metrics = self.system_evaluator.evaluate_on_dataset(
            val_data, 
            self.reference_triplets
        )
        
        # 更新最佳模型
        if self.best_metrics is None or metrics.accuracy > self.best_metrics.accuracy:
            self.best_metrics = metrics
            self.best_iteration = self.iteration
            self.no_improvement_count = 0
        else:
            self.no_improvement_count += 1
        
        return metrics
    
    def _check_convergence(self, current_metrics: EvaluationMetrics) -> bool:
        """检查收敛"""
        if len(self.metrics_history) < 2:
            return False
        
        prev_metrics = self.metrics_history[-2]
        
        # 检查多轮平均改进
        improvement = current_metrics.accuracy - prev_metrics.accuracy
        
        return abs(improvement) < self.config.convergence_threshold
    
    def _check_patience(self) -> bool:
        """检查耐心（早停）"""
        return self.no_improvement_count >= self.config.optimization_patience
    
    def _optimize_agents(self, metrics: EvaluationMetrics) -> None:
        """优化Agent"""
        # 调整学习率
        old_lr = self.optimizer.learning_rate
        self._update_learning_rate(metrics)
        logger.info(f"学习率: {old_lr:.4f} -> {self.optimizer.learning_rate:.4f}")
        
        # 调整采样比率
        old_ratio = self.optimizer.sampling_ratio
        self._update_sampling_ratio(metrics)
        logger.info(f"采样比率: {old_ratio:.2f} -> {self.optimizer.sampling_ratio:.2f}")
        
        # 根据性能瓶颈优化
        if metrics.completeness < 0.75:
            logger.info("→ 优化完整性：改进语义规则")
            self._improve_semantic_rules()
        
        if metrics.argument_integrity < 0.75:
            logger.info("→ 优化论元完整性：增强提取模式")
            self._enhance_extraction_patterns()
    
    def _update_learning_rate(self, metrics: EvaluationMetrics) -> None:
        """更新学习率"""
        if len(self.metrics_history) < 2:
            return
        
        prev = self.metrics_history[-2]
        improvement = metrics.accuracy - prev.accuracy
        
        if improvement > 0.05:  # 快速改进
            self.optimizer.learning_rate *= 1.05
        elif improvement < -0.02:  # 性能下降
            self.optimizer.learning_rate *= 0.9
    
    def _update_sampling_ratio(self, metrics: EvaluationMetrics) -> None:
        """更新采样比率"""
        if metrics.accuracy < 0.70:
            self.optimizer.sampling_ratio = 1.0  # 使用全部数据
        elif metrics.accuracy < 0.85:
            self.optimizer.sampling_ratio = 0.7
        else:
            self.optimizer.sampling_ratio = 0.5  # 数据充足，可以采样
    
    def _improve_semantic_rules(self) -> None:
        """改进语义规则"""
        logger.info("→ 执行语义规则优化...")
        
        # 这里可以调用Agent B的规则改进机制
        if hasattr(self.agent_b, 'improve_semantic_rules'):
            self.agent_b.improve_semantic_rules()
    
    def _enhance_extraction_patterns(self) -> None:
        """增强提取模式"""
        logger.info("→ 执行提取模式增强...")
        
        # 这里可以调用Agent A的模式改进机制
        if hasattr(self.agent_a, 'enhance_patterns'):
            self.agent_a.enhance_patterns()
    
    def _fetch_new_data(self) -> None:
        """爬取新数据"""
        new_data = self.data_crawler.crawl_all_sources()
        new_data = [
            s for s in new_data 
            if s.quality_score >= self.config.quality_threshold
        ]
        
        logger.info(f"爬取新数据: {len(new_data)} 条")
        
        # 创建新版本数据集
        self.data_manager.update_training_set(new_data)
        
        # 追加到现有数据
        self.dataset.extend(new_data)
        logger.info(f"数据集现在有 {len(self.dataset)} 条")
    
    def _generate_report(self, elapsed: float, converged: bool) -> EvolutionReport:
        """生成演化报告"""
        report = EvolutionReport(
            config=self.config,
            total_iterations=self.iteration + 1,
            best_metrics=self.best_metrics,
            best_iteration=self.best_iteration,
            convergence_achieved=converged,
            metrics_history=self.metrics_history,
            data_evolution=self._summarize_data_evolution(),
            time_elapsed=elapsed,
            timestamp=datetime.now().isoformat()
        )
        
        return report
    
    def _summarize_data_evolution(self) -> Dict:
        """总结数据演化"""
        return {
            'initial_size': len(self.dataset) // (self.iteration + 1),
            'final_size': len(self.dataset),
            'total_versions': len(self.data_manager.versions) if hasattr(self.data_manager, 'versions') else 0,
            'avg_quality': sum(s.quality_score for s in self.dataset) / len(self.dataset) if self.dataset else 0
        }
    
    def add_user_feedback(self, sentence: str, triplet: Dict, rating: float, 
                        feedback: str = "") -> None:
        """
        添加用户反馈
        
        Args:
            sentence: 句子
            triplet: 三元组
            rating: 用户评分 (0-10)
            feedback: 反馈文本
        """
        if self.config.use_user_feedback:
            self.user_study.add_annotation(sentence, triplet, rating, feedback)
            logger.info(f"添加用户反馈: {sentence[:50]}... (评分: {rating})")
    
    def get_satisfaction_status(self) -> Dict:
        """获取满意度状态"""
        avg_rating = self.user_study.get_average_rating()
        satisfaction = self.user_study.get_satisfaction_level()
        
        return {
            'average_rating': avg_rating,
            'satisfaction_level': satisfaction,
            'total_feedback': len(self.user_study.annotations),
            'system_accuracy': self.best_metrics.accuracy if self.best_metrics else 0.0
        }
    
    def save_report(self, filepath: str) -> None:
        """保存报告"""
        # 需要先运行过演化
        if not self.metrics_history:
            logger.warning("未执行演化，无报告可保存")
            return
        
        report = EvolutionReport(
            config=self.config,
            total_iterations=self.iteration + 1,
            best_metrics=self.best_metrics,
            best_iteration=self.best_iteration,
            convergence_achieved=False,  # 这里需要实际的收敛状态
            metrics_history=self.metrics_history,
            data_evolution=self._summarize_data_evolution(),
            time_elapsed=0.0,
            timestamp=datetime.now().isoformat()
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)
        
        logger.info(f"报告已保存至: {filepath}")


def run_full_evolution_demo(agent_a, agent_b) -> EvolutionReport:
    """
    运行完整演化演示
    
    Args:
        agent_a: Agent A实例
        agent_b: Agent B实例
        
    Returns:
        演化报告
    """
    # 配置
    config = EvolutionConfig(
        max_iterations=20,
        convergence_threshold=0.02,
        target_accuracy=0.80,
        crawl_frequency=5,
        optimization_patience=8
    )
    
    # 创建系统
    system = IntegratedEvolutionSystem(agent_a, agent_b, config)
    
    # 运行演化
    report = system.start_evolution()
    
    # 显示结果
    print("\n" + "=" * 60)
    print("演化完成！")
    print("=" * 60)
    print(f"总轮数: {report.total_iterations}")
    print(f"最佳准确率: {report.best_metrics.accuracy:.4f}")
    print(f"最佳轮数: {report.best_iteration}")
    print(f"总耗时: {report.time_elapsed:.1f}秒")
    print(f"是否收敛: {report.convergence_achieved}")
    print(f"满意度: {system.get_satisfaction_status()['satisfaction_level']}")
    print("=" * 60)
    
    return report
