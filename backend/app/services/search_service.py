
import requests
from duckduckgo_search import DDGS
import json, aiohttp,asyncio


with open('../google_config.json') as config_file:
    config = json.load(config_file)

API_KEY = config['search']['api_key']
SEARCH_ENGINE_ID = config['search']['search_engine_id']
GOOGLE_API_URL = "https://www.googleapis.com/customsearch/v1"

async def search_google(query, num_results=10) -> list[dict]:
    """
    Google Custom Search APIを非同期で使って指定したクエリで検索し、結果を整形する。

    Args:
        query (str): 検索クエリ
        num_results (int): 取得する検索結果の数

    Returns:
        list[dict]: 整形された検索結果のリスト。各辞書は以下のキーを持つ:
            - "title": 検索結果のタイトル
            - "url": 検索結果のリンク
    """
    if not query:
        raise ValueError("検索クエリは必須です")

    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": num_results
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(GOOGLE_API_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                # 検索結果を整形してリストにする
                results_list = [
                    {
                        "title": item.get("title", ""),
                        "url": item.get("link", "")
                    }
                    for item in data.get("items", [])
                ]
                return results_list
            else:
                raise Exception(f"APIエラー: {response.status}, {await response.text()}")

def search_duckduckgo(search_query: str) -> list[dict]:
    """
    DuckDuckGo検索を行い、結果をタイトルとURLのリスト形式で返す。

    Args:
        search_query (str): 検索クエリ

    Returns:
        list[dict]: 検索結果のリスト [{'title': 'ページタイトル', 'url': 'URL'}, ...]
    """
    results_list = []
    with DDGS() as ddgs:
        results = list(ddgs.text(
            keywords=search_query,
            region='jp-jp',        
            safesearch='off',
            timelimit=None,
            max_results=10
        ))
        
        for result in results:
            results_list.append({
                "title": result.get("title", ""),
                "url": result.get("href", "")
            })
    
    return results_list



async def main():
    try:
        query = "東京大学医学部単位数"
        results = search_duckduckgo(query)
        for result in results:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        # query = "東京大学 医学部 単位数"
        # results = await search_google(query)
        # print(results)
    except Exception as e:
        print(f"エラーが発生しました: {e}")

# 非同期実行
if __name__ == "__main__":
    asyncio.run(main())