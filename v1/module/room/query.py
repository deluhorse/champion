# -*- coding:utf-8 -*-

"""
@author: delu
@file: query.py
@time: 2020-02-03 17:40
"""

from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (None, False)

    @tornado.gen.coroutine
    def get(self):
        params = self.params()
        res = yield self.do_service('room.service', 'query_room_list', params=params)
        self.out(res)
