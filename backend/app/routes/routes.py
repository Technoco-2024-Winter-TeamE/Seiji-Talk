from flask import Blueprint, jsonify, request
from app.repositories.repository import UnkoRepository  

bp = Blueprint('api', __name__)

@bp.route('/unkos', methods=['GET'])
def get_all_unkos():
    try:
        unkos = UnkoRepository.get_unkos()
        unkos_list = [unko for unko in unkos]
        return jsonify(unkos_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/unko/<int:id>', methods=['GET'])
def get_unko_by_id(id):
    """
    特定のIDに対応するうんこデータを取得するエンドポイント。

    Args:
        id (int): URLから渡されるうんこID。

    Returns:
        Response: 指定したIDのうんこデータをJSON形式で返す。
                  もしIDが見つからなければ404エラーを返す。
    """
    try:
        # UnkoRepositoryのget_unkoメソッドを使って特定のうんこを取得
        unko_data = UnkoRepository.get_unko(id)
        if unko_data:  # データが存在する場合
            return jsonify(unko_data), 200
        else:  # データが存在しない場合
            return jsonify({"error": "Unko not found"}), 404
    except Exception as e:  # 予期せぬエラーが発生した
        return jsonify({"error": str(e)}), 500
    
@bp.route('/unko', methods=['POST'])
def create_new_unko():
    
    """
    新しいうんこデータを作成するエンドポイント。
    """
    try:
        # リクエストボディからデータを取得
        data = request.get_json()

        # 必要なキーが揃っているか確認
        if not all(k in data for k in ("name", "color_id", "size_id")):
            return jsonify({"error": "Invalid input data"}), 400

        # UnkoRepository の create_unko メソッドを呼び出してデータを作成
        new_unko = UnkoRepository.create_unko(
            unko_name=data["name"],
            color_id=data["color_id"],
            size_id=data["size_id"]
        )
        return jsonify(new_unko), 201  # 成功時に201 Createdを返す

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # エラー発生時に500を返す