from app.models.model import db, Question,Mode,Answer,RelatedWord,Reference,Status,User
class UnkoRepository:
    def __init__(self):
        pass

class SeijiTalkRepository:
    """
    データベース操作を管理するリポジトリクラス
    """

    @staticmethod
    def find_user_by_id(user_id: str) -> User:
        """
        ユーザーIDでユーザーを検索する。

        Args:
            user_id (str): 検索するユーザーID。

        Returns:
            User: 見つかったユーザーオブジェクト、または None。
        """
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def add_user_if_not_exists(user_info: dict) -> User:
        """
        ユーザー情報をチェックし、初回の場合はDBに登録する。

        Args:
            user_info (dict): Google認証から取得したユーザー情報。

        Returns:
            User: 登録された、または既存のユーザーオブジェクト。
        """
        user_id = user_info.get("id")
        if not user_id:
            raise ValueError("User info must contain an ID")

        # ユーザーが既に存在するか確認
        existing_user = SeijiTalkRepository.find_user_by_id(user_id)
        if existing_user:
            print(f"User {user_id} already exists.")
            return existing_user

        # 新規ユーザーを作成
        new_user = User(
            id=user_id,
            email=user_info.get("email"),
            name=user_info.get("name")
        )
        db.session.add(new_user)
        db.session.commit()
        print(f"User {user_id} added to the database.")
        return new_user