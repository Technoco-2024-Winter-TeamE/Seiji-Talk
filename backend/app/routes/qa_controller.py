from flask import Blueprint, jsonify, request, make_response
from app.repositories.repository import SeijiTalkRepository
from app.services.google_auth_service import fetch_user_info
from app.services.question_service import process_question
from app.models.model import Question, Status, Answer, RelatedWord, Reference
import asyncio
import threading

question_bp = Blueprint("question_bp", __name__)


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


def validate_user_and_get(user_info_function):
    """
    リクエストからユーザー情報を取得し、検証してデータベースに登録または取得する。

    Args:
        user_info_function (function): ユーザー情報を取得する関数（例: get_user_info_from_request）

    Returns:
        tuple:
            - user: ユーザーオブジェクト (成功時)
            - error_response: エラーがあればJSONレスポンスオブジェクト (失敗時)
            - status_code: HTTPステータスコード
    """
    try:
        # ユーザー情報の取得
        user_info, status_code = user_info_function()
        if status_code != 200:
            return None, jsonify(user_info), status_code

        # ユーザー情報を確認し、存在しなければ登録
        user = SeijiTalkRepository.get_or_add_user(user_info)
        return user, None, 200

    except Exception as e:
        return None, jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500

def run_async_task(async_func, *args):
    """
    非同期関数をスレッド内で実行するヘルパー関数。
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_func(*args))
    loop.close()

@question_bp.route('', methods=['POST'])
def create_question():
    """
    質問を登録するエンドポイント。
    非同期処理のステータスとして 202 Accepted を返し、質問はデータベースに保存します。
    """
    try:
        # ユーザー情報の検証と取得
        user, error_response, status_code = validate_user_and_get(get_user_info_from_request)
        if error_response:
            return error_response, status_code
        
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

        # 非同期タスクをスレッドで実行
        process_question(new_question.id)
        
        # 質問IDを返却（非同期ステータス）
        return jsonify({
            "question_id": new_question.id,
            "mode": new_question.mode.name,
            "state": new_question.status.name
        }), 202


    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@question_bp.route('/<string:question_id>', methods=['GET'])
def get_question_answer(question_id):
    """
    質問の回答を取得するエンドポイント。

    Args:
        question_id (str): 質問ID。

    Returns:
        JSON: 質問の回答に応じたレスポンス。
    """
    try:

        # ユーザー情報の検証と取得
        user, error_response, status_code = validate_user_and_get(get_user_info_from_request)
        if error_response:
            return error_response, status_code

        # 質問を取得
        question = Question.query.filter_by(id=question_id).first()
        if not question:
            return make_response(jsonify({"error": f"Question with ID '{question_id}' not found."}), 404)

        # 質問のモードを取得
        mode = question.mode.name
        state = question.status.name

        # PENDING 状態の場合
        if state == "PENDING":
            return make_response(
                jsonify({
                    "question_id": question.id,
                    "mode": mode,
                    "state": state,
                }), 202
            )

        # FAILURE 状態の場合
        if state == "FAILURE":
            return make_response(
                jsonify({
                    "question_id": question.id,
                    "mode": mode,
                    "state": state,
                }), 500
            )

        # SUCCESS 状態の場合
        answer = Answer.query.filter_by(question_id=question.id).first()
        if not answer:
            return make_response(jsonify({"error": "Answer not found for SUCCESS state."}), 500)

        # 用語モードの場合
        if mode == "word":
            related_words = [rw.related_word for rw in RelatedWord.query.filter_by(answer_id=answer.id).all()]
            return make_response(
                jsonify({
                    "question_id": question.id,
                    "mode": mode,
                    "state": state,
                    "answer": {
                        "message": answer.message,
                        "related_words": related_words
                    }
                }), 200
            )

        # 最新情報モードの場合
        if mode == "latest":
            references = [{"title": ref.title, "url": ref.url} for ref in Reference.query.filter_by(answer_id=answer.id).all()]
            return make_response(
                jsonify({
                    "question_id": question.id,
                    "mode": mode,
                    "state": state,
                    "answer": {
                        "message": answer.message,
                        "references": references
                    }
                }), 200
            )

        # モードが未知の場合
        return make_response(jsonify({"error": f"Unknown mode '{mode}'."}), 400)

    except Exception as e:
        return make_response(
            jsonify({
                "error": "An error occurred while processing the request.",
                "details": str(e)
            }), 500
        )

@question_bp.route('/history', methods=['GET'])
def get_question_history():
    """
    質問履歴を取得するエンドポイント。

    Returns:
        JSON: 質問履歴とその回答情報。
    """
    try:
        # ユーザー情報の検証と取得
        user, error_response, status_code = validate_user_and_get(get_user_info_from_request)
        if error_response:
            return error_response, status_code

        # クエリパラメータの取得
        offset = request.args.get('offset', default=0, type=int)
        limit = request.args.get('limit', default=10, type=int)

        # 質問履歴を取得
        questions = Question.query.filter_by(user_id=user.id)\
            .order_by(Question.created_at.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()

        # 質問と回答情報を整形
        question_history = []
        for question in questions:
            answer = Answer.query.filter_by(question_id=question.id).first()

            if question.mode.name == "word":
                related_words = [
                    rw.related_word
                    for rw in RelatedWord.query.filter_by(answer_id=answer.id).all()
                ] if answer else []
                question_history.append({
                    "question_id": question.id,
                    "message": question.message,
                    "answer": {
                        "message": answer.message if answer else None,
                        "related_words": related_words
                    }
                })

            elif question.mode.name == "latest":
                references = [
                    {"title": ref.title, "url": ref.url}
                    for ref in Reference.query.filter_by(answer_id=answer.id).all()
                ] if answer else []
                question_history.append({
                    "question_id": question.id,
                    "message": question.message,
                    "answer": {
                        "message": answer.message if answer else None,
                        "references": references
                    }
                })

        # レスポンスの生成
        return jsonify({"questions": question_history}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred while retrieving question history.", "details": str(e)}), 500
