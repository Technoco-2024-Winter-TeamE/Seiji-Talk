from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
import secrets
import os

db = SQLAlchemy()   #データベース操作のツールを準備（定義）
migrate = Migrate() #データベース構造の変更を管理（変更）

def create_app():
    app = Flask(__name__)   #Flaskアプリケーションのインスタンスを作成
    app.config.from_object(Config)  #Configクラスの設定をFlaskアプリケーションに適用
    
    db.init_app(app)  #Flaskアプリとデータベースを接続
    migrate.init_app(app,db)    #スキーマ変更の管理を接続
    
    # secret_keyを設定（環境変数から取得、なければランダムなキーを生成）
    app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(16))

    first_request_handled = False #最初期のリクエスト前かどうかのフラグ

    @app.before_request
    def before_first_request():
        nonlocal first_request_handled  #グローバル変数を関数内で使うときの宣言
        if not first_request_handled:
            from app.seeds import register_master_data  #初期処理としてマスタデータを登録
            register_master_data()
            first_request_handled = True    

    from app.routes.qa_controller import question_bp
    from app.routes.auth_controller import auth_bp 
    app.register_blueprint(question_bp, url_prefix='/api/questions')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')  

    return app

