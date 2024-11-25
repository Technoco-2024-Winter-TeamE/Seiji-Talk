from app.models.model import db, Question,Mode,Answer,RelatedWord,Reference,Status,User
class UnkoRepository:
    def __init__(self):
        pass

class SeijiTalkRepository:
    @staticmethod
    def add_user_if_not_exists(user_info: dict) -> User:
        """
        ユーザー情報をチェックし、初回の場合はDBに登録する。

        Args:
            user_info (dict): Google認証から取得したユーザー情報。

        Returns:
            User: 登録された、または既存のユーザーオブジェクト。
        """
        email = user_info.get("email")
        if not email:
            raise ValueError("User info must contain an email")

        # ユーザーが既に存在するか確認
        existing_user = SeijiTalkRepository.find_user_by_email(email)
        if existing_user:
            print(f"User {email} already exists.")
            return existing_user

        # 新規ユーザーを作成
        new_user = User(
            id=user_info.get("id"),
            email=email,
            name=user_info.get("name")
        )
        db.session.add(new_user)
        db.session.commit()
        print(f"User {email} added to the database.")
        return new_user

# class UnkoRepository:
#     """
#     UnkoRepositoryクラス
#     うんこモデルに対するCRUD操作や関連データの取得を提供するリポジトリクラス。
#     """

#     @staticmethod
#     def get_unkos() -> list[dict]:
#         """
#         すべてのうんこデータを取得します。

#         Returns:
#             list[dict]: すべてのうんこオブジェクトを辞書形式にしたリスト。
#         """
#         unkos = Unko.query.all()
#         return [unko.to_dict() for unko in unkos]
    
#     @staticmethod
#     def get_unko(unko_id: int) -> dict:
#         """
#         特定のうんこデータをIDで取得します。

#         Args:
#             unko_id (int): 取得したいうんこオブジェクトのID。

#         Returns:
#             dict: 指定したIDに対応するうんこオブジェクトの辞書。
#         """
#         unko = Unko.query.filter(Unko.id == unko_id).first()
#         if unko is None:
#             return None  # データが存在しない場合はNoneを返す
#         return unko.to_dict()

#     @staticmethod
#     def create_unko(unko_name: str, color_id: int, size_id: int) -> dict:
#         """
#         新しいうんこデータを作成します。

#         Args:
#             unko_name (str): 作成するうんこの名前。
#             color_id (int): 関連付ける色のID。
#             size_id (int): 関連付けるサイズのID。

#         Returns:
#             dict: 作成されたうんこオブジェクトの辞書。

#         Raises:
#             Exception: データベース操作中にエラーが発生した場合。
#         """
#         try:
#             new_unko = Unko(name=unko_name, color_id=color_id, size_id=size_id)
#             db.session.add(new_unko)
#             db.session.commit()
#             return new_unko.to_dict()
#         except Exception as e:
#             db.session.rollback()
#             raise e
        
#     @staticmethod
#     def get_colors() -> list[dict]:
#         """
#         すべての色データを取得します。

#         Returns:
#             list[dict]: すべての色オブジェクトを辞書形式にしたリスト。
#         """
#         colors = Color.query.all()
#         return [color.to_dict() for color in colors]

#     @staticmethod
#     def get_sizes() -> list[dict]:
#         """
#         すべてのサイズデータを取得します。

#         Returns:
#             list[dict]: すべてのサイズオブジェクトを辞書形式にしたリスト。
#         """
#         sizes = Size.query.all()
#         return [size.to_dict() for size in sizes]