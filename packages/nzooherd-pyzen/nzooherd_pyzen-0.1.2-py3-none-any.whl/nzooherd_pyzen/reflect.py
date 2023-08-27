# -*- coding: utf-8 -*-
# @Time    : 22/08/2023
# @Author  : nzooherd
# @File    : reflect.py 
# @Software: PyCharm
# -*- coding: utf-8 -*-
import logging
import sys

logger = logging.getLogger(__name__)


def reflect_class_by_cls_method(func):
    """
    通过函数获取函数所在的类
    :param func:
    :return:
    """
    func_modules = func.__module__.split(".")
    func_names = func.__qualname__.split(".")
    if len(func_names) != 2:
        logger.error("The func %s is not valid class func." % func)

    target_module = sys.modules[func_modules[0]] or __import__(func_modules[0])

    for module_index in range(1, len(func_modules)):
        target_module = getattr(target_module, func_modules[module_index], None) or \
                        __import__(".".join(func_modules[0:module_index+1]))
        if not target_module:
            logger.error("The func %s is not valid class func." % func)

    return getattr(target_module, func_names[0])

