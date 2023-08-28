#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2023 datavita.com.cn, Inc. All Rights Reserved
#
########################################################################


"""
File: run_concurrent.py
Author: wangjiangfeng(wangjiangfeng@hcyjs.com)
Date: 2023/8/18 12:45:26
"""
import time
import random

from concurrent.futures import ThreadPoolExecutor
from typing import Generator, Any, Optional, Callable, Tuple


def task_1(path):
    time.sleep(random.randint(1, 5))
    print("task_1")
    print(path)


def task_2(path):
    time.sleep(random.randint(1, 5))
    print("task_2")
    print(path)


def task_3(path):
    time.sleep(random.randint(1, 5))
    print("task_3")
    print(path)


def task_4(path):
    time.sleep(random.randint(1, 5))
    print("task_4")
    print(path)


gen_funcs = (
    task_1, task_2, task_3, task_4
)


class FactorCalculateTask(object):

    def __init__(self, factor):
        self._factor = factor

    def __call__(self, path, fields, **kwargs):
        print("process factor: {}".format(self._factor))
        ret = random.randint(1, 5)
        time.sleep(ret)
        return ret

    def _calculate_ic(self):
        """计算IC"""
        pass

    def _calculate_hitrate(self):
        """计算胜率"""
        pass

    def _calculate_return(self):
        """计算收益、仅3个月、6个月、1年、3年、5年收益率和CAGR"""
        pass

    def _calculate_wealth(self):
        """计算净值"""
        pass

    def _calculate_turnover(self):
        """计算换手率"""
        pass

    def _calculate_coverage(self):
        """计算覆盖率"""
        pass

    def _get_summary(self):
        pass

    def _graph_ic_month(self):
        pass

    def _graph_ic_industry(self):
        pass

    def _graph_hit_rate_10bin(self):
        pass

    def _sf_report(self):
        pass


other = dict()
other['compression'] = 9
with ThreadPoolExecutor(max_workers=2) as executor:
    futures = []
    for fac in ['factor_{}'.format(i) for i in range(1, 20)]:
        future = executor.submit(FactorCalculateTask(fac), "/data/quant", "['', '']", **other)
        futures.append(future)
    executor.shutdown(wait=True)
    for future in futures:
        print(future.result())



