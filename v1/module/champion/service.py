# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 2020-02-01 15:30
"""
import tornado.gen
import copy
from base.service import ServiceBase


class Service(ServiceBase):
    """
    service
    """
    temp = [4, 1, 6, 5, 3, 2]

    base_all = [
        {
            'name': '状元',
            'num': 1,
            'value': 32,
            'patten': [
                # 六驳
                '6 6 6 6 6 6',
                '5 5 5 5 5 5',
                '4 4 4 4 4 4',
                '3 3 3 3 3 3',
                '2 2 2 2 2 2',
                '1 1 1 1 1 1',

                '4 4 4 4 4 1',   # 五红幺
                '4 4 4 4 4 6',   # 五红六
                '4 4 4 4 4 5',   # 五红五
                '4 4 4 4 4 3',   # 五红三
                '4 4 4 4 4 2',   # 五红二

                # '4 4 4 4 * *',   #

                '1 1 1 1 1 *',
                '2 2 2 2 2 *',
                '3 3 3 3 3 *',
                '5 5 5 5 5 *',
                '6 6 6 6 6 *',

                '4 4 4 4 1 3',   # 和牌
                '4 4 4 4 2 2',   # 变二
                '6 6 6 6 2 4',   # 二四锦
                '6 6 6 6 1 5',   # 幺五锤
                '6 6 6 6 3 3',   # 双飘带
                '5 5 5 5 1 4',   # 红鸡
                '5 5 5 5 2 3',   # 黑鸡
                '3 3 3 3 1 2',   # 虾饺三
                '2 2 2 2 1 1',   # 孩儿十

                '4 4 4 4 6 6',   # 天牌
                '4 4 4 4 5 6',   # 虎头(十一点)
                '4 4 4 4 5 5',   # 梅花(十点)
                '4 4 4 4 3 6',   # 九点(九哥)
                '4 4 4 4 3 5',   # 八点(八子)
                '4 4 4 4 2 6',
                '4 4 4 4 2 5',   # 七点
                '4 4 4 4 1 5',   # 六点
                '4 4 4 4 3 3',   # 六点(斜三)
                '4 4 4 4 2 3',   # 五点(五子)
                '4 4 4 4 1 2',   # 三点(三丁)
                '4 4 4 4 1 1'    # 二点(地牌)
            ]
        },
        {
            'name': '三红加豹子',
            'num': 0,
            'value': 24,
            'patten': [
                '4 4 4 -3'
            ]
        },
        {
            'name': '榜眼(豹子)',
            'num': 2,
            'value': 16,
            'patten': [
                '-3 -3',
                '1 2 3 4 5 6',
                '1 1 2 2 3 3',
                '4 4 5 5 6 6'
            ]
        },
        {
            'name': '会元',
            'num': 4,
            'value': 8,
            'patten': [
                '4 4 4 * * *'
            ]
        },
        {
            'name': '进士带二举',
            'num': 0,
            'value': 6,
            'patten': [
                '1 1 1 1 4 4',
                '2 2 2 2 4 4',
                '3 3 3 3 4 4',
                '5 5 5 5 4 4',
                '6 6 6 6 4 4'
            ]
        },
        {
            'name': '进士带一秀',
            'num': 0,
            'value': 5,
            'patten': [
                '1 1 1 1 4 *',
                '2 2 2 2 4 *',
                '3 3 3 3 4 *',
                '5 5 5 5 4 *',
                '6 6 6 6 4 *'
            ]
        },
        {
            'name': '进士',
            'num': 8,
            'value': 4,
            'patten': [
                '1 1 1 1 * *',
                '2 2 2 2 * *',
                '3 3 3 3 * *',
                '5 5 5 5 * *',
                '6 6 6 6 * *'
            ]
        },
        {
            'name': '举人',
            'num': 16,
            'value': 2,
            'patten': [
                '4 4 * * * *'
            ]
        },
        {
            'name': '秀才',
            'num': 32,
            'value': 1,
            'patten': [
                '4 * * * * *'
            ]
        }
    ]

    room_base_all_dict = {}

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        pass

    @tornado.gen.coroutine
    def init_champion(self, params):
        """
        初始化当前房间的卡池
        :param params:
        :return:
        """
        if self.common_utils.is_empty(['room_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')
        self.room_base_all_dict[params['room_id']] = copy.deepcopy(self.base_all)

        raise self._grs()

    @tornado.gen.coroutine
    def query_champion(self, params):
        """
        查询所欲对象
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['user_id', 'room_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')
        # 生成随机数
        touzi = []
        for x in range(6):
            touzi.append(self.salt(1, is_num=True))
        if not params.get('touzi'):
            params['touzi'] = touzi
        result = yield self.check_patten(params)
        if result['code'] != 0:
            result['data'] = {
                'touzi': params['touzi']
            }
            raise self._gr(result)

        raise self._grs({
            'entity_list': result['data']['entity_list'],
            'touzi': params['touzi'],
            'left': self.room_base_all_dict[params['room_id']],
            'name': result['data']['name']
        })

    @tornado.gen.coroutine
    def check_patten(self, params):
        if isinstance(params['touzi'], str):
            params['touzi'] = self.common_utils.loads_json(params['touzi'])

        params['touzi'].sort()

        for entity in self.room_base_all_dict[params['room_id']]:

            for patten in entity['patten']:
                temp_touzi = params['touzi'].copy()
                temp_patten = patten.split(" ")
                current_index = 0
                right_num = 0
                while current_index < 6:
                    if right_num == 6:

                        if entity['num'] >= 0:
                            entity['num'] -= 1
                        final_entity = self.adapt_chips(entity, params['room_id'])
                        raise self._grs({
                            'entity_list': final_entity,
                            'name': entity['name']
                        })
                    try:
                        if temp_touzi[current_index] in temp_patten:
                            old_value = temp_touzi.pop(current_index)
                            temp_patten.remove(old_value)
                            right_num += 1
                        elif '*' in temp_patten:
                            temp_touzi.pop(current_index)
                            temp_patten.remove('*')
                            right_num += 1
                        elif '-3' in temp_patten:
                            # 剩余的数中至少要有三个一样的
                            final_value = self.find_sample_num(temp_touzi, 3)
                            if final_value:
                                temp_patten.remove('-3')
                                for i in range(3):
                                    temp_touzi.remove(final_value)

                                right_num += 3
                            else:
                                break
                        else:
                            break

                    except Exception as e:
                        self.logger.exception(e)

        raise self._gre('CHAMPION_NOT_EXIST')

    def find_sample_num(self, touzi_list, count):
        """
        检查数组中是否存在count个相同的数，如果存在则移除数组
        :param touzi:
        :param count:
        :return:
        """
        touzi_dict = {}
        final_value = ''

        for touzi in touzi_list:
            if touzi not in touzi_dict:
                touzi_dict[touzi] = 1
            else:
                touzi_dict[touzi] += 1

        for key, value in touzi_dict.items():

            if value == count:
                final_value = key
                break

        return final_value

    def adapt_chips(self, params, room_id):
        """
        匹配筹码
        如果没有当前筹码，则用低级的筹码去拼凑
        如果剩余筹码不足，则将剩余筹码全部返回
        :param params:
        :param room_id
        :return:
        """
        if params['num'] >= 0:
            return [{
                'name': params['name'],
                'num': 1,
                'value': params['value']
            }]
        final_entity_list = []
        current_value = 0
        # 用低级筹码去拼凑
        right = False
        for entity in self.room_base_all_dict[room_id]:

            if not right and entity['name'] != params['name']:
                continue
            elif not right:
                right = True
                continue

            if right:
                if current_value == params['value']:
                    return final_entity_list
                elif entity['num'] <= 0:
                    continue
                else:
                    max_current_num = (params['value'] - current_value) // entity['value']

                    if not max_current_num:
                        continue

                    if entity['num'] >= max_current_num:
                        entity['num'] -= max_current_num
                        current_value += max_current_num * entity['value']
                        final_entity_list.append({
                            'name': entity['name'],
                            'num': max_current_num,
                            'value': entity['value']
                        })
                    else:
                        current_value += entity['num'] * entity['value']
                        final_entity_list.append({
                            'name': entity['name'],
                            'num': entity['num'],
                            'value': entity['value']
                        })
                        entity['num'] = 0

        return final_entity_list






