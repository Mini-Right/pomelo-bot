#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/4 23:24
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : im.py
# @Software    : PyCharm
# @Description :
import uuid
from typing import List

from requests_toolbelt import MultipartEncoder

from pomelo.config.MIME import MIME
from pomelo.ext.sdk.lark_suite import LarkSuiteBaseAPI


class LarkSuiteIMAPI(LarkSuiteBaseAPI):
    def __init__(self, app_id: str, app_secret: str):
        super().__init__(app_id=app_id, app_secret=app_secret)

    def chat_list(self):
        """
        获取机器人所在群列表
        https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/chat/list
        """
        url = self.domain + '/open-apis/im/v1/chats'
        params = {
            'page_size': 5,
        }
        chat_list = self.recursion_invoke_api(url=url, method='GET', params=params)
        chat_list = [
            {
                'chat_name': item.get('name'),
                'chat_id': item.get('chat_id'),
                'chat_avatar': item.get('avatar'),
                'chat_description': item.get('description'),
            }
            for item in chat_list
        ]
        return chat_list

    def chat_get(self, chat_id: str):
        """
        获取群信息
        https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/chat/get
        :param chat_id:  群组ID
        """
        url = self.domain + f'/open-apis/im/v1/chats/{chat_id}'
        response = self.invoke_api(url=url, method='GET')
        response_data = response.json().get('data')
        chat_info = {
            'chat_name': response_data.get('name'),
            'chat_id': chat_id,
            'chat_avatar': response_data.get('avatar'),
            'chat_description': response_data.get('description'),
            # 机器人数量
            'bot_count': response_data.get('bot_count'),
            # 用户数量
            'user_count': response_data.get('user_count'),
        }
        return chat_info

    def chat_create(self, name: str, user_open_id_list: List[str], description: str = None, avatar: str = 'default-avatar_44ae0ca3-e140-494b-956f-78091e348435', owner_id: str = None):
        """
        创建群聊
        https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/chat/create
        :param name:                群名称
        :param user_open_id_list:   群成员open_id数组
        :param description:         群描述
        :param avatar:              群图片 为上传图片的image key
        :param owner_id:            群主open_id
        """
        url = self.domain + '/open-apis/im/v1/chats'
        params = {
            'set_bot_manager': False,
            'user_id_type': 'open_id',
            'uuid': uuid.uuid4().hex
        }
        body = {
            "avatar": avatar,
            "name": name,
            "description": description,
            "user_id_list": user_open_id_list,
            "owner_id": owner_id,
            "chat_mode": "group",
            "chat_type": "private",
            "external": False,
            "join_message_visibility": "all_members",
            "leave_message_visibility": "all_members",
            "membership_approval": "no_approval_required"
        }
        response = self.invoke_api(url=url, method='POST', params=params, body=body)
        response_data = response.json().get('data')
        chat_id = response_data.get('chat_id')
        return chat_id

    def chat_delete(self, chat_id: str):
        """
        解散群聊 只能解散机器人为群主或者管理员的群
        https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/chat/delete
        :param chat_id:     群组ID
        :return:
        """
        url = self.domain + f'/open-apis/im/v1/chats/{chat_id}'
        response = self.invoke_api(url=url, method='DELETE')
        return response.json().get('code')

    def message_create(self, receive_id: str, msg_type: str, content: str, receive_id_type: str = 'open_id', uuid: str = None):
        """
        发送消息
        https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create
        :param receive_id:          接收者id 根据receive_id_type
        :param msg_type:            文本 text; 富文本 post; 图片 image; 消息卡片 interactive; 分享群名片 share_chat; 分享个人名片 share_user; 语音 audio; 视频 media; 文件 file; 表情包 sticker
        :param content:             消息内容，JSON结构序列化后的字符串
        :param receive_id_type:     消息接收者id类型 open_id user_id union_id email chat_id
        :param uuid:                由开发者生成的唯一字符串序列，用于发送消息请求去重；持有相同uuid的请求1小时内至多成功发送一条消息
        """
        url = self.domain + '/open-apis/im/v1/messages'
        params = {
            'receive_id_type': receive_id_type,
        }
        body = {
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": content,
            "uuid": uuid,
        }
        response = self.invoke_api(url=url, method='POST', params=params, body=body)
        response_data = response.json().get('data')
        message_id = response_data.get('message_id')
        return message_id

    def image_create(self, image_path: str, image_type: str = 'message'):
        """
        上传图片
        https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create
        :param image_path:  图片本地路径
        :param image_type:  图片类型 message; avatar
        :return:
        """
        url = self.domain + '/open-apis/im/v1/images'
        form = {
            'image_type': image_type,
            'image': (open(image_path, 'rb')),
        }
        multi_form = MultipartEncoder(form)
        headers = {
            "Authorization": self.get_tenant_access_token_api(),
            "Content-Type": multi_form.content_type
        }
        response = self.invoke_api(url=url, method='POST', headers=headers, data=multi_form)
        response_data = response.json().get('data')
        image_key = response_data.get('image_key')
        return image_key

    def file_create(self, file_name: str, file_path: str, file_type: str = 'stream', duration: int = None):
        """
        上传文件
        https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create
        :param file_name:   带后缀的文件名
        :param file_path:   文件路径
        :param file_type:   文件类型    mp4; pdf; doc; xls; ppt; stream
        :param duration:    视频、音频文件时长 毫秒
        """
        url = self.domain + '/open-apis/im/v1/files'
        form = {
            'file_type': file_type,
            'file_name': file_name,
            'file': (file_name, open(file_path, 'rb'), MIME.get(file_name.split('.')[-1]) or 'text/plain'),
            'duration': duration,
        }
        multi_form = MultipartEncoder(form)
        headers = {
            "Authorization": self.get_tenant_access_token_api(),
            "Content-Type": multi_form.content_type
        }
        response = self.invoke_api(url=url, method='POST', headers=headers, data=multi_form)
        response_data = response.json().get('data')
        file_key = response_data.get('file_key')
        return file_key

    def pin_create(self, message_id: str):
        """
        pin消息
        https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/pin/create
        :param message_id:  消息ID
        """
        url = self.domain + '/open-apis/im/v1/pins'
        body = {
            "message_id": message_id,
        }
        self.invoke_api(url=url, method='POST', body=body)

    def pin_delete(self, message_id: str):
        """
        取消pin消息
        https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/pin/delete
        :param message_id:  消息ID
        :return:
        """
        url = self.domain + f'/open-apis/im/v1/pins/{message_id}'
        self.invoke_api(url=url, method='DELETE')
