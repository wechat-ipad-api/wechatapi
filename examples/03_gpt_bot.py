"""示例 3：接入大模型的智能微信机器人。

在『收消息回调』里把内容交给大模型（GPT / Claude / 通义等），再发回微信。
文档：https://post.wechatapi.net
"""
from flask import Flask, request
from wechatapi import WeixinClient
from openai import OpenAI  # 也可换成 Claude / 通义 等 SDK

app = Flask(__name__)
client = WeixinClient(base="https://你的接口域名", token="你的Token", app_id="你的appId")
llm = OpenAI(api_key="你的模型APIKey")


def ask_ai(text: str) -> str:
    resp = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是一个微信客服助手，回答简洁、友好。"},
            {"role": "user", "content": text},
        ],
    )
    return resp.choices[0].message.content.strip()


@app.route("/callback", methods=["POST"])
def callback():
    msg = request.get_json() or {}
    from_wxid = msg.get("fromWxid")
    content = (msg.get("content") or "").strip()
    if from_wxid and content:
        client.send_text(from_wxid, ask_ai(content))
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
