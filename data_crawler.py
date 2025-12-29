"""
数据爬取模块 - 自动从网络抽取例句用于Agent训练和演化

支持多种数据源:
1. 中文维基百科示例句
2. 新闻和评论文本
3. 文学作品
4. 开源NLP数据集

数据质量控制:
- 自动清洗和标准化
- 去重处理
- 长度过滤
"""

import re
import json
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from collections import defaultdict
import time


@dataclass
class Sentence:
    """表示一个句子的数据结构"""
    text: str                    # 原始句子
    source: str                  # 来源 (wikipedia, news, etc.)
    domain: str                  # 领域 (social, news, literature, etc.)
    quality_score: float = 0.0   # 质量分数 (0-1)
    metadata: Dict = None        # 额外元数据
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class DataCrawler:
    """
    数据爬取器 - 从多个源自动获取例句
    
    特点:
    - 多数据源支持 (可轻易扩展)
    - 质量评估和过滤
    - 结构化输出
    - 批量处理
    """
    
    def __init__(self, cache_size: int = 10000):
        """
        初始化数据爬取器
        
        Args:
            cache_size: 内存缓存大小
        """
        self.cache_size = cache_size
        self.sentence_cache = []
        self.source_counts = defaultdict(int)
        self.quality_threshold = 0.5
    
    def crawl_from_news(self, keywords: List[str] = None, limit: int = 100) -> List[Sentence]:
        """
        从新闻源爬取例句
        
        Args:
            keywords: 关键词列表
            limit: 最多爬取的句子数
            
        Returns:
            句子列表
        """
        # 这里会使用真实的新闻API (NewsAPI, 新闻爬虫等)
        # 示例数据用于演示
        sample_news_sentences = [
            "今天天气非常晴朗，适合出去游玩。",
            "公司在北京成立了新的研发中心。",
            "他用创新的方式解决了这个问题。",
            "技术团队正在努力开发新产品。",
            "市场需求不断增长，企业获利良好。",
            "为了提高效率，我们采取了新措施。",
            "专家建议消费者谨慎选择投资产品。",
            "这项政策将从下个月开始实施。",
            "学生们在学校认真地学习数学。",
            "运动员在比赛中表现出色获得了奖牌。",
        ]
        
        sentences = []
        for text in sample_news_sentences[:limit]:
            sentence = Sentence(
                text=text,
                source='news',
                domain='general',
                quality_score=self._evaluate_sentence_quality(text),
                metadata={'crawl_time': time.time()}
            )
            if sentence.quality_score >= self.quality_threshold:
                sentences.append(sentence)
                self.source_counts['news'] += 1
        
        return sentences
    
    def crawl_from_literature(self, limit: int = 100) -> List[Sentence]:
        """
        从文学作品爬取例句
        
        Returns:
            句子列表
        """
        sample_literature = [
            "那个高大的男人在远方的山上看到了一只鸟。",
            "她用温柔的语气对我说话。",
            "在那个寒冷的冬夜，我感到了深深的孤独。",
            "他怀着对未来的美好憧憬踏上了旅程。",
            "时光在指尖悄悄流逝，留下了无数回忆。",
            "老人每天都在公园里散步，思考人生的意义。",
            "这个古老的城市见证了历史的变迁。",
            "她用笔在纸上缓缓写下自己的心声。",
            "窗外的雨声伴随着我进入了梦乡。",
            "他们在那条林荫小道上漫步，讨论着人生的哲学。",
        ]
        
        sentences = []
        for text in sample_literature[:limit]:
            sentence = Sentence(
                text=text,
                source='literature',
                domain='fiction',
                quality_score=self._evaluate_sentence_quality(text),
                metadata={'genre': 'literature'}
            )
            if sentence.quality_score >= self.quality_threshold:
                sentences.append(sentence)
                self.source_counts['literature'] += 1
        
        return sentences
    
    def crawl_from_encyclopedia(self, limit: int = 100) -> List[Sentence]:
        """
        从百科全书爬取例句
        
        Returns:
            句子列表
        """
        sample_encyclopedia = [
            "中国是世界上人口最多的国家。",
            "物理学研究物质和能量的基本性质。",
            "计算机科学在现代社会中应用广泛。",
            "生物学家通过显微镜观察细胞的结构。",
            "化学反应在工业生产中起到重要作用。",
            "地理学研究地球表面的各种现象。",
            "数学是所有科学的基础。",
            "历史学家研究过去的文明和事件。",
            "艺术家用创意表达他们对世界的看法。",
            "经济学分析生产、分配和消费的规律。",
        ]
        
        sentences = []
        for text in sample_encyclopedia[:limit]:
            sentence = Sentence(
                text=text,
                source='encyclopedia',
                domain='factual',
                quality_score=self._evaluate_sentence_quality(text),
                metadata={'type': 'factual'}
            )
            if sentence.quality_score >= self.quality_threshold:
                sentences.append(sentence)
                self.source_counts['encyclopedia'] += 1
        
        return sentences
    
    def crawl_from_social_media(self, limit: int = 100) -> List[Sentence]:
        """
        从社交媒体爬取例句
        
        Returns:
            句子列表
        """
        sample_social = [
            "我昨天在咖啡馆喝了一杯很好喝的咖啡。",
            "他们一起去旅游，拍了很多美丽的照片。",
            "我新买的书昨天终于送到了。",
            "天气真好，适合去户外活动。",
            "看到这个新闻真的很开心。",
            "工作太累了，需要休息一下。",
            "朋友推荐我看了一部很不错的电影。",
            "假期的时候我们一家去爬山。",
            "最近学到了很多新东西，感觉很充实。",
            "今天做菜的时候不小心烧糊了。",
        ]
        
        sentences = []
        for text in sample_social[:limit]:
            sentence = Sentence(
                text=text,
                source='social_media',
                domain='social',
                quality_score=self._evaluate_sentence_quality(text),
                metadata={'platform': 'weibo'}
            )
            if sentence.quality_score >= self.quality_threshold:
                sentences.append(sentence)
                self.source_counts['social_media'] += 1
        
        return sentences
    
    def _evaluate_sentence_quality(self, sentence: str) -> float:
        """
        评估句子质量
        
        指标:
        - 长度合适 (8-120个字符)
        - 没有特殊符号过多
        - 结构完整
        
        Returns:
            质量分数 (0-1)
        """
        score = 1.0
        
        # 长度检查
        if len(sentence) < 8 or len(sentence) > 120:
            score -= 0.3
        
        # 特殊字符检查
        special_char_ratio = len(re.findall(r'[^a-zA-Z0-9\u4e00-\u9fff，。！？；：、·\s]', sentence)) / len(sentence)
        if special_char_ratio > 0.2:
            score -= 0.2
        
        # 重复字符检查
        if re.search(r'(.)\1{3,}', sentence):
            score -= 0.2
        
        # 中文句子检查 (检查句子成分的完整性)
        has_cjk = bool(re.search(r'[\u4e00-\u9fff]', sentence))
        if has_cjk:
            # 应该有动词或形容词
            if not re.search(r'[是有做说给去来在被]', sentence):
                score -= 0.15
        
        return max(0.0, min(1.0, score))
    
    def crawl_all_sources(self, per_source: int = 50) -> List[Sentence]:
        """
        从所有源爬取数据
        
        Args:
            per_source: 每个源爬取的句子数
            
        Returns:
            所有句子列表
        """
        all_sentences = []
        
        # 从各个源爬取
        all_sentences.extend(self.crawl_from_news(limit=per_source))
        all_sentences.extend(self.crawl_from_literature(limit=per_source))
        all_sentences.extend(self.crawl_from_encyclopedia(limit=per_source))
        all_sentences.extend(self.crawl_from_social_media(limit=per_source))
        
        # 去重
        seen_texts = set()
        unique_sentences = []
        for sentence in all_sentences:
            if sentence.text not in seen_texts:
                seen_texts.add(sentence.text)
                unique_sentences.append(sentence)
        
        return unique_sentences
    
    def filter_by_quality(self, sentences: List[Sentence], 
                         min_quality: float = 0.5) -> List[Sentence]:
        """
        按质量过滤句子
        
        Args:
            sentences: 句子列表
            min_quality: 最低质量分数
            
        Returns:
            过滤后的句子列表
        """
        return [s for s in sentences if s.quality_score >= min_quality]
    
    def filter_by_domain(self, sentences: List[Sentence], 
                        domains: List[str]) -> List[Sentence]:
        """
        按领域过滤句子
        
        Args:
            sentences: 句子列表
            domains: 领域列表
            
        Returns:
            过滤后的句子列表
        """
        return [s for s in sentences if s.domain in domains]
    
    def filter_by_length(self, sentences: List[Sentence],
                        min_len: int = 5, max_len: int = 120) -> List[Sentence]:
        """
        按长度过滤句子
        
        Args:
            sentences: 句子列表
            min_len: 最小长度
            max_len: 最大长度
            
        Returns:
            过滤后的句子列表
        """
        return [s for s in sentences if min_len <= len(s.text) <= max_len]
    
    def export_sentences(self, sentences: List[Sentence], 
                        filepath: str) -> None:
        """
        导出句子为JSON格式
        
        Args:
            sentences: 句子列表
            filepath: 输出文件路径
        """
        data = [
            {
                'text': s.text,
                'source': s.source,
                'domain': s.domain,
                'quality_score': s.quality_score,
                'metadata': s.metadata
            }
            for s in sentences
        ]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_statistics(self, sentences: List[Sentence]) -> Dict[str, Any]:
        """
        获取数据集统计信息
        
        Args:
            sentences: 句子列表
            
        Returns:
            统计信息字典
        """
        if not sentences:
            return {'total': 0}
        
        source_dist = defaultdict(int)
        domain_dist = defaultdict(int)
        quality_scores = []
        lengths = []
        
        for s in sentences:
            source_dist[s.source] += 1
            domain_dist[s.domain] += 1
            quality_scores.append(s.quality_score)
            lengths.append(len(s.text))
        
        return {
            'total': len(sentences),
            'source_distribution': dict(source_dist),
            'domain_distribution': dict(domain_dist),
            'average_quality': sum(quality_scores) / len(quality_scores),
            'min_quality': min(quality_scores),
            'max_quality': max(quality_scores),
            'average_length': sum(lengths) / len(lengths),
            'min_length': min(lengths),
            'max_length': max(lengths)
        }


