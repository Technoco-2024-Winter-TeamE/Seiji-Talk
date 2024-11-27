from bs4 import BeautifulSoup
import requests

async def scrape_page_content(url: str) -> str:
    """
    指定したURLのページ内容を非同期でスクレイピングして、テキストを返す。

    Args:
        url (str): ページのURL

    Returns:
        str: ページのテキスト内容
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # HTTPエラーを確認
        html_content = response.text  # ページ内容を取得
        soup = BeautifulSoup(html_content, "html.parser")

        # 主に本文に含まれるテキストを抽出
        text = soup.get_text(separator="\n", strip=True)
        return text
    except Exception as e:
        print(f"ページ内容の取得に失敗しました: {e}")
        return ""
    

if __name__ == "__main__":
    # サンプルURLを指定
    test_url = "https://www.tokushima-u.ac.jp/access/"  # Wikipediaのトップページ

    # スクレイピングを実行
    content = scrape_page_content(test_url)

    # 結果を表示
    if content:
        print("スクレイピング結果:")
        print(content)  # 最初の1000文字を表示
        print(len(content))
    else:
        print("スクレイピングに失敗しました。")