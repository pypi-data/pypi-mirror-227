# -*- coding: utf-8 -*-
# @Time    : 26/08/2023
# @Author  : nzooherd
# @File    : collection.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
from typing import Sequence, Iterator


def bulk_to_batch(seq: Sequence, batch_size: int) -> Iterator[Sequence]:
    """
    Segment bulk data to small batch data
    :param seq:
    :type seq:
    :param batch_size:
    :type batch_size:
    :return:
    :rtype:
    """
    start = 0
    while start < len(seq):
        yield seq[start: start + batch_size]
        start += batch_size



