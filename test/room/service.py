# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 2020-02-03 19:11
"""
from test.tester import Tester


class MyTest(Tester):

    def query_room_list(self):
        # 退款成功
        self.path = 'room.service'
        self.method = 'query_room_list'
        self.params = {
            'user_id': ''
        }

    def create_room(self):
        # 退款成功
        self.path = 'room.service'
        self.method = 'create_room'
        self.params = {
            'user_id': ''
        }

    def update_room(self):
        # 退款成功
        self.path = 'room.service'
        self.method = 'update_room'
        self.params = {
            'user_id': ''
        }


if __name__ == '__main__':
    refund = MyTest()
    refund.run('update_room')
