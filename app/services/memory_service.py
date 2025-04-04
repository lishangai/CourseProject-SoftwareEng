import redis
from datetime import datetime, timedelta
from flask import current_app
import json
import random

class MemoryService:
    """记忆管理服务类"""
    
    def __init__(self):
        """初始化记忆服务"""
        self.redis_client = redis.from_url(current_app.config['REDIS_URL'])
        self.intervals = current_app.config['MEMORY_INTERVALS']
        self.memory_strength_threshold = current_app.config['MEMORY_STRENGTH_THRESHOLD']
        # 实际应用中应从数据库加载数据
        self.user_memory = {}

    def get_review_schedule(self, user_id):
        """获取用户的复习计划
        
        Args:
            user_id: 用户ID
            
        Returns:
            list: 复习计划列表
        """
        # 实际应用中应从数据库获取数据
        # 这里使用模拟数据
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 生成今日复习内容
        today_reviews = [
            {
                'concept': '机器学习',
                'memory_strength': 0.65,
                'next_review': today,
                'review_count': 3
            },
            {
                'concept': '神经网络',
                'memory_strength': 0.45,
                'next_review': today,
                'review_count': 2
            },
            {
                'concept': '深度学习',
                'memory_strength': 0.75,
                'next_review': today,
                'review_count': 5
            }
        ]
        
        # 生成历史复习内容
        history_reviews = []
        concepts = ['Python', '数据结构', '算法', '数据库', 'Web开发', '人工智能', '大数据']
        
        for i in range(10):
            days_ago = random.randint(1, 30)
            review_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
            concept = random.choice(concepts)
            memory_strength = random.uniform(0.3, 0.9)
            review_count = random.randint(1, 8)
            
            history_reviews.append({
                'concept': concept,
                'memory_strength': memory_strength,
                'next_review': review_date,
                'review_count': review_count
            })
        
        # 合并今日和历史复习内容
        return today_reviews + history_reviews

    def start_review(self, user_id, concept):
        """开始复习某个概念
        
        Args:
            user_id: 用户ID
            concept: 概念名称
            
        Returns:
            dict: 操作结果
        """
        # 实际应用中应更新数据库
        return {
            'status': 'success',
            'message': f'已开始复习概念: {concept}',
            'timestamp': datetime.now().isoformat()
        }

    def skip_review(self, user_id, concept):
        """跳过复习某个概念
        
        Args:
            user_id: 用户ID
            concept: 概念名称
            
        Returns:
            dict: 操作结果
        """
        # 实际应用中应更新数据库
        return {
            'status': 'success',
            'message': f'已跳过概念: {concept}',
            'timestamp': datetime.now().isoformat()
        }

    def get_learning_stats(self, user_id):
        """获取学习统计数据
        
        Args:
            user_id: 用户ID
            
        Returns:
            dict: 学习统计数据
        """
        # 实际应用中应从数据库获取数据
        return {
            'total_concepts': 25,
            'mastered_concepts': 15,
            'review_count': 120,
            'average_strength': 0.75
        }

    def get_memory_strength(self, user_id):
        """获取记忆强度数据
        
        Args:
            user_id: 用户ID
            
        Returns:
            dict: 记忆强度数据
        """
        # 实际应用中应从数据库获取数据
        concepts = ['机器学习', '神经网络', '深度学习', 'Python', '数据结构', '算法', '数据库']
        strengths = [random.uniform(0.3, 0.9) for _ in range(len(concepts))]
        
        return {
            'concepts': concepts,
            'strengths': strengths
        }

    def _get_learning_records(self, user_id):
        """获取用户的学习记录"""
        records_key = f"learning_records:{user_id}"
        records = self.redis_client.get(records_key)
        return json.loads(records) if records else []

    def _calculate_next_review(self, first_learned, memory_strength):
        """计算下次复习时间"""
        if memory_strength >= self.memory_strength_threshold:
            return None
            
        # 根据记忆强度选择复习间隔
        interval_index = int(memory_strength * len(self.intervals))
        if interval_index >= len(self.intervals):
            return None
            
        days = self.intervals[interval_index]
        return first_learned + timedelta(days=days)

    def update_memory_strength(self, user_id, concept, performance_score):
        """更新概念的记忆强度"""
        try:
            records_key = f"learning_records:{user_id}"
            records = self._get_learning_records(user_id)
            
            # 查找并更新记录
            for record in records:
                if record['concept'] == concept:
                    # 根据表现更新记忆强度
                    new_strength = self._calculate_new_strength(
                        record.get('memory_strength', 0.5),
                        performance_score
                    )
                    record['memory_strength'] = new_strength
                    record['review_count'] = record.get('review_count', 0) + 1
                    record['last_reviewed'] = datetime.now().isoformat()
                    break
            
            # 保存更新后的记录
            self.redis_client.set(records_key, json.dumps(records))
            
        except Exception as e:
            raise Exception(f"更新记忆强度失败: {str(e)}")

    def _calculate_new_strength(self, current_strength, performance_score):
        """计算新的记忆强度"""
        # 简单的线性更新模型
        # 可以根据需要实现更复杂的算法
        weight = 0.3  # 学习权重
        new_strength = current_strength * (1 - weight) + performance_score * weight
        return min(max(new_strength, 0), 1)  # 确保在0-1之间

    def add_learning_record(self, user_id, concept):
        """添加新的学习记录"""
        try:
            records_key = f"learning_records:{user_id}"
            records = self._get_learning_records(user_id)
            
            # 检查是否已存在
            for record in records:
                if record['concept'] == concept:
                    return
            
            # 添加新记录
            new_record = {
                'concept': concept,
                'first_learned': datetime.now().isoformat(),
                'memory_strength': 0.5,
                'review_count': 0
            }
            records.append(new_record)
            
            # 保存更新后的记录
            self.redis_client.set(records_key, json.dumps(records))
            
        except Exception as e:
            raise Exception(f"添加学习记录失败: {str(e)}") 