class DataManager:
    """
    数据管理器 - 管理爬取、存储和版本控制
    """
    
    def __init__(self, data_dir: str = './data'):
        """
        初始化数据管理器
        
        Args:
            data_dir: 数据目录
        """
        self.data_dir = data_dir
        self.crawler = DataCrawler()
        self.dataset_versions = {}
    
    def create_training_set(self, name: str, size: int = 500, 
                          quality_threshold: float = 0.5) -> List[Sentence]:
        """
        创建训练集
        
        Args:
            name: 数据集名称
            size: 数据集大小
            quality_threshold: 质量阈值
            
        Returns:
            训练集句子列表
        """
        # 爬取数据
        all_sentences = self.crawler.crawl_all_sources(per_source=size // 4)
        
        # 过滤
        filtered = self.crawler.filter_by_quality(all_sentences, quality_threshold)
        
        # 截断到指定大小
        dataset = filtered[:size]
        
        # 记录版本
        self.dataset_versions[name] = {
            'size': len(dataset),
            'quality_threshold': quality_threshold,
            'timestamp': time.time(),
            'statistics': self.crawler.get_statistics(dataset)
        }
        
        return dataset
    
    def update_training_set(self, name: str, additional_size: int = 100) -> List[Sentence]:
        """
        更新训练集 (添加新数据)
        
        Args:
            name: 数据集名称
            additional_size: 新增数据量
            
        Returns:
            更新后的训练集
        """
        # 爬取新数据
        new_sentences = self.crawler.crawl_all_sources(per_source=additional_size // 4)
        
        return new_sentences
