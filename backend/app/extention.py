import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import http

def create_repeat_session() -> requests.Session:
    """
    再試行機能付きのHTTPセッションを作成する関数です。
    この関数は、指定されたステータスコードに対して最大5回のリトライを設定し、
    各リトライの間に指数バックオフを適用します。

    Returns:
        requests.Session: 再試行機能を持つセッションオブジェクト。
    """
    
    session = requests.Session()
    retry = Retry(
        total=5, 
        backoff_factor=1,
        status_forcelist=[
                          http.HTTPStatus.INTERNAL_SERVER_ERROR.value,
                          http.HTTPStatus.BAD_GATEWAY.value,
                          http.HTTPStatus.SERVICE_UNAVAILABLE.value,
                          http.HTTPStatus.GATEWAY_TIMEOUT.value,
                          http.HTTPStatus.REQUEST_TIMEOUT.value
                          ], 
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session