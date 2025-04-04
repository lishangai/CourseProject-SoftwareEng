import openai
from flask import current_app
import json
import random
from app.services.deepseek_client import DeepSeekClient

class ConceptService:
    def __init__(self):
        openai.api_key = current_app.config['OPENAI_API_KEY']
        self.model = current_app.config['OPENAI_MODEL']
        # 实际应用中应从数据库加载数据
        self.concepts = {}
        self.deepseek_client = DeepSeekClient()

    def get_explanation(self, concept):
        """获取概念的多角度解释"""
        prompt = current_app.config['CONCEPT_EXPLANATION_TEMPLATE'].format(concept=concept)
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的教育专家，擅长用多种方式解释复杂概念。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            explanation = response.choices[0].message.content
            return self._structure_explanation(explanation)
        except Exception as e:
            raise Exception(f"获取概念解释失败: {str(e)}")

    def _structure_explanation(self, raw_explanation):
        """将原始解释结构化"""
        # 这里可以添加更复杂的解析逻辑
        sections = raw_explanation.split('\n\n')
        return {
            'core_definition': sections[0] if len(sections) > 0 else '',
            'feynman_explanation': sections[1] if len(sections) > 1 else '',
            'common_misconceptions': sections[2] if len(sections) > 2 else ''
        }

    def generate_exercises(self, concept, difficulty='medium'):
        """生成练习题"""
        prompt = f"""
        为概念"{concept}"生成3道{difficulty}难度的练习题，包括：
        1. 一道判断题
        2. 一道案例分析题
        3. 一道代码填空题
        
        请按以下JSON格式返回：
        {{
            "true_false": {{
                "question": "问题描述",
                "answer": true/false,
                "explanation": "解释"
            }},
            "case_study": {{
                "question": "问题描述",
                "answer": "参考答案",
                "key_points": ["要点1", "要点2"]
            }},
            "code_fill": {{
                "question": "代码片段",
                "answer": "填空答案",
                "hints": ["提示1", "提示2"]
            }}
        }}
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的教育专家，擅长出题。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            raise Exception(f"生成练习题失败: {str(e)}")

    def generate_learning_path(self, concept, user_level='beginner'):
        """生成学习路径"""
        prompt = f"""
        为{user_level}级别的学习者制定"{concept}"的学习路径，包括：
        1. 3天的学习计划
        2. 每天的学习目标
        3. 推荐的学习资源
        
        请按以下JSON格式返回：
        {{
            "day1": {{
                "goal": "学习目标",
                "resources": ["资源1", "资源2"],
                "activities": ["活动1", "活动2"]
            }},
            "day2": {{
                "goal": "学习目标",
                "resources": ["资源1", "资源2"],
                "activities": ["活动1", "活动2"]
            }},
            "day3": {{
                "goal": "学习目标",
                "resources": ["资源1", "资源2"],
                "activities": ["活动1", "活动2"]
            }}
        }}
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的教育专家，擅长制定学习计划。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            raise Exception(f"生成学习路径失败: {str(e)}")

    def search_concept(self, query):
        """搜索概念
        
        Args:
            query: 搜索关键词
            
        Returns:
            list: 搜索结果列表
        """
        # 实际应用中应从数据库搜索
        # 这里使用模拟数据
        concepts = [
            '机器学习', '深度学习', '神经网络', 'Python', '数据结构', 
            '算法', '数据库', 'Web开发', '人工智能', '大数据'
        ]
        
        # 简单的模糊匹配
        results = [c for c in concepts if query.lower() in c.lower()]
        
        return results
    
    def get_concept(self, concept_name):
        """获取概念详情
        
        Args:
            concept_name: 概念名称
            
        Returns:
            dict: 概念详情
        """
        # 实际应用中应从数据库获取
        # 这里使用模拟数据
        return {
            'name': concept_name,
            'description': f'{concept_name}是一个重要的概念，在多个领域都有应用。',
            'category': random.choice(['计算机科学', '人工智能', '数据科学', '软件工程']),
            'difficulty': random.choice(['简单', '中等', '困难']),
            'related_concepts': random.sample([
                '机器学习', '深度学习', '神经网络', 'Python', '数据结构', 
                '算法', '数据库', 'Web开发', '人工智能', '大数据'
            ], 3)
        }
    
    def get_concept_explanation(self, concept_name):
        """获取概念解释
        
        Args:
            concept_name: 概念名称
            
        Returns:
            dict: 概念解释
        """
        try:
            # 使用DeepSeek API生成概念解释
            return self.deepseek_client.generate_concept_explanation(concept_name)
        except Exception as e:
            # 如果API调用失败，使用模拟数据
            return {
                'core_definition': f'{concept_name}的核心定义是...',
                'feynman_explanation': f'用费曼技巧解释{concept_name}...',
                'misconceptions': [
                    f'关于{concept_name}的常见误解1...',
                    f'关于{concept_name}的常见误解2...',
                    f'关于{concept_name}的常见误解3...'
                ]
            }
    
    def get_concept_exercises(self, concept_name):
        """获取概念练习题
        
        Args:
            concept_name: 概念名称
            
        Returns:
            dict: 练习题
        """
        try:
            # 使用DeepSeek API生成练习题
            return self.deepseek_client.generate_exercises(concept_name)
        except Exception as e:
            # 如果API调用失败，使用模拟数据
            return {
                'true_false': [
                    {
                        'question': f'关于{concept_name}的说法1是正确的。',
                        'answer': True,
                        'explanation': f'解释为什么关于{concept_name}的说法1是正确的。'
                    },
                    {
                        'question': f'关于{concept_name}的说法2是错误的。',
                        'answer': False,
                        'explanation': f'解释为什么关于{concept_name}的说法2是错误的。'
                    }
                ],
                'case_studies': [
                    {
                        'scenario': f'场景1：如何使用{concept_name}解决问题A...',
                        'questions': [
                            f'在场景1中，{concept_name}的应用是否正确？',
                            f'在场景1中，如何改进{concept_name}的应用？'
                        ],
                        'answers': [
                            '是的，应用正确。',
                            '可以通过以下方式改进...'
                        ]
                    }
                ],
                'code_exercises': [
                    {
                        'description': f'编写代码实现{concept_name}的基本功能...',
                        'template': 'def function_name():\n    # 在这里编写代码\n    pass',
                        'solution': 'def function_name():\n    # 解决方案\n    return result',
                        'hints': [
                            f'提示1：考虑{concept_name}的核心特性...',
                            f'提示2：注意{concept_name}的边界条件...'
                        ]
                    }
                ]
            }
    
    def get_concept_knowledge_graph(self, concept_name):
        """获取概念知识图谱
        
        Args:
            concept_name: 概念名称
            
        Returns:
            dict: 知识图谱
        """
        # 实际应用中应从数据库获取
        # 这里使用模拟数据
        related_concepts = random.sample([
            '机器学习', '深度学习', '神经网络', 'Python', '数据结构', 
            '算法', '数据库', 'Web开发', '人工智能', '大数据'
        ], 5)
        
        nodes = [{'id': concept_name, 'label': concept_name, 'group': 0}]
        edges = []
        
        for i, related in enumerate(related_concepts):
            nodes.append({'id': related, 'label': related, 'group': i+1})
            edges.append({'from': concept_name, 'to': related, 'label': f'相关'})
        
        return {
            'nodes': nodes,
            'edges': edges
        } 