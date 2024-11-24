from app.models.unko import Unko, Color, Size
from app import db  #db = SQLAlchemy()のdbインスタンス

def register_first_unko():
    """
    初期データを登録します。
    """
    if Color.query.count() == 0:
        colors = [Color(name='brown'),Color(name='gold'),Color(name='rainbow'),Color(name='silver')]
        db.session.add_all(colors)
        db.session.commit()
        print("The initial Colors registration process for the Unko DB has been done.")
    else:
        print("Colors have already been registered in the Unko DB.")
        
    if Size.query.count() == 0:
        sizes = [Size(name='large'),Size(name='medium'),Size(name='small')]
        db.session.add_all(sizes)
        db.session.commit()
        print("The initial Sizes registration process for the Unko DB has been done.")
    else:
        print("Sizes have already been registered in the Unko DB.")

    if Unko.query.count() == 0:
        default_color = Color.query.first()  
        default_size = Size.query.first()  
        default_unko = Unko(name='デフォルトのうんこ', color=default_color, size=default_size)
        db.session.add(default_unko)
        db.session.commit()
        print("The initial Unkos registration process for the Unko DB has been done.")
    else:
        print("Unkos have already been registered in the Unko DB.")
