import uuid
import http
import json
from flask import session
from app.extention import create_repeat_session

rep_session = create_repeat_session()

with open('app/google_config.json') as config_file:
    config = json.load(config_file)

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
CLIENT_ID = config['web']['client_id']
CLIENT_SECRET = config['web']['client_secret']
REDIRECT_URI = config['web']['redirect_uris'][0]

def validate_state(received_state: str) -> bool:
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

def fetch_google_token(code: str) -> tuple:
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

def fetch_user_info(access_token: str) -> tuple:
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

def generate_auth_url() -> str:
    """
    Google認証用のURLを生成
    
    Returns:
        str : Google認証用のURL
    """
    state = str(uuid.uuid4())
    session['state'] = state

    return (
        f"{GOOGLE_AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
        f"&response_type=code&scope=email profile&state={state}"
    )


