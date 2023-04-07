import os
import requests
from dotenv import load_dotenv
load_dotenv()

import openai
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

openai.api_key = os.environ.get("OPENAI_API_KEY")


@app.message("Test")
def test(message, say):
    print(message)
    user = message['user']
    say(f"{user} 님, ChatGPT 테스트입니다.")

# @app.event("app_mention")
# def test(message, say):
#     print(message)
#     user = message['user']
#     say(f"{user} 님, ChatGPT 테스트입니다.")


@app.event("message")
def handle_message(message, say):

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{message}",
        temperature=0,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )
    
    print(response)
    say(response.choices[0].text)

# @app.event("app_mention")
# def answer(message, say):
#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=f"클라우드타입 ChatGPT 슬랙봇 Python 템플릿입니다. 질문을 입력해주세요.\n>> {message}",
#         max_tokens=50,
#         temperature=0,
#         top_p=1,
#         stop=["\n"]
#     )

#     print(response)
#     say(response.choices[0])

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()