from app.models.model import db, Question,Mode,Answer,RelatedWord,Reference,Status,User

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
    def get_or_add_user(user_info: dict) -> User:
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
    

    @staticmethod
    def create_question(user_id: str, message: str, mode_name: str) -> Question:
        """
        質問をデータベースに登録する。

        Args:
            user_id (str): 登録するユーザーID。
            message (str): 質問内容。
            mode_name (str): モード名。

        Returns:
            Question: 登録された質問オブジェクト。
        """
        # モードを取得
        mode = Mode.query.filter_by(name=mode_name).first()
        if not mode:
            raise ValueError(f"Mode '{mode_name}' not found.")

        # ステータスをデフォルトで「PENDING」に設定
        status = Status.query.filter_by(name="PENDING").first()
        if not status:
            raise ValueError("Default status 'PENDING' not found.")

        # 質問の重複チェック
        existing_question = Question.query.filter_by(
            user_id=user_id,
            message=message,
            mode_id=mode.id
        ).first()
        
        if existing_question:
            print(f"Question already exists: {existing_question.id}")
            return existing_question

        # 新しい質問を登録
        new_question = Question(
            message=message,
            user_id=user_id,
            status_id=status.id,
            mode_id=mode.id
        )
        db.session.add(new_question)
        db.session.commit()
        print(f"Question {new_question.id} added to the database.")
        return new_question

        
    @staticmethod
    def create_answer_with_associations(question_id: str, message: str, data: dict) -> Answer:
        """
        質問のモードに応じて回答を作成し、関連語または参考記事を登録する。

        Args:
            question_id (str): 対象の質問ID。
            message (str): 回答内容。
            data (dict): 関連語や参考記事データ。
                         - "related_words" (list[str]): Modeが"word"の場合に登録する関連語。
                         - "references" (list[dict]): Modeが"latest"の場合に登録する参考記事。

        Returns:
            Answer: 登録された回答オブジェクト。
        """
        # 質問を取得
        question = Question.query.filter_by(id=question_id).first()
        if not question:
            raise ValueError(f"Question with ID '{question_id}' not found.")

        # 回答を作成
        new_answer = Answer(
            question_id=question_id,
            message=message
        )
        db.session.add(new_answer)
        db.session.commit()

        # モードに応じた関連付けを実施
        mode_name = question.mode.name
        if mode_name == "word":
            related_words = data.get("related_words", [])
            for word in related_words:
                related_word = RelatedWord(
                    answer_id=new_answer.id,
                    related_word=word
                )
                db.session.add(related_word)

        elif mode_name == "latest":
            references = data.get("references", [])
            for ref in references:
                reference = Reference(
                    answer_id=new_answer.id,
                    title=ref.get("title"),
                    url=ref.get("url")
                )
                db.session.add(reference)

        db.session.commit()
        return new_answer
        