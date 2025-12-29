"""
双智能体协作框架
管理智能体A和B的交互，直至三元组达到完美状态
"""

from typing import Dict, List, Tuple, Any
import json
from datetime import datetime


class DualAgentSystem:
    """
    双智能体系统
    
    工作流程:
    1. 智能体A抽取初始三元组
    2. 智能体B验证三元组
    3. 如果不完整，B提供反馈
    4. A根据反馈修订三元组
    5. 重复2-4直至完美或达到最大迭代数
    """
    
    def __init__(self, agent_a, agent_b, max_iterations: int = 3):
        """
        初始化双智能体系统
        
        Args:
            agent_a: 三元组抽取智能体
            agent_b: 三元组验证智能体
            max_iterations: 最大迭代次数
        """
        self.agent_a = agent_a
        self.agent_b = agent_b
        self.max_iterations = max_iterations
        self.interaction_history = []
    
    def process_sentence(self, sentence: str) -> Dict[str, Any]:
        """
        处理一个句子，使用双智能体进行完整的三元组抽取-验证循环
        
        Args:
            sentence: 输入句子
            
        Returns:
            最终的处理结果
        """
        print(f"\n{'='*70}")
        print(f"开始处理句子: {sentence}")
        print(f"{'='*70}")
        
        # 第一步：智能体A进行初始抽取
        print(f"\n[第1步] 智能体A进行初始三元组抽取...")
        initial_triplet = self.agent_a.extract_triplets(sentence)
        
        if initial_triplet.get('error'):
            print(f"✗ 初始抽取失败: {initial_triplet['error']}")
            return initial_triplet
        
        print(f"✓ 初始三元组: {self.agent_a.format_output(initial_triplet)}")
        
        # 迭代验证和修订
        current_triplet = initial_triplet
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            print(f"\n[第{iteration+1}步] 智能体B进行验证...")
            
            # 智能体B验证
            validation_result = self.agent_b.validate_triplet(sentence, current_triplet)
            self.agent_b.print_validation_result(validation_result)
            
            # 记录交互
            self.interaction_history.append({
                'sentence': sentence,
                'iteration': iteration,
                'triplet': current_triplet,
                'validation': validation_result,
                'timestamp': datetime.now().isoformat()
            })
            
            # 如果验证通过，则完成
            if validation_result['is_valid']:
                print(f"\n✓ 三元组验证通过！")
                return {
                    'sentence': sentence,
                    'final_triplet': current_triplet,
                    'is_valid': True,
                    'iterations': iteration,
                    'validation_result': validation_result,
                    'interaction_history': self.interaction_history[-iteration:]
                }
            
            # 如果未通过且未达到最大迭代次数，则修订
            if iteration < self.max_iterations:
                print(f"\n[第{iteration+1}步] 智能体A根据反馈进行修订...")
                
                revised_triplet = self.agent_a.revise_triplet(
                    validation_result['feedback'],
                    {
                        'sentence': sentence,
                        'triplet': current_triplet,
                        'attempt': iteration
                    }
                )
                
                print(f"✓ 修订后的三元组: {self.agent_a.format_output(revised_triplet)}")
                current_triplet = revised_triplet
            else:
                print(f"\n⚠ 已达到最大迭代次数({self.max_iterations})，停止修订")
        
        # 达到最大迭代次数但未验证通过
        final_validation = self.agent_b.validate_triplet(sentence, current_triplet)
        
        return {
            'sentence': sentence,
            'final_triplet': current_triplet,
            'is_valid': final_validation['is_valid'],
            'iterations': self.max_iterations,
            'final_validation': final_validation,
            'status': 'max_iterations_reached',
            'interaction_history': self.interaction_history[-self.max_iterations:]
        }
    
    def process_batch(self, sentences: List[str], save_results: bool = False) -> List[Dict]:
        """
        批量处理多个句子
        
        Args:
            sentences: 句子列表
            save_results: 是否保存结果
            
        Returns:
            所有句子的处理结果
        """
        results = []
        
        for i, sentence in enumerate(sentences, 1):
            print(f"\n\n{'#'*70}")
            print(f"# 处理句子 {i}/{len(sentences)}")
            print(f"{'#'*70}")
            
            result = self.process_sentence(sentence)
            results.append(result)
        
        # 保存结果
        if save_results:
            self._save_results(results)
        
        return results
    
    def _save_results(self, results: List[Dict], filename: str = "results.json") -> None:
        """保存处理结果"""
        
        # 转换为可序列化的格式
        serializable_results = []
        for result in results:
            serializable_result = {
                'sentence': result['sentence'],
                'final_triplet': self._format_triplet_for_output(result['final_triplet']),
                'is_valid': result['is_valid'],
                'iterations': result['iterations'],
                'status': result.get('status', 'success')
            }
            serializable_results.append(serializable_result)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 结果已保存到 {filename}")
    
    def _format_triplet_for_output(self, triplet: Dict) -> str:
        """格式化三元组用于输出"""
        return self.agent_a.format_output(triplet)
    
    def print_summary(self, results: List[Dict]) -> None:
        """打印处理总结"""
        
        print(f"\n{'='*70}")
        print(f"处理总结")
        print(f"{'='*70}\n")
        
        total = len(results)
        valid_count = sum(1 for r in results if r['is_valid'])
        avg_iterations = sum(r['iterations'] for r in results) / total if total > 0 else 0
        
        print(f"总句子数: {total}")
        print(f"验证通过: {valid_count}/{total} ({valid_count/total*100:.1f}%)")
        print(f"平均迭代次数: {avg_iterations:.1f}")
        
        print(f"\n详细结果:")
        for i, result in enumerate(results, 1):
            status = "✓" if result['is_valid'] else "✗"
            print(f"  {i}. {status} {result['sentence']}")
            print(f"     三元组: {self._format_triplet_for_output(result['final_triplet'])}")
            print(f"     迭代数: {result['iterations']}")
        
        print(f"\n{'='*70}\n")
