"""WechatApi HTTP 客户端封装。

设计为通用、轻量的 HTTP 包装：所有接口都是 POST + JSON，token 放请求头，
通用参数 appId 自动注入。除内置的便捷方法外，可用 `call(path, **params)`
调用任意接口。**具体接口路径、参数与返回字段以官方文档为准：**
https://post.wechatapi.net
"""
import requests


class WechatApiError(Exception):
    """接口调用异常。"""


class WeixinClient:
    def __init__(self, base, token, app_id=None,
                 token_header="VideosApi-token", timeout=15):
        """
        :param base:  接口域名，如 https://你的接口域名（注册后在文档/控制台获取）
        :param token: 鉴权 Token
        :param app_id: 设备ID，扫码登录成功后获得；之后所有接口自动带上
        :param token_header: 鉴权请求头字段名（以官方文档为准）
        """
        self.base = base.rstrip("/")
        self.app_id = app_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers[token_header] = token

    # ---------- 通用调用 ----------
    def call(self, path, **params):
        """调用任意接口。自动注入 appId。返回解析后的 JSON dict。"""
        body = {k: v for k, v in params.items() if v is not None}
        if self.app_id and "appId" not in body:
            body["appId"] = self.app_id
        try:
            r = self.session.post(self.base + path, json=body, timeout=self.timeout)
            data = r.json()
        except ValueError:
            raise WechatApiError("接口返回非 JSON：%s" % r.text[:200])
        except requests.RequestException as e:
            raise WechatApiError("请求失败：%s" % e)
        return data

    @staticmethod
    def ok(resp):
        """ret == 200 视为成功（字段以官方文档为准）。"""
        return isinstance(resp, dict) and resp.get("ret") == 200

    # ---------- 登录 ----------
    def get_login_qrcode(self, region_id=None, proxy_ip=None):
        return self.call("/login/getLoginQrCode", appId=self.app_id or "",
                         regionId=region_id, proxyIp=proxy_ip)

    def check_login(self):
        return self.call("/login/checkLogin")

    def check_online(self):
        return self.call("/login/checkOnline")

    def set_callback(self, callback_url):
        """设置消息回调地址（公网可达）。"""
        return self.call("/login/setCallback", callbackUrl=callback_url)

    def logout(self):
        return self.call("/login/logout")

    # ---------- 消息 ----------
    def send_text(self, to_wxid, content, ats=None):
        """发送文本。群里 @某人时 ats 传对方 wxid（多个逗号分隔，'notify@all' 为全体）。"""
        return self.call("/message/postText", toWxid=to_wxid, content=content, ats=ats)

    def send_image(self, to_wxid, img_url):
        return self.call("/message/postImage", toWxid=to_wxid, imgUrl=img_url)

    def send_file(self, to_wxid, file_url, file_name=None):
        return self.call("/message/postFile", toWxid=to_wxid, fileUrl=file_url, fileName=file_name)

    def send_link(self, to_wxid, title, desc, link_url, thumb_url=None):
        return self.call("/message/postLink", toWxid=to_wxid, title=title,
                         desc=desc, linkUrl=link_url, thumbUrl=thumb_url)

    def revoke(self, to_wxid, new_msg_id, **kw):
        return self.call("/message/revokeMsg", toWxid=to_wxid, newMsgId=new_msg_id, **kw)

    # ---------- 联系人 ----------
    def fetch_contacts(self):
        return self.call("/contacts/fetchContactsList")

    def search_friend(self, keyword):
        return self.call("/contacts/search", keyword=keyword)

    def add_friend(self, **params):
        """加好友/同意好友（参数以官方文档为准，如 v1/v2/scene/content）。"""
        return self.call("/contacts/addContacts", **params)

    def get_detail(self, wxids):
        return self.call("/contacts/getDetailInfo", wxids=wxids)

    def set_remark(self, wxid, remark):
        return self.call("/contacts/setFriendRemark", wxid=wxid, remark=remark)

    # ---------- 群 ----------
    def create_chatroom(self, wxids):
        return self.call("/group/createChatroom", wxids=wxids)

    def get_chatroom_members(self, chatroom_id):
        return self.call("/group/getChatroomMemberList", chatroomId=chatroom_id)

    def invite_member(self, chatroom_id, wxids):
        return self.call("/group/inviteMember", chatroomId=chatroom_id, wxids=wxids)

    def remove_member(self, chatroom_id, wxids):
        return self.call("/group/removeMember", chatroomId=chatroom_id, wxids=wxids)

    def set_announcement(self, chatroom_id, content):
        return self.call("/group/setChatroomAnnouncement", chatroomId=chatroom_id, content=content)

    def get_chatroom_qrcode(self, chatroom_id):
        return self.call("/group/getChatroomQrCode", chatroomId=chatroom_id)

    # ---------- 朋友圈 ----------
    def send_text_sns(self, content):
        return self.call("/sns/sendTextSns", content=content)

    def send_image_sns(self, content, image_infos):
        return self.call("/sns/sendImgSns", content=content, imageInfos=image_infos)

    def like_sns(self, sns_id, **kw):
        return self.call("/sns/likeSns", snsId=sns_id, **kw)

    # ---------- 下载 ----------
    def download_image(self, **params):
        return self.call("/message/downloadImage", **params)

    def download_file(self, **params):
        return self.call("/message/downloadFile", **params)
