from app import db
from sqlalchemy.orm import Mapped

class Unko(db.Model):
    """
    Unkoクラス
    このクラスは`unkos`テーブルを表現します。
    """

    __tablename__ = 'unkos'
    """テーブル名:unkos"""

    id: int = db.Column(db.Integer, primary_key=True)
    """うんこID"""
    name: str = db.Column(db.String(128), nullable=False)
    """うんこの名前"""
    color_id: int = db.Column(db.Integer, db.ForeignKey('colors.id'), nullable=False)
    """色ID（colorsテーブルのidと紐づけ）"""
    size_id: int = db.Column(db.Integer, db.ForeignKey('sizes.id'), nullable=False)
    """サイズID(sizesテーブルのidと紐づけ)"""
    
    color: Mapped['Color'] = db.relationship('Color', back_populates='unkos')
    """色"""
    size: Mapped['Size'] = db.relationship('Size', back_populates='unkos')
    """サイズ"""

    def to_dict(self) -> dict:
        """
        モデルを辞書形式に変換します。

        Returns:
            dict: モデルの属性をキーとする辞書。
        """
        return {
            'id': self.id,
            'name': self.name,
            'color_id': self.color_id,
            'size_id': self.size_id,
            'color': self.color.to_dict(),
            'size': self.size.to_dict()
        }



class Color(db.Model):
    """
    色クラス
    このクラスは`colors`テーブルを表現します。
    """
    __tablename__ = 'colors'
    
    id : int = db.Column(db.Integer, primary_key=True)
    """色ID"""
    name : str = db.Column(db.String(128), nullable=False)
    """色の名前"""
    
    unkos : Mapped[list['Unko']] = db.relationship('Unko', back_populates='color')

    def to_dict(self) -> dict:
        """
        モデルを辞書形式に変換します。

        Returns:
            dict: モデルの属性をキーとする辞書。
        """
        return {
            'id': self.id,
            'name': self.name
        }


class Size(db.Model):
    """
    大きさクラス
    このクラスは`sizes`テーブルを表現します。
    """
    __tablename__ = 'sizes'
    
    id : int = db.Column(db.Integer, primary_key=True)
    """大きさID"""
    name : str = db.Column(db.String(128), nullable=False)
    """大きさの名前"""
    
    unkos : Mapped[list['Unko']] = db.relationship('Unko', back_populates='size')

    def to_dict(self) -> dict:
        """
        モデルを辞書形式に変換します。

        Returns:
            dict: モデルの属性をキーとする辞書。
        """
        return {
            'id': self.id,
            'name': self.name
        }
