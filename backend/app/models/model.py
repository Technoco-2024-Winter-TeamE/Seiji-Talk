from app import db
from sqlalchemy.orm import Mapped
import uuid
from sqlalchemy.dialects.mysql import CHAR

class Question(db.Model):
    """
    質問クラス
    """
    __tablename__ = 'questions'

    id: str = db.Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    """質問ID"""
    message: str = db.Column(db.String(255), nullable=False)
    """質問内容"""
    user_id: str = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    """ユーザーID"""
    status_id: int = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=False)
    """ステータスID"""
    mode_id: int = db.Column(db.Integer, db.ForeignKey('modes.id'), nullable=False)
    """モードID"""
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    """更新日時"""
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    """作成日時"""

    user: Mapped['User'] = db.relationship('User', back_populates='questions')
    status: Mapped['Status'] = db.relationship('Status', back_populates='questions')
    mode: Mapped['Mode'] = db.relationship('Mode', back_populates='questions')
    answers: Mapped[list['Answer']] = db.relationship('Answer', back_populates='question')

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'message': self.message,
            'user_id': self.user_id,
            'status_id': self.status_id,
            'mode_id': self.mode_id,
            'updated_at': self.updated_at,
            'created_at': self.created_at
        }

class User(db.Model):
    """
    ユーザークラス
    """
    __tablename__ = 'users'

    id: str = db.Column(db.String(255), primary_key=True)  # GoogleのIDを保存
    """ユーザーID"""
    email: str = db.Column(db.String(255), unique=True, nullable=False)
    """メールアドレス"""
    name: str = db.Column(db.String(100), nullable=False)
    """名前"""

    questions: Mapped[list['Question']] = db.relationship('Question', back_populates='user')

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name
        }





class Mode(db.Model):
    """
    モードクラス
    """
    __tablename__ = 'modes'

    id: int = db.Column(db.Integer, primary_key=True)
    """モードID"""
    name: str = db.Column(db.String(100), nullable=False)
    """モード名"""

    questions: Mapped[list['Question']] = db.relationship('Question', back_populates='mode')

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }


class Status(db.Model):
    """
    ステータスクラス
    """
    __tablename__ = 'statuses'

    id: int = db.Column(db.Integer, primary_key=True)
    """ステータスID"""
    name: str = db.Column(db.String(100), nullable=False)
    """ステータス名"""

    questions: Mapped[list['Question']] = db.relationship('Question', back_populates='status')

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }


class Answer(db.Model):
    """
    回答クラス
    """
    __tablename__ = 'answers'

    id: int = db.Column(db.Integer, primary_key=True)
    """回答ID"""
    question_id: str = db.Column(CHAR(36), db.ForeignKey('questions.id'), unique=True, nullable=False)
    """質問ID"""
    message: str = db.Column(db.String(255), nullable=False)
    """回答内容"""
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    """作成日時"""

    question: Mapped['Question'] = db.relationship('Question', back_populates='answers')

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'question_id': self.question_id,
            'message': self.message,
            'created_at': self.created_at
        }