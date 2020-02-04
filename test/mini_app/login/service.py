# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 2020-02-03 19:26
"""
from test.tester import Tester


class MyTest(Tester):
    def login(self):
        # 退款成功
        self.path = 'mini_app.login.service'
        self.method = 'login'
        self.params = {
            'code': '003YICY317frHP1hkZY317JzY31YICY6',
        }


if __name__ == '__main__':
    refund = MyTest()
    refund.run('login')
