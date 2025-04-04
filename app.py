from flask import Flask, render_template, jsonify, request
from config import config
import os

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 确保实例文件夹存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 注册蓝图
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # 前端路由
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/learning-path')
    def learning_path():
        return render_template('learning_path.html')

    @app.route('/review')
    def review():
        return render_template('review.html')

    # 注册错误处理
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_CONFIG', 'default'))
    app.run(host='0.0.0.0', port=5000) 