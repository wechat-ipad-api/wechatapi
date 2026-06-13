"""示例 4：新成员入群自动欢迎 + 发群规。

监听群事件回调 → 识别新成员入群 → @新人发欢迎语。
事件类型与字段以官方文档为准：https://post.wechatapi.net
"""
from flask import Flask, request
from wechatapi import WeixinClient

app = Flask(__name__)
client = WeixinClient(base="https://你的接口域名", token="你的Token", app_id="你的appId")

WELCOME = "欢迎 @{name} 加入！进群先看群公告，有问题直接 @我。"


@app.route("/callback", methods=["POST"])
def callback():
    msg = request.get_json() or {}
    # 不同平台的入群事件结构不同，以下为示意，字段以官方文档为准
    if msg.get("type") == "member_join":
        chatroom = msg.get("chatroomId")
        new_wxid = msg.get("memberWxid")
        new_name = msg.get("memberName", "新朋友")
        if chatroom and new_wxid:
            client.send_text(chatroom, WELCOME.format(name=new_name), ats=new_wxid)
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
