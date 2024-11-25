from flask import Blueprint,redirect, make_response, session, request, jsonify, Response
from app.repositories.repository import SeijiTalkRepository
import uuid
import json
from app.extention import create_repeat_session
import http

with open('app/google_config.json') as config_file:
    config = json.load(config_file)

auth_bp = Blueprint('api/auth', __name__)

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
CLIENT_ID = config['web']['client_id']
CLIENT_SECRET = config['web']['client_secret']
REDIRECT_URI = config['web']['redirect_uris'][0]

rep_session = create_repeat_session()

def validate_state(received_state : str) -> bool:
	"""
    サーバー側で保持しているセッションのstateの値と受信したstateの値を比較して、
	セッションが有効かどうかを返します。
    
    Args:
		received_state (str) : 取得したstateの値。
        
    Returns:
		bool : セッションが有効かどうか
	"""
	session_state = session.get('state')
	return session_state and session_state == received_state


def fetch_google_token(code : str) -> tuple:
    """
    Googleのアクセストークンを取得します。

    GoogleのOAuth 2.0認証コードを使って、アクセストークンを取得します。
    成功した場合はアクセストークンのデータを含む辞書を返し、失敗した場合はNoneとエラーメッセージを返します。

    Parameters:
        code (str): Google認証サーバーから取得した認証コード。

    Returns:
        tuple:
            - 成功した場合: アクセストークンを含む辞書（dict）、エラーがないためNone。
            - 失敗した場合: Noneとエラーメッセージを含む辞書（dict）。
    """
    token_data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = rep_session.post(GOOGLE_TOKEN_URL, data=token_data)
    if response.status_code != http.HTTPStatus.OK.value:
        return None, response.json()
    return response.json(), None

def fetch_user_info(access_token : str) -> tuple:
    """
    Google APIを使って、ユーザーの情報を取得します。

    与えられたアクセストークンを用いてGoogleのユーザー情報エンドポイントにリクエストを送り、
    ユーザーの詳細情報を取得します。成功した場合はユーザー情報の辞書を返し、失敗した場合は
    Noneとエラーメッセージを返します。

    Parameters:
        access_token (str): Google OAuth 2.0で取得したアクセストークン。

    Returns:
        tuple:
            - 成功した場合: ユーザー情報を含む辞書（dict）、エラーがないためNone。
            - 失敗した場合: Noneとエラーメッセージを含む辞書（dict）。
    """
    response = rep_session.get(
        GOOGLE_USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"}
    )
    if response.status_code != http.HTTPStatus.OK.value:
        return None, response.json()
    return response.json(), None

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
    state = str(uuid.uuid4())
    session['state'] = state

    google_auth_url = (
        f"{GOOGLE_AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
        f"&response_type=code&scope=email profile&state={state}"
    )

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
        return jsonify({"error": "Invalid state"}), 400

    if not code:
        return jsonify({"error": "Authorization code missing"}), 400

    token_data, token_error = fetch_google_token(code)
    if not token_data:
        return jsonify({"error": "Failed to fetch token", "details": token_error}), 400

    access_token = token_data.get("access_token")
    
    user_info, user_info_error = fetch_user_info(access_token)
    if not user_info:
        return jsonify({"error": "Failed to fetch user info", "details": user_info_error}), 400

    return jsonify({
        "access_token": access_token,
        "expires_in": token_data.get("expires_in"),
        "user_info": user_info
    })