from flask import Blueprint, jsonify, request
from app.repositories.repository import SeijiTalkRepository
from app.services.google_auth_service import fetch_user_info

question_bp = Blueprint('api/questions', __name__)


def get_user_info_from_request():
    """
    リクエストヘッダーからアクセストークンを取得し、Googleユーザー情報を取得する。

    Returns:
        tuple:
            - 成功時: ユーザー情報の辞書（dict）、HTTPステータスコード200。
            - 失敗時: エラーメッセージの辞書（dict）、対応するHTTPステータスコード。
    """
    # リクエストヘッダーからアクセストークンを取得
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return {"error": "Authorization header missing"}, 401
    if not auth_header.startswith('Bearer '):
        return {"error": "Authorization header invalid format"}, 401

    # "Bearer " 部分を取り除く
    access_token = auth_header.split(" ")[1]

    # アクセストークンを検証してユーザー情報を取得
    try:
        user_info, error = fetch_user_info(access_token)
        if error:
            return {"error": "Invalid token", "details": error}, 403
    except Exception as e:
        return {"error": "Failed to fetch user info", "details": str(e)}, 500

    # 必須フィールドを検証
    user_id = user_info.get("id")
    if not user_id:
        return {"error": "User ID not found in Google response"}, 500

    # 必要なら追加フィールドも検証可能
    return user_info, 200


@question_bp.route('', methods=['POST'])
def create_question():
    """
    質問を登録するエンドポイント。
    非同期処理のステータスとして 202 Accepted を返し、質問はデータベースに保存します。
    """
    try:
        # ユーザー情報の取得
        user_info, status_code = get_user_info_from_request()
        if status_code != 200:
            return jsonify(user_info), status_code

        # ユーザー情報を確認し、なければデータベースに登録
        user = SeijiTalkRepository.get_or_add_user(user_info)

        # リクエストデータの検証
        data = request.get_json()
        if not data or "message" not in data or "mode" not in data:
            return jsonify({"error": "Invalid request body"}), 400

        # 質問を登録
        new_question = SeijiTalkRepository.create_question(
            user_id=user.id,
            message=data["message"],
            mode_name=data["mode"]
        )

        # 質問IDを返却（非同期ステータス）
        return jsonify({
            "question_id": new_question.id,
            "mode": new_question.mode.name,
            "state": "PENDING"
        }), 202

    except ValueError as e:
        # バリデーションエラー
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # 予期せぬエラーをキャッチ
        return jsonify({"error": str(e)}), 500
    

# @bp.route('/unkos', methods=['GET'])
# def get_all_unkos():
#     try:
#         unkos = UnkoRepository.get_unkos()
#         unkos_list = [unko for unko in unkos]
#         return jsonify(unkos_list), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @bp.route('/unko/<int:id>', methods=['GET'])
# def get_unko_by_id(id):
#     """
#     特定のIDに対応するうんこデータを取得するエンドポイント。

#     Args:
#         id (int): URLから渡されるうんこID。

#     Returns:
#         Response: 指定したIDのうんこデータをJSON形式で返す。
#                   もしIDが見つからなければ404エラーを返す。
#     """
#     try:
#         # UnkoRepositoryのget_unkoメソッドを使って特定のうんこを取得
#         unko_data = UnkoRepository.get_unko(id)
#         if unko_data:  # データが存在する場合
#             return jsonify(unko_data), 200
#         else:  # データが存在しない場合
#             return jsonify({"error": "Unko not found"}), 404
#     except Exception as e:  # 予期せぬエラーが発生した
#         return jsonify({"error": str(e)}), 500
    
# @bp.route('/unko', methods=['POST'])
# def create_new_unko():
    
#     """
#     新しいうんこデータを作成するエンドポイント。
#     """
#     try:
#         # リクエストボディからデータを取得
#         data = request.get_json()

#         # 必要なキーが揃っているか確認
#         if not all(k in data for k in ("name", "color_id", "size_id")):
#             return jsonify({"error": "Invalid input data"}), 400

#         # UnkoRepository の create_unko メソッドを呼び出してデータを作成
#         new_unko = UnkoRepository.create_unko(
#             unko_name=data["name"],
#             color_id=data["color_id"],
#             size_id=data["size_id"]
#         )
#         return jsonify(new_unko), 201  # 成功時に201 Createdを返す

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500  # エラー発生時に500を返す