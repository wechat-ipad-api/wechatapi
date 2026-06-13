"""WechatApi Python SDK —— 个人微信 HTTP API 客户端。

官网:   https://wechatapi.net
文档:   https://post.wechatapi.net
博客:   https://wechatapi.net/blog/
"""
from .client import WeixinClient, WechatApiError

__all__ = ["WeixinClient", "WechatApiError"]
__version__ = "0.1.0"
