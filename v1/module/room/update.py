# -*- coding:utf-8 -*-

"""
@author: delu
@file: update.py
@time: 2020-02-03 19:07
"""

from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (None, False)

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        res = yield self.do_service('room.service', 'update_room', params=params)
        self.out(res)
