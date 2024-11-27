import aiohttp
from openai import OpenAI
import json
import asyncio
import os

# OpenAI APIキーの設定（環境変数や設定ファイルから取得するのが推奨）
#os.environ.get("OPENAI_API_KEY")
client = OpenAI()


async def generate_search_query(question: str):
    """
    質問内容をOpenAI APIで処理し、検索エンジン向けの最適化されたクエリを生成する。

    Args:
        question (str): ユーザーが入力した質問内容。

    Returns:
        str: 検索エンジン向けに最適化されたクエリ。
    """
    try:

        # チャット補完のリクエスト
        chat_completion = client.chat.completions.create(
            model="gpt-4o-mini",  # 使用するモデル
            messages = [
                {
                    "role": "system",
                    "content": (
                        "あなたは検索クエリの作成に特化した専門家です。"
                        "ユーザーが提供した情報を基に、検索エンジンで効果的かつ関連性の高い検索クエリを生成してください。"
                        "生成するクエリはシンプルで、ユーザーが求める情報を的確に引き出せるように工夫してください。"
                        "鍵かっこや余計な記号を含めず、簡潔で明確な検索クエリを生成してください。"
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.7,
            max_tokens=60,
            n=1  # 生成する選択肢の数
        )

        # 結果を取り出す
        search_query = chat_completion.choices[0].message.content.strip()

        return search_query

    except Exception as e:
        print(f"Error generating search query: {str(e)}")
        return None



async def generate_word_answer(question: str):
    """
    質問内容をOpenAI APIで処理し、用語検索や従来知識の回答を出力する。

    Args:
        question (str): ユーザーが入力した質問内容。

    Returns:
        str: 用語に対しての適切な回答。
    """
    try:

        # チャット補完のリクエスト
        chat_completion = client.chat.completions.create(
            model="gpt-4o-mini",  # 使用するモデル
            messages = [
                {
                    "role": "system",
                    "content": (
                        "あなたは政治や社会に関する質問に厳格に対応する専門家です。"
                        "ユーザーの質問に対して、簡潔で正確な回答を提供してください。"
                        "さらに、回答に関連するキーワードや用語を4つ生成し、厳密にJSON形式で出力してください。"
                        "JSON形式のルールに厳密に従い、それ以外の形式で応答を返さないでください。"
                        "JSON形式は次のようにしてください："
                        '{"message": "回答内容", "related_words": ["関連用語1", "関連用語2", "関連用語3", "関連用語4"]}'
                        "注意: JSON内のすべてのキーと文字列はダブルクォーテーションで囲む必要があります。"
                        "その他のコメントや説明文は出力に含めないでください。"
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.7,
            max_tokens=250,
            n=1  # 生成する選択肢の数
        )

        # 結果を取り出す
        answer = chat_completion.choices[0].message.content.strip()

        # JSON形式の検証と変換
        try:
            parsed_json = json.loads(answer)  # JSON形式かどうかを検証しながら辞書に変換

            # フォーマットの詳細な検証
            if (
                isinstance(parsed_json, dict) and
                "message" in parsed_json and isinstance(parsed_json["message"], str) and
                "related_words" in parsed_json and
                isinstance(parsed_json["related_words"], list) and
                all(isinstance(word, str) for word in parsed_json["related_words"])  # すべて文字列か確認
            ):
                return parsed_json  # 正しい形式なら辞書を返す
            else:
                print("JSON形式は正しいが、フォーマットが不適切です。")
                return None  # フォーマットが不正の場合

        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            print(f"生成された回答: {answer}")
            return None  # JSON形式が不正な場合


    except Exception as e:
        print(f"Error generating search query: {str(e)}")
        return None

async def rank_search_results(query: str, results: list[dict]) -> list[dict]:
    """
    検索クエリと検索結果を基に、OpenAIを使って適切な順序に並べ替える。

    Args:
        query (str): 検索クエリ
        results (list[dict]): 検索結果のリスト [{'title': '...', 'url': '...', 'snippet': '...'}, ...]

    Returns:
        list[dict]: 並べ替えられた検索結果リスト
    """
    # プロンプトの構築
    prompt = (
        f"以下は検索クエリ「{query}」に対する検索結果のリストです。\n"
        "クエリに基づいて最も関連性が高い順に並べ替えてください。\n"
        "スニペットやURLの信頼性も考慮してください。\n\n"
        f"検索クエリ: {query}\n"
        "検索結果:\n"
        f"{results}\n\n"
        "出力形式:\n"
        "[\n"
        "  {\"title\": \"...\", \"url\": \"...\", \"snippet\": \"...\"},\n"
        "]\n"
    )

    # OpenAI APIリクエスト
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0
    )

    # OpenAIからの応答を解析
    try:
        sorted_results = eval(response["choices"][0]["message"]["content"])
        return sorted_results
    except Exception as e:
        raise ValueError(f"並べ替え結果の解析に失敗しました: {e}")

if __name__ == "__main__":
    async def main():
        # ユーザーに質問を入力してもらう
        question = input("検索クエリを生成したい質問を入力してください: ")

        # generate_search_query関数を実行して検索クエリを生成
        search_query = await generate_search_query(question)
        # search_query = await generate_word_answer(question)

        if search_query:
            print(f"生成された検索クエリ: {search_query}")
        else:
            print("検索クエリの生成に失敗しました。")

    # asyncioのイベントループでmainを実行
    asyncio.run(main())