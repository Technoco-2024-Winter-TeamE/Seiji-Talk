#アプリケーションの設定ファイル

import os

#現在のファイル（config.py）があるディレクトリの絶対パスを取得
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Flaskの設定定数をまとめたクラスです。
    """
    #SQLiteデータベースの接続先を指定(root,password,データベース名は随時変更してください！)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/Seiji_talk'
    
    
    #データベースの変更追跡機能を無効
    SQLALCHEMY_TRACK_MODIFICATIONS = False
