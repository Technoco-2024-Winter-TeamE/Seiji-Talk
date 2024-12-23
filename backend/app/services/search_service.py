
import requests
from duckduckgo_search import DDGS
import json


with open('app/google_config.json') as config_file:
    config = json.load(config_file)

API_KEY = config['search']['api_key']
SEARCH_ENGINE_ID = config['search']['search_engine_id']
GOOGLE_API_URL = "https://www.googleapis.com/customsearch/v1"

def search_google(query, num_results=6) -> list[dict]:
    """
    Google Custom Search APIを非同期で使って指定したクエリで検索し、結果を整形する。

    Args:
        query (str): 検索クエリ
        num_results (int): 取得する検索結果の数

    Returns:
        list[dict]: 検索結果のリスト [{'title': 'ページタイトル', 'url': 'URL','snippet': '概要'}, ...]
    """
    if not query:
        raise ValueError("検索クエリは必須です")

    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": num_results
    }

    try:
        response = requests.get(GOOGLE_API_URL, params=params, timeout=10)
        response.raise_for_status()  # HTTPエラーを確認
        data = response.json()
        # 検索結果を整形してリストにする
        results_list = [
            {
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", "")  # スニペットを追加
            }
            for item in data.get("items", [])
        ]
        return results_list
    except Exception as e:
        raise Exception(f"Google APIエラー: {e}")
    

def search_duckduckgo(search_query: str,num_results=6) -> list[dict]:
    """
    DuckDuckGo検索を行い、結果をタイトルとURLのリスト形式で返す。

    Args:
        search_query (str): 検索クエリ

    Returns:
        list[dict]: 検索結果のリスト [{'title': 'ページタイトル', 'url': 'URL','snippet': '概要'}, ...]
    """
    results_list = []
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                keywords=search_query,
                region='jp-jp',
                safesearch='off',
                timelimit=None,
                max_results=num_results
            ))

            for result in results:
                results_list.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", "")  # スニペットを追加
                })
    except Exception as e:
        raise Exception(f"DuckDuckGo検索エラー: {e}")

    return results_list


def search_with_fallback(query: str) -> list[dict]:
    """
    Google Custom Search APIで検索し、エラー時にはDuckDuckGoに切り替える。

    Args:
        query (str): 検索クエリ
        num_results (int): 取得する検索結果の数

    Returns:
        list[dict]: 検索結果のリスト [{'title': '...', 'url': '...', 'snippet': '...'}, ...]
    """
    try:
        # Google APIで検索
        print("Google Custom Search APIを使用しています...")
        results = search_google(query)
        return results
    except Exception as e:
        print(f"Google APIでエラーが発生: {e}")
        print("DuckDuckGoに切り替えます...")

        # DuckDuckGoで検索
        results = search_duckduckgo(query)
        return results

def main():
    try:
        query = "徳島県 県知事 現在"
        results = search_duckduckgo(query)

        print("=== 検索結果の全体を出力 ===")
        for result in results:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        print("\n=== Snippetの内容をすべて表示 ===")
        for result in results:
            snippet = result.get("snippet", "スニペットが見つかりません")
            print(f"Snippet: {snippet}\n")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    main()