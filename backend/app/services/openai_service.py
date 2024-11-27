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
        list[dict]: 並べ替えられた検索結果リスト（上位3件）
    """
    # システムプロンプト
    system_prompt = (
        "あなたは検索結果を評価し、クエリに基づいて最も関連性の高い順に並べ替える専門家です。\n"
        "以下の要素を考慮して評価を行い、結果を厳密に指定されたJSON形式で返してください。\n"
        "考慮すべき要素:\n"
        "- クエリとの関連性: 検索クエリ内のキーワードが結果のタイトルやスニペットにどの程度一致しているか。\n"
        "- スニペットの内容: スニペットが具体的で役に立つ情報を含んでいるか。\n"
        "- URLの信頼性: 信頼性のあるドメイン（例: .edu, .gov, .jp など）か。\n"
        "- 情報の鮮度: 最新の情報を優先。\n"
        "- 情報の具体性: 内容が曖昧でなく具体的か。\n\n"
        "JSON形式のルール:\n"
        "1. 出力形式は以下のようにしてください:\n"
        '[{"title": "タイトル1", "url": "URL1", "snippet": "スニペット1"}, {"title": "タイトル2", "url": "URL2", "snippet": "スニペット2"}]\n'
        "2. すべてのキーと値はダブルクォーテーションで囲む必要があります。\n"
        "3. JSON以外の形式や追加のコメントを含めないでください。"
    )

    # ユーザープロンプト
    user_prompt = (
        f"以下は検索クエリ「{query}」に対する検索結果のリストです。\n"
        "検索結果を並べ替えてください。\n\n"
        f"検索クエリ: {query}\n"
        "検索結果:\n"
        f"{json.dumps(results, ensure_ascii=False, indent=2)}\n\n"
    )

    try:
        # OpenAI APIリクエスト
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 使用するモデル
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
            n=1
        )

        # OpenAIからの応答をパース
        content = response.choices[0].message.content.strip()

        # 応答が空の場合のチェック
        if not content:
            raise ValueError("OpenAIからの応答が空です。")

        try:
            # JSON形式にパース
            parsed_json = json.loads(content)

            # フォーマットの詳細な検証
            if (
                isinstance(parsed_json, list) and
                all(
                    isinstance(item, dict) and
                    "title" in item and isinstance(item["title"], str) and
                    "url" in item and isinstance(item["url"], str) and
                    "snippet" in item and isinstance(item["snippet"], str)
                    for item in parsed_json
                )
            ):
                return parsed_json[:3]  # 上位3件を返す
            else:
                print("JSON形式は正しいが、フォーマットが不適切です。")
                return None  # フォーマットが不正の場合

        except json.JSONDecodeError as e:
            # 応答をトリムして解析の再試行
            fixed_content = content.splitlines()
            try:
                parsed_json = json.loads("".join(fixed_content))
                return parsed_json[:3]
            except Exception as inner_e:
                raise ValueError(f"JSON解析に失敗しました: {inner_e}\n応答内容:\n{content}")

    except Exception as e:
        raise ValueError(f"並べ替え中にエラーが発生しました: {e}")


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