# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 2020-02-03 20:11
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
    def is_game_start(self, params):
        """
        根据房间id和当前参与人数判断游戏是否开始
        :param params:
        :return: 
        """
        if self.common_utils.is_empty(['room_id', 'user_nums'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        if params['user_nums'] == 1:
            raise self._grs()

        raise self._gre('ROOM_USERS_NOT_ENOUGH')

    @tornado.gen.coroutine
    def game_start(self, params):
        """
        游戏开始，通知当前房间的所有参与者
        :param params:
        :return:
        """
        if self.common_utils.is_empty(['room_id', 'users'], params):
            raise self._gre('PARAMS_NOT_EXIST')
        # 初始化卡池
        yield self.do_service(
            'champion.service',
            'init_champion',
            {
                'room_id': params['room_id']
            }
        )

        # 通知所有游戏参与者
        for user in params['users']:
            user.write_message('game start')

        raise self._grs()
