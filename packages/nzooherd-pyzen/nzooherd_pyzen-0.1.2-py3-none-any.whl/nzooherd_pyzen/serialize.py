# -*- coding: utf-8 -*-
# @Time    : 23/08/2023
# @Author  : nzooherd
# @File    : serialize.py
# @Software: PyCharm
# -*- coding: utf-8 -*-

import json


class Serializable:
    """
    A Decoration that enables a Class to be serializable.
    """

    def __init__(self, cls):
        self.cls = cls

        # 添加序列化方法
        def serialize(instance):
            return json.dumps(instance.__dict__)
        self.cls.serialize = serialize

    def __call__(self, *args, **kwargs):
        return self.cls(*args, **kwargs)

    def deserialize(self, json_data):
        """
        反序列化
        :param json_data:
        :return:
        """
        instance = self.cls()
        instance.__dict__ = json.loads(json_data)
        return instance

