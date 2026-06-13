"""示例 1：发送各类消息。

运行前把 BASE / TOKEN / APPID 换成你注册后获取的真实值。
文档：https://post.wechatapi.net
"""
from wechatapi import WeixinClient

client = WeixinClient(
    base="https://你的接口域名",   # 注册后在官方文档/控制台获取
    token="你的Token",
    app_id="你的appId",           # 扫码登录后得到
)

# 文本
print(client.send_text("wxid_xxxxxx", "你好，我是机器人 👋"))

# 群里 @某人（content 里也要包含 @昵称）
# print(client.send_text("12345678@chatroom", "@张三 欢迎入群", ats="wxid_zhangsan"))

# 图片 / 文件 / 链接
# print(client.send_image("wxid_xxxxxx", "https://example.com/a.png"))
# print(client.send_file("wxid_xxxxxx", "https://example.com/a.pdf", "报价单.pdf"))
# print(client.send_link("wxid_xxxxxx", "标题", "描述", "https://wechatapi.net"))
