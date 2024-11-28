from app import db
from flask import current_app
from app.models.model import Question, Answer
from app.repositories.repository import SeijiTalkRepository
from app.services.openai_service import generate_search_query,generate_word_answer,rank_search_results, process_search_results
from app.services.search_service import search_with_fallback
import json
import traceback

# from openai_service import generate_search_query,generate_word_answer,rank_search_results
# from search_service import search_with_fallback



def handle_latest_mode(question :Question):
    """
    'latest' モードの場合の処理。
    外部API（例: Google APIやDuckDuckGo API）を使って検索し、結果を要約する。

    Args:
        question (Question): 質問オブジェクト。

    Returns:
        None    (データベースにとうろくしたら終わり)

    """
    try:
        # 質問から検索クエリを生成
        search_query = generate_search_query(question.message)
        
        # 検索結果を取得（Google API または DuckDuckGo API）
        search_results = search_with_fallback(search_query)

        # 検索結果を出力
        print("検索結果:")
        for result in search_results:
            print(json.dumps(result, indent=2, ensure_ascii=False))


        ranked_results = rank_search_results(search_query,search_results)


        final_results = process_search_results(question.message,ranked_results)


        data = SeijiTalkRepository.save_latest_answer(question,final_results)

    except Exception as e:
        print(f"Error in handle_latest_mode for question {question.id}: {str(e)}")


def handle_word_mode(question :Question):
    """
    'word' モードの場合の処理。
    chatGPTに対して質問を流し、それに対する回答を得る。

    Args:
        question (Question): 質問オブジェクト。

    Returns:
        None (データベースに追加して終わり)
    """
    try:
        # 質問からキーワードを抽出 OpenAiで抽出
        answer = generate_word_answer(question.message)
        
        data = SeijiTalkRepository.save_word_answer(question, answer)
    except Exception as e:
        print(f"Error in handle_latest_mode for question {question.id}: {str(e)}")



def process_question(question_id: str) -> None:
    """
    質問IDを受け取り、対応する質問を取得して非同期で処理を行う。

    Args:
        question_id (str): 質問のID。

    Returns:
        None
    """

    try:
        # アプリケーションコンテキストの中で処理を実行
        with current_app.app_context():
            # 質問をデータベースから取得
            question = Question.query.filter_by(id=question_id).first()
            if not question:
                raise ValueError(f"Question with ID '{question_id}' not found.")

            if question.mode.name == "latest":
                # "latest" モードに対する処理
                handle_latest_mode(question)  # 外部API呼び出しや検索の処理
            elif question.mode.name == "word":
                # "word" モードに対する処理
                handle_word_mode(question)  # 関連語の抽出や検出の処理

    except Exception as e:
        print(f"Error in process_question for question {question_id}: {str(e)}")
        traceback.print_exc()


if __name__ == "__main__":

    def main():
        # ユーザーに質問を入力してもらう
        question = input("検索クエリを生成したい質問を入力してください: ")

        # generate_search_query関数を実行して検索クエリを生成
        search_query = generate_search_query(question)

        if search_query:
            print(f"生成された検索クエリ: {search_query}")
        else:
            print("検索クエリの生成に失敗しました。")
            return

        # 検索結果を取得（Google API または DuckDuckGo API）
        search_results = search_with_fallback(search_query)

        # 検索結果を出力
        print("検索結果:")
        for result in search_results:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        # 検索結果を並べ替え
        ranked_results = rank_search_results(search_query, search_results)

        print("並べ替えられた検索結果:")
        for result in ranked_results:
            print(json.dumps(result, indent=2, ensure_ascii=False))



