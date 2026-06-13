"""示例 2：关键词自动回复机器人。

思路：平台把收到的消息 POST 到你的回调地址 → 匹配关键词 → 调接口回复。
需要一个公网可达的服务（本地调试可用 ngrok / cpolar）。
文档：https://post.wechatapi.net
"""
from flask import Flask, request
from wechatapi import WeixinClient

app = Flask(__name__)
client = WeixinClient(base="https://你的接口域名", token="你的Token", app_id="你的appId")

RULES = {
    "你好": "你好呀，有什么可以帮你？",
    "价格": "套餐与价格见官网，或回复『人工』转客服。",
    "文档": "开发文档：https://post.wechatapi.net",
}


@app.route("/callback", methods=["POST"])
def callback():
    msg = request.get_json() or {}
    # 字段以官方文档为准
    from_wxid = msg.get("fromWxid")
    content = (msg.get("content") or "").strip()
    if from_wxid and content:
        for kw, reply in RULES.items():
            if kw in content:
                client.send_text(from_wxid, reply)
                break
    return "ok"


if __name__ == "__main__":
    # 启动后把公网地址告诉平台：
    # client.set_callback("https://你的服务器/callback")
    app.run(host="0.0.0.0", port=8080)
