# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 2020-02-02 20:52
"""

import tornado.gen
import datetime
from tornado.websocket import WebSocketHandler
from tools.logs import Logs
from source.service_manager import ServiceManager


class Controller(WebSocketHandler):

    users = set()
    user_dict = {}
    logger = Logs().logger
    """
    {
        'room_id': {
                'user_id_list': ()
        }
    }
    """
    room_user_dict = {}

    @tornado.gen.coroutine
    def open(self, *args, **kwargs):
        self.users.add(self)

        params = self.get_params()

        if not params.get('room_id'):
            raise tornado.gen.Return(False)

        if params['room_id'] in self.room_user_dict:
            self.room_user_dict[params['room_id']]['user_id_list'].add(params['user_id'])
        else:
            temp_set = set()
            temp_set.add(params['user_id'])
            self.room_user_dict[params['room_id']] = {
                'user_id_list': temp_set
            }

        self.user_dict[params['user_id']] = self

        # 判断是否开始游戏
        result = yield ServiceManager.do_service(
            'game.service',
            'is_game_start',
            {
                'room_id': params['room_id'],
                'user_nums': len(self.room_user_dict[params['room_id']]['user_id_list'])
            }
        )
        if result['code'] == 0:

            current_users = []

            for user_id in self.room_user_dict[params['room_id']]['user_id_list']:
                current_users.append(self.user_dict[user_id])
            # 游戏开始
            yield ServiceManager.do_service(
                'game.service',
                'game_start',
                {
                    'room_id': params['room_id'],
                    'users': current_users
                }
            )
        raise tornado.gen.Return(True)

        # for user in self.users:
        #     user.write_message(
        #         u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    @tornado.gen.coroutine
    def on_message(self, message):
        pass
        # for u in self.users:  # 向在线用户广播消息
        #     u.write_message(u"[%s]-[%s]-说：%s" % (
        #     self.request.remote_ip,
        #     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #     message))

    @tornado.gen.coroutine
    def check_origin(self, origin):
        return True

    @tornado.gen.coroutine
    def on_close(self):
        pass
        # self.users.remove(self)  # 用户关闭连接后从容器中移除用户
        # for u in self.users:
        #     u.write_message(
        #         u"[%s]-[%s]-离开聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def get_params(self, key=""):
        """
        获取请求参数
        如果只有一个值，将其转为字符串，如果是list，保留list类型
        @:param key 参数名称
        @:param data_type 返回数据类型，默认
        """
        if not key:
            result = {}
            data = self.request.arguments
            for (k, v) in data.items():
                if len(v) > 1:
                    value_strip = []
                    for item in v:
                        value_strip.append(item.strip())
                    result[k] = value_strip
                else:
                    result[k] = v[0].strip().decode('utf-8')
            return result
        else:
            try:
                value = self.request.arguments[key]
                if len(value) > 1:
                    value_strip = []
                    for item in value:
                        value_strip.append(item.strip())
                    return value_strip
                else:
                    return value[0].strip().decode('utf-8')
            except Exception as e:
                return ''

