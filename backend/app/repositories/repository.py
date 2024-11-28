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
        try:
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

        except Exception as e:
            # エラー発生時にロールバック
            db.session.rollback()
            print(f"Error occurred while adding user: {e}")
            raise

    

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
    def save_latest_answer(question: Question, result_data: dict):
        """
        質問に対する回答と関連情報を保存し、ステータスを更新する。

        Args:
            question (Question): 回答対象の質問オブジェクト。
            result_data (dict): 回答と詳細情報を含む辞書。
                {
                    "answer": {
                        "message": str,  # 全体の要約結果
                        "references": [
                            {
                                "title": str,  # 参考記事のタイトル
                                "url": str     # 参考記事のURL
                            },
                            ...
                        ]
                    }
                }

        Returns:
            Answer: 登録された回答オブジェクト。
        """
        try:
            # 辞書からデータを抽出
            answer_message = result_data.get("answer", {}).get("message")
            references = result_data.get("answer", {}).get("references", [])

            if not answer_message:
                raise ValueError("Answer message is missing in result_data.")
            
            # 新しい回答を登録
            new_answer = Answer(
                question_id=question.id,
                message=answer_message
            )
            db.session.add(new_answer)

            # 参考記事を登録
            for reference in references:
                new_reference = Reference(
                    answer=new_answer,
                    title=reference.get("title"),
                    url=reference.get("url")
                )
                db.session.add(new_reference)

            # 質問のステータスをSUCCESSに更新
            success_status = Status.query.filter_by(name="SUCCESS").first()
            if not success_status:
                raise ValueError("Default status 'SUCCESS' not found.")
            question.status_id = success_status.id

            # コミットして保存
            db.session.commit()
            print(f"Answer for Question {question.id} saved successfully.")
            return new_answer

        except Exception as e:
            # エラー発生時にロールバック
            db.session.rollback()
            print(f"Error occurred while saving answer and references: {e}")
            raise

    @staticmethod
    def save_word_answer(question: Question, result_data: dict):
        """
        質問に対する回答を保存し、関連語を登録し、ステータスをSUCCESSに変更する。

        Args:
            question (Question): 回答対象の質問オブジェクト。
            result_data (dict): 回答と関連語を含む辞書。
                {
                    "message": "回答内容",
                    "related_words": ["関連語1", "関連語2", ...]
                }

        Returns:
            Answer: 登録された回答オブジェクト。
        """
        try:
            # 必要なデータを取得
            answer_message = result_data.get("message")
            related_words = result_data.get("related_words", [])

            if not answer_message:
                raise ValueError("Answer message is missing in result_data.")
            if not isinstance(related_words, list):
                raise ValueError("Related words must be a list.")

            # 新しい回答を登録
            new_answer = Answer(
                question_id=question.id,
                message=answer_message
            )
            db.session.add(new_answer)

            # 関連語を登録
            for word in related_words:
                new_related_word = RelatedWord(
                    answer=new_answer,
                    related_word=word
                )
                db.session.add(new_related_word)

            # 質問のステータスをSUCCESSに更新
            success_status = Status.query.filter_by(name="SUCCESS").first()
            if not success_status:
                raise ValueError("Default status 'SUCCESS' not found.")
            question.status_id = success_status.id

            # コミットして保存
            db.session.commit()
            print(f"Answer and related words for Question {question.id} saved successfully.")
            return new_answer

        except Exception as e:
            # エラー発生時にロールバック
            db.session.rollback()
            print(f"Error occurred while saving answer and related words: {e}")
            raise