from app import db
from app.models.model import Question, Answer
import aiohttp
from services.openai_service import generate_search_query,generate_word_answer,rank_search_results
from services.search_service import search_with_fallback
import json

# from openai_service import generate_search_query,generate_word_answer,rank_search_results
# from search_service import search_with_fallback

async def handle_latest_mode(question :Question):
    """
    'latest' モードの場合の処理。
    外部API（例: Google APIやDuckDuckGo API）を使って検索し、結果を要約する。

    Args:
        question (Question): 質問オブジェクト。

    Returns:
        None
    """
    try:
        # 質問から検索クエリを生成
        search_query = await generate_search_query(question.message)
        
        # 検索結果を取得（Google API または DuckDuckGo API）
        search_results = await search_with_fallback(search_query)

        # 検索結果を出力
        print("検索結果:")
        for result in search_results:
            print(json.dumps(result, indent=2, ensure_ascii=False))


        ranked_results = await rank_search_results(search_query,search_results)

        print(ranked_results)

        # # 検索結果があれば、それを要約
        # if search_results:
        #     summarized_results = await summarize_search_results(search_results)
        #     print(f"Summarized search results: {summarized_results}")
            
        #     # 要約結果をデータベースに保存するなどの処理
        #     # 例えば、Answerを作成して返すなど
        #     await save_answer(question, summarized_results)
        
        # else:
        #     print("No search results found.")

    except Exception as e:
        print(f"Error in handle_latest_mode for question {question.id}: {str(e)}")


async def handle_word_mode(question :Question):
    """
    'latest' モードの場合の処理。
    外部API（例: Google APIやDuckDuckGo API）を使って検索し、結果を要約する。

    Args:
        question (Question): 質問オブジェクト。

    Returns:
        None
    """
    try:
        # 質問からキーワードを抽出（OpenAIや他の方法で抽出）
        keywords = await extract_keywords_from_question(question.message)
        
        # 検索結果を取得（Google API または DuckDuckGo API）
        search_results = await search_with_keywords(keywords)
        
        # 検索結果があれば、それを要約
        if search_results:
            summarized_results = await summarize_search_results(search_results)
            print(f"Summarized search results: {summarized_results}")
            
            # 要約結果をデータベースに保存するなどの処理
            # 例えば、Answerを作成して返すなど
            await save_answer(question, summarized_results)
        
        else:
            print("No search results found.")

    except Exception as e:
        print(f"Error in handle_latest_mode for question {question.id}: {str(e)}")



async def process_question(question_id: str):
    """
    質問IDを受け取り、対応する質問を取得して非同期で処理を行う。

    Args:
        question_id (str): 質問のID。

    Returns:
        None
    """

    try:
        # 質問をデータベースから取得
        question = Question.query.filter_by(id=question_id).first()
        if not question:
            raise ValueError(f"Question with ID '{question_id}' not found.")

        if question.mode.name == "latest":
            # "latest" モードに対する処理
            await handle_latest_mode(question)  # 例: 外部API呼び出しや検索
        elif question.mode.name == "word":
            # "word" モードに対する処理
            await handle_word_mode(question)  # 例: 関連語の抽出や検

    except Exception as e:
        print(f"Error in process_question for question {question_id}: {str(e)}")



if __name__ == "__main__":
    import asyncio

    async def main():
        # ユーザーに質問を入力してもらう
        question = input("検索クエリを生成したい質問を入力してください: ")

        # generate_search_query関数を実行して検索クエリを生成
        search_query = await generate_search_query(question)

        if search_query:
            print(f"生成された検索クエリ: {search_query}")
        else:
            print("検索クエリの生成に失敗しました。")
            return

        # 検索結果を取得（Google API または DuckDuckGo API）
        search_results = await search_with_fallback(search_query)

        # 検索結果を出力
        print("検索結果:")
        for result in search_results:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        # 検索結果を並べ替え
        ranked_results = await rank_search_results(search_query, search_results)

        print("並べ替えられた検索結果:")
        for result in ranked_results:
            print(json.dumps(result, indent=2, ensure_ascii=False))

    asyncio.run(main())


