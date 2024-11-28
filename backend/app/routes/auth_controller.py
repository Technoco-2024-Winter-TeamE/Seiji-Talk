from flask import Blueprint,redirect, make_response, session, request, jsonify, Response
import uuid
import http
from app.services.google_auth_service import (
	validate_state,fetch_google_token,fetch_user_info,generate_auth_url
)

auth_bp = Blueprint('api/auth', __name__)

@auth_bp.route('/start', methods=['GET'])
def auth_start() -> Response:
    """
    認証プロセスを開始するためのエンドポイントです。
    この関数は、UUIDを使用して新しいセッションIDと状態を生成し、Googleの認証URLにリダイレクトします。
    セッションIDはクッキーに保存され、状態はセッションに保存されます。

    Returns:
        response : Googleの認証ページにリダイレクトします。
    """
    session_id = str(uuid.uuid4())
    google_auth_url = generate_auth_url()

    response = make_response(redirect(google_auth_url, code=http.HTTPStatus.SEE_OTHER.value))
    response.set_cookie('session_id', session_id, httponly=True, secure=True, samesite='Strict')
    return response

@auth_bp.route('/callback', methods=['GET'])
def auth_callback() -> Response:
    """
    Google認証からのコールバックを処理するエンドポイントです。
    認証コードと状態を受け取り、状態の検証、トークンの取得、ユーザー情報の取得を行います。
    すべての処理が成功すれば、アクセストークンとユーザー情報を返します。

    Returns:
        JSON response: 認証が成功すればアクセストークン、ユーザー情報を含むJSONレスポンスを返します。
                        エラーが発生した場合、エラーメッセージを含むJSONレスポンスを返します。
    """
    received_state = request.args.get('state')
    code = request.args.get('code')

    if not validate_state(received_state):
        return jsonify({"error": "Invalid state"}), http.HTTPStatus.BAD_REQUEST.value

    if not code:
        return jsonify({"error": "Authorization code missing"}), http.HTTPStatus.BAD_REQUEST.value

    token_data, token_error = fetch_google_token(code)
    if not token_data:
        return jsonify({"error": "Failed to fetch token", "details": token_error}), http.HTTPStatus.BAD_REQUEST.value

    access_token = token_data.get("access_token")
    
    user_info, user_info_error = fetch_user_info(access_token)
    if not user_info:
        return jsonify({"error": "Failed to fetch user info", "details": user_info_error}), http.HTTPStatus.BAD_REQUEST.value

    return jsonify({
        "access_token": access_token,
        "expires_in": token_data.get("expires_in"),
        "user_info": user_info
    })