from flask import Blueprint, jsonify, request
from app.services.concept_service import ConceptService
from app.services.learning_service import LearningService
from app.services.memory_service import MemoryService

api_bp = Blueprint('api', __name__)
concept_service = ConceptService()
learning_service = LearningService()
memory_service = MemoryService()

# 概念相关API
@api_bp.route('/concept/search', methods=['GET'])
def search_concept():
    """搜索概念"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': '搜索关键词不能为空'}), 400
    
    try:
        results = concept_service.search_concept(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/concept/<concept_name>', methods=['GET'])
def get_concept(concept_name):
    """获取概念详情"""
    try:
        concept = concept_service.get_concept(concept_name)
        return jsonify(concept)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/concept/<concept_name>/explanation', methods=['GET'])
def get_concept_explanation(concept_name):
    """获取概念解释"""
    try:
        explanation = concept_service.get_concept_explanation(concept_name)
        return jsonify(explanation)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/concept/<concept_name>/exercises', methods=['GET'])
def get_concept_exercises(concept_name):
    """获取概念练习题"""
    try:
        exercises = concept_service.get_concept_exercises(concept_name)
        return jsonify(exercises)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/concept/<concept_name>/knowledge-graph', methods=['GET'])
def get_concept_knowledge_graph(concept_name):
    """获取概念知识图谱"""
    try:
        knowledge_graph = concept_service.get_concept_knowledge_graph(concept_name)
        return jsonify(knowledge_graph)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 学习路径相关API
@api_bp.route('/learning/path', methods=['POST'])
def generate_learning_path():
    """生成学习路径"""
    data = request.json
    concept = data.get('concept')
    user_level = data.get('user_level', 'beginner')
    
    if not concept:
        return jsonify({'error': '概念名称不能为空'}), 400
    
    try:
        learning_path = learning_service.generate_learning_path(concept, user_level)
        return jsonify(learning_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 记忆管理相关API
@api_bp.route('/memory/review', methods=['GET'])
def get_review_schedule():
    """获取复习计划"""
    user_id = request.args.get('user_id', '1')
    
    try:
        schedule = memory_service.get_review_schedule(user_id)
        return jsonify(schedule)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/memory/review/start', methods=['POST'])
def start_review():
    """开始复习"""
    data = request.json
    concept = data.get('concept')
    user_id = data.get('user_id', '1')
    
    if not concept:
        return jsonify({'error': '概念名称不能为空'}), 400
    
    try:
        result = memory_service.start_review(user_id, concept)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/memory/review/skip', methods=['POST'])
def skip_review():
    """跳过复习"""
    data = request.json
    concept = data.get('concept')
    user_id = data.get('user_id', '1')
    
    if not concept:
        return jsonify({'error': '概念名称不能为空'}), 400
    
    try:
        result = memory_service.skip_review(user_id, concept)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/memory/stats', methods=['GET'])
def get_learning_stats():
    """获取学习统计"""
    user_id = request.args.get('user_id', '1')
    
    try:
        stats = memory_service.get_learning_stats(user_id)
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/memory/strength', methods=['GET'])
def get_memory_strength():
    """获取记忆强度"""
    user_id = request.args.get('user_id', '1')
    
    try:
        strength_data = memory_service.get_memory_strength(user_id)
        return jsonify(strength_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 