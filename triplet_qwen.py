"""
Triplet-Qwen 核心API

简化的导入接口，用户只需导入这个模块即可使用所有功能。
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import logging

# 核心模块
from agent_a import TripletsExtractionAgent
from agent_b import TripletsValidationAgent
from data_crawler import DataCrawler, DataManager, Sentence
from evolution_system import EvolutionSystem, AdaptiveOptimizer
from evaluation_metrics import SystemEvaluator, TripleteEvaluator, UserStudy
from code_optimization import CacheManager, PerformanceMonitor, optimize_system
from integrated_evolution import IntegratedEvolutionSystem, EvolutionConfig, EvolutionReport

# 版本号
__version__ = "1.0.0"

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 导出的公开API
__all__ = [
    # Agent
    'TripletsExtractionAgent',
    'TripletsValidationAgent',
    
    # 演化系统
    'IntegratedEvolutionSystem',
    'EvolutionConfig',
    'EvolutionReport',
    
    # 数据采集
    'DataCrawler',
    'DataManager',
    'Sentence',
    
    # 评估
    'SystemEvaluator',
    'TripleteEvaluator',
    'UserStudy',
    
    # 优化
    'CacheManager',
    'PerformanceMonitor',
    'optimize_system',
    
    # 版本
    '__version__',
]


def quick_start(agent_a=None, agent_b=None, **kwargs) -> EvolutionReport:
    """
    快速启动演化系统
    
    Args:
        agent_a: Agent A实例，如果为None则自动创建
        agent_b: Agent B实例，如果为None则自动创建
        **kwargs: 传递给EvolutionConfig的参数
        
    Returns:
        演化报告
        
    Example:
        >>> from triplet_qwen import quick_start
        >>> report = quick_start()
    """
    if agent_a is None:
        agent_a = TripletsExtractionAgent()
    
    if agent_b is None:
        agent_b = TripletsValidationAgent()
    
    config = EvolutionConfig(**kwargs)
    system = IntegratedEvolutionSystem(agent_a, agent_b, config)
    
    return system.start_evolution()
