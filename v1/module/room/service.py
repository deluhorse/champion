# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 2020-02-02 20:51
"""
import tornado.gen
from base.service import ServiceBase


class Service(ServiceBase):
    """
    service
    """
    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        pass

    @tornado.gen.coroutine
    def query_room_list(self, params):
        """
        查询房间列表
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['user_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        room_id = yield self.redis.get('room_id')

        if not room_id:
            raise self._gre('ROOM_NOT_EXIST')

        raise self._grs({
            'room_id': room_id
        })

    @tornado.gen.coroutine
    def create_room(self, params):
        """
        创建房间
        :param params:
        :return:
        """
        if self.common_utils.is_empty(['user_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        room_id = yield self.redis.get('room_id')

        if room_id:
            raise self._gre('ROOM_EXIST')

        room_id = self.salt(6)
        yield self.redis.set('room_id')

        raise self._grs({
            'room_id': room_id
        })

    @tornado.gen.coroutine
    def update_room(self, params):
        """
        更新房间
        :param params:
        :return:
        """
        if self.common_utils.is_empty(['user_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        room_id = yield self.redis.get('room_id')

        if not room_id:
            raise self._gre('ROOM_NOT_EXIST')

        yield self.redis.sadd('room:%s'.format(room_id), params['user_id'])

        raise self._grs({
            'room_id': room_id
        })
