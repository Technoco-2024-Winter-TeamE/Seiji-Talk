#アプリケーションの設定ファイル

import os
from dotenv import load_dotenv



#現在のファイル（config.py）があるディレクトリの絶対パスを取得
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Flaskの設定定数をまとめたクラスです。
    """

    # .envファイルを読み込む
    load_dotenv()

    #SQLiteデータベースの接続先を指定

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    
    #データベースの変更追跡機能を無効
    SQLALCHEMY_TRACK_MODIFICATIONS = False
