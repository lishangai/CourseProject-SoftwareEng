import random
from datetime import datetime, timedelta
from app.services.deepseek_client import DeepSeekClient

class LearningService:
    """学习服务类"""
    
    def __init__(self):
        """初始化学习服务"""
        # 实际应用中应从数据库加载数据
        self.learning_paths = {}
        self.deepseek_client = DeepSeekClient()
    
    def generate_learning_path(self, concept, user_level='beginner'):
        """生成学习路径
        
        Args:
            concept: 概念名称
            user_level: 用户水平，可选值为 beginner, intermediate, advanced
            
        Returns:
            dict: 学习路径
        """
        try:
            # 使用DeepSeek API生成学习路径
            messages = [
                {
                    'role': 'system',
                    'content': '你是一个专业的教育专家，擅长设计学习路径。'
                },
                {
                    'role': 'user',
                    'content': f'请为"{concept}"这个概念设计一个适合{user_level}水平的学习路径，包括每天的学习目标和活动。'
                }
            ]
            
            response = self.deepseek_client.chat_completion(messages)
            content = response['choices'][0]['message']['content']
            
            # 解析响应内容
            learning_path = self._parse_learning_path(content)
            return learning_path
            
        except Exception as e:
            # 如果API调用失败，使用模拟数据
            # 根据用户水平调整学习路径
            if user_level == 'beginner':
                days = 7
                difficulty = '简单'
            elif user_level == 'intermediate':
                days = 5
                difficulty = '中等'
            else:  # advanced
                days = 3
                difficulty = '困难'
            
            # 生成学习路径
            learning_path = {}
            
            # 第一天：介绍和基础
            learning_path['day1'] = {
                'goal': f'了解{concept}的基本概念和原理',
                'activities': [
                    f'阅读{concept}的入门介绍',
                    f'观看{concept}的基础视频教程',
                    f'完成{concept}的基础练习题'
                ],
                'resources': [
                    f'https://example.com/{concept}/intro',
                    f'https://example.com/{concept}/video',
                    f'https://example.com/{concept}/exercises'
                ]
            }
            
            # 第二天到倒数第二天：深入学习
            for day in range(2, days):
                learning_path[f'day{day}'] = {
                    'goal': f'深入学习{concept}的{difficulty}内容',
                    'activities': [
                        f'学习{concept}的{difficulty}知识点',
                        f'完成{concept}的{difficulty}练习题',
                        f'阅读{concept}的{difficulty}案例'
                    ],
                    'resources': [
                        f'https://example.com/{concept}/advanced{day}',
                        f'https://example.com/{concept}/exercises{day}',
                        f'https://example.com/{concept}/cases{day}'
                    ]
                }
            
            # 最后一天：总结和实践
            learning_path[f'day{days}'] = {
                'goal': f'总结{concept}的学习内容并进行实践',
                'activities': [
                    f'复习{concept}的所有知识点',
                    f'完成{concept}的综合项目',
                    f'参与{concept}的讨论或问答'
                ],
                'resources': [
                    f'https://example.com/{concept}/summary',
                    f'https://example.com/{concept}/project',
                    f'https://example.com/{concept}/forum'
                ]
            }
            
            return learning_path
    
    def _parse_learning_path(self, content):
        """解析学习路径内容
        
        Args:
            content: API响应内容
            
        Returns:
            dict: 学习路径
        """
        learning_path = {}
        current_day = None
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('第') and '天' in line:
                # 新的一天
                day_num = int(line[1:line.index('天')])
                current_day = f'day{day_num}'
                learning_path[current_day] = {
                    'goal': '',
                    'activities': [],
                    'resources': []
                }
            elif line.startswith('目标：'):
                # 学习目标
                learning_path[current_day]['goal'] = line[3:].strip()
            elif line.startswith('- '):
                # 学习活动或资源
                item = line[2:].strip()
                if 'http' in item:
                    learning_path[current_day]['resources'].append(item)
                else:
                    learning_path[current_day]['activities'].append(item)
        
        return learning_path 