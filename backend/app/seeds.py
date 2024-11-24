from app.models.model import Status, Mode
from app import db  # db = SQLAlchemy()のインスタンス

def initialize_master_data():
    """
    マスタテーブルの初期データを登録します。
    """
    # ステータスマスタの初期化
    if Status.query.count() == 0:
        statuses = [
            Status(id=1, name="未回答"),
            Status(id=2, name="回答中"),
            Status(id=3, name="完了")
        ]
        db.session.add_all(statuses)
        db.session.commit()
        print("The initial Status registration process for the DB has been done.")
    else:
        print("Statuses have already been registered in the DB.")

    # モードマスタの初期化
    if Mode.query.count() == 0:
        modes = [
            Mode(id=1, name="簡単"),
            Mode(id=2, name="標準"),
            Mode(id=3, name="高度")
        ]
        db.session.add_all(modes)
        db.session.commit()
        print("The initial Modes registration process for the DB has been done.")
    else:
        print("Modes have already been registered in the DB.")