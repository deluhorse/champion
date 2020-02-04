# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 2020-02-03 19:18
"""
import tornado.gen
from base.service import ServiceBase


class Service(ServiceBase):
    """
    service
    """
    model = None
    app_id = 'wx15e3d5e7eafd86e2'
    app_secret = 'e007a32a3c13dcf84d7c177bbc3e4522'

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        pass

    @tornado.gen.coroutine
    def login(self, params):
        """
        小程序登陆获取open_id
        :param params:
        :return: 
        """
        if self.common_utils.is_empty(['code'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        result = yield self.httputils.get(
            'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(
                self.app_id,
                self.app_secret,
                params['code']
            ),
            is_json=True
        )

        self.logger.info(result)

        if 'errcode' in result:
            raise self._gr({
                'code': result['errcode'],
                'msg': result['errmsg']
            })

        raise self._grs(result)
