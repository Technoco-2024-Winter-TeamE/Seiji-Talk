from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()   #データベース操作のツールを準備（定義）
migrate = Migrate() #データベース構造の変更を管理（変更）

def create_app():
    app = Flask(__name__)   #Flaskアプリケーションのインスタンスを作成
    app.config.from_object(Config)  #Configクラスの設定をFlaskアプリケーションに適用
    
    db.init_app(app)  #Flaskアプリとデータベースを接続
    migrate.init_app(app,db)    #スキーマ変更の管理を接続

    first_request_handled = False #リクエスト前かどうかのフラグ
    @app.before_request
    def before_first_request():
        nonlocal first_request_handled  #グローバル変数を関数内で使うときの宣言
        if not first_request_handled:
            from app.seeds_unko import register_first_unko  #初期処理として最初のうんこを登録
            register_first_unko()
            first_request_handled = True    

    from app.routes.routes import bp as api_bp  
    app.register_blueprint(api_bp, url_prefix='/api')  

    return app

