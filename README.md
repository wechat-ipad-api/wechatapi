<div align="center">

# WechatApi · 个人微信 HTTP API / SDK

**基于 iPad 协议的个人微信机器人接入服务** —— 扫码登录，用 HTTP 接口收发消息、管理好友与群、发朋友圈，几行代码做出微信机器人。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?logo=python&logoColor=white)](#-快速开始)
[![docs](https://img.shields.io/badge/docs-post.wechatapi.net-37c6f4)](https://post.wechatapi.net)
[![website](https://img.shields.io/badge/官网-wechatapi.net-7aa6ff)](https://wechatapi.net)

[官网](https://wechatapi.net) · [开发文档](https://post.wechatapi.net) · [实战博客](https://wechatapi.net/blog/) · [控制台](https://newmanager.wechatapi.net/dashboard/)

</div>

---

## 简介

**WechatApi** 把复杂的个人微信协议封装成简单的 **HTTP / REST 接口**：你不用研究底层协议、不用常驻 PC，**注册、扫码登录微信号**，就能用任意语言调用接口实现自动化——自动回复、智能客服、社群运营、SCRM、私域获客等。

> 适合：微信机器人开发、微信二次开发、个人微信 API 对接、wechaty / itchat 替代方案。

## ✨ 特性

- 🟢 **能力全**：登录、消息收发（文本/图片/文件/语音/视频/链接/小程序）、好友、群、朋友圈、标签、收藏、视频号
- 🔌 **语言无关**：纯 HTTP + JSON，Python / Java / Go / PHP / Node 任意语言可接
- 📩 **消息回调**：收到消息实时 Webhook 推送到你的服务，方便接 GPT / Claude / 通义等大模型
- 🛡 **稳定**：基于 iPad 协议，可与手机端共存；内置调用频率规范，降低风控
- 📖 **文档齐全**：[完整接口文档](https://post.wechatapi.net) + [100+ 篇实战教程](https://wechatapi.net/blog/)

## 🚀 快速开始

> 代码为示例，`BASE / TOKEN / APPID` 替换为你注册后获取的真实值；具体接口路径与字段以[官方文档](https://post.wechatapi.net)为准。

**1. 安装依赖**

```bash
pip install requests
```

**2. 拿到凭证**：到[控制台](https://newmanager.wechatapi.net/dashboard/)注册 → 扫码登录微信号 → 获得 `Token` 和 `appId`。

**3. 发出第一条消息**

```python
from wechatapi import WeixinClient

client = WeixinClient(
    base="https://你的接口域名",   # 注册后在官方文档/控制台获取
    token="你的Token",
    app_id="你的appId",           # 扫码登录后得到（设备ID）
)

resp = client.send_text("wxid_xxxxxx", "你好，我是机器人 👋")
print(resp)   # {'ret': 200, 'msg': '操作成功', 'data': {...}}
```

**4. 收消息 + 自动回复**（Flask 接收回调）

```python
from flask import Flask, request
from wechatapi import WeixinClient

app = Flask(__name__)
client = WeixinClient(base="https://你的接口域名", token="你的Token", app_id="你的appId")

@app.route("/callback", methods=["POST"])
def callback():
    msg = request.get_json() or {}
    frm, content = msg.get("fromWxid"), msg.get("content", "")  # 字段以官方文档为准
    if frm and content:
        client.send_text(frm, f"已收到：{content}")
    return "ok"

# 别忘了把公网回调地址告诉平台：client.set_callback("https://你的服务器/callback")
app.run(host="0.0.0.0", port=8080)
```

更多示例见 [`examples/`](examples/)：自动回复、接 GPT、入群欢迎、群管理等。

## 🧩 接口模块概览

| 模块 | 能力 |
|---|---|
| 登录 | 获取二维码、扫码登录、检测在线、断线重连、设置回调、设置代理 |
| 消息 | 发文本/图片/文件/语音/视频/链接/名片/小程序、转发、撤回、下载 |
| 联系人 | 通讯录、搜索、加好友/同意、删除、备注、检测关系 |
| 群 | 建群、邀请/移除、群成员、群公告、群二维码、群管理 |
| 朋友圈 | 发文字/图片/视频/链接、点赞评论、可见范围 |
| 其它 | 标签、个人资料、收藏夹、视频号 |

> 完整参数与返回见 **[接口文档](docs/api-reference.md)** 或在线版 **[post.wechatapi.net](https://post.wechatapi.net)**。

## 📚 文档与教程

- 📖 **完整接口文档**：https://post.wechatapi.net
- 📝 **实战博客（100+ 篇）**：https://wechatapi.net/blog/ —— 微信机器人、API 对接、私域自动化、各语言教程
- 🌐 **官网**：https://wechatapi.net

## ⚠️ 合规提示

请确保微信账号已实名认证且正常使用；**新注册、未实名、有被封记录的低质量账号请勿接入**。严禁用于骚扰、营销轰炸、诈骗等违反微信规则与法律法规的行为。个人微信协议接入存在平台规则与风控要求，请合理合规使用、控制调用频率。

## 📄 License

[MIT](LICENSE) © WechatApi
