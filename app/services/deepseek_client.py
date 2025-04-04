from openai import OpenAI
from flask import current_app

class DeepSeekClient:
    """DeepSeek API客户端"""
    
    def __init__(self):
        """初始化DeepSeek客户端"""
        self.client = OpenAI(
            api_key=current_app.config['DEEPSEEK_API_KEY'],
            base_url=current_app.config['DEEPSEEK_API_BASE']
        )
        self.model = current_app.config['DEEPSEEK_MODEL']
    
    def chat_completion(self, messages, temperature=0.7, max_tokens=2000):
        """发送聊天请求
        
        Args:
            messages: 消息列表
            temperature: 温度参数，控制随机性
            max_tokens: 最大生成token数
            
        Returns:
            dict: API响应
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False
            )
            return response
        except Exception as e:
            raise Exception(f'DeepSeek API请求失败: {str(e)}')
    
    def generate_concept_explanation(self, concept):
        """生成概念解释
        
        Args:
            concept: 概念名称
            
        Returns:
            dict: 概念解释
        """
        messages = [
            {
                'role': 'system',
                'content': '你是一个专业的教育专家，擅长用通俗易懂的方式解释复杂的概念。'
            },
            {
                'role': 'user',
                'content': f'请用以下三种方式解释"{concept}"这个概念：\n1. 核心定义\n2. 用费曼技巧解释\n3. 列出3个常见的误解'
            }
        ]
        
        try:
            response = self.chat_completion(messages)
            content = response.choices[0].message.content
            
            # 解析响应内容
            parts = content.split('\n\n')
            explanation = {
                'core_definition': parts[0].replace('1. 核心定义\n', ''),
                'feynman_explanation': parts[1].replace('2. 用费曼技巧解释\n', ''),
                'misconceptions': parts[2].replace('3. 列出3个常见的误解\n', '').split('\n')
            }
            
            return explanation
        except Exception as e:
            raise Exception(f'生成概念解释失败: {str(e)}')
    
    def generate_exercises(self, concept, difficulty='medium'):
        """生成练习题
        
        Args:
            concept: 概念名称
            difficulty: 难度级别
            
        Returns:
            dict: 练习题
        """
        messages = [
            {
                'role': 'system',
                'content': '你是一个专业的教育专家，擅长设计练习题。'
            },
            {
                'role': 'user',
                'content': f'请为"{concept}"这个概念生成{difficulty}难度的练习题，包括：\n1. 2道判断题\n2. 1个案例分析\n3. 1道编程题'
            }
        ]
        
        try:
            response = self.chat_completion(messages)
            content = response.choices[0].message.content
            
            # 解析响应内容
            parts = content.split('\n\n')
            exercises = {
                'true_false': self._parse_true_false(parts[0]),
                'case_studies': self._parse_case_studies(parts[1]),
                'code_exercises': self._parse_code_exercises(parts[2])
            }
            
            return exercises
        except Exception as e:
            raise Exception(f'生成练习题失败: {str(e)}')
    
    def _parse_true_false(self, content):
        """解析判断题"""
        questions = []
        lines = content.replace('1. 判断题\n', '').split('\n')
        
        for line in lines:
            if line.strip():
                question = line.strip()
                answer = '正确' in question
                questions.append({
                    'question': question,
                    'answer': answer,
                    'explanation': f'解释为什么这个说法{"正确" if answer else "错误"}'
                })
        
        return questions
    
    def _parse_case_studies(self, content):
        """解析案例分析"""
        content = content.replace('2. 案例分析\n', '')
        parts = content.split('\n问题：')
        
        return [{
            'scenario': parts[0].strip(),
            'questions': parts[1].split('\n'),
            'answers': ['答案1', '答案2']  # 实际应用中应该从API响应中获取
        }]
    
    def _parse_code_exercises(self, content):
        """解析编程题"""
        content = content.replace('3. 编程题\n', '')
        parts = content.split('\n提示：')
        
        return [{
            'description': parts[0].strip(),
            'template': 'def solution():\n    # 在这里编写代码\n    pass',
            'solution': 'def solution():\n    # 解决方案\n    return result',
            'hints': parts[1].split('\n') if len(parts) > 1 else []
        }] 