import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    # OpenAI配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = 'gpt-4'

    # DeepSeek API配置
    DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
    DEEPSEEK_API_BASE = os.environ.get('DEEPSEEK_API_BASE', 'https://api.deepseek.com')
    DEEPSEEK_MODEL = os.environ.get('DEEPSEEK_MODEL', 'deepseek-chat')

    # Neo4j配置
    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')

    # Redis配置
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'

    # 应用配置
    CONCEPT_EXPLANATION_TEMPLATE = """
    请从以下三个角度解释{concept}：
    1. 核心定义
    2. 费曼解释（用简单的类比）
    3. 常见误解
    """

    # 记忆系统配置
    MEMORY_INTERVALS = [1, 3, 7, 14, 30]  # 复习间隔（天）
    MEMORY_STRENGTH_THRESHOLD = 0.8  # 记忆强度阈值

    # 知识图谱配置
    MAX_RELATED_CONCEPTS = 5  # 每个概念最多显示的相关概念数
    GRAPH_DEPTH = 2  # 知识图谱展开深度

    # 文件上传配置
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    NEO4J_URI = 'bolt://localhost:7687/test'
    REDIS_URL = 'redis://localhost:6379/1'

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 