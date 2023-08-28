#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2023 datavita.com.cn, Inc. All Rights Reserved
#
########################################################################


"""
File: __init__.py.py
Author: wangjiangfeng(wangjiangfeng@hcyjs.com)
Date: 2023/8/14 16:09:11
"""
import time
import logging
import os
from functools import wraps

__all__ = [
    '__version__', 'run_factor_backtest', 'run_portfolio_backtest', 'time_cost'
]


def time_cost(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        begin_time = time.perf_counter()
        result = func(*args, **kwargs)
        start_time = time.perf_counter()
        tips = '函数: %r 耗时: %2.4f 秒' % (func.__name__, start_time - begin_time)
        logging.info(tips)
        print(tips)
        return result
    return wrap


@time_cost
def run_factor_backtest(**kwargs):
    """
    传入约定函数和因子配置运行回测。约定函数详见 API 手册约定函数部分，可用的配置项详见参数配置部分。

    :Keyword Arguments:
        * **config** (dict) -- 策略配置字典

    :return: dict

    """
    from rqalpha.utils.functools import clear_all_cached_functions
    from rqalpha.utils.config import parse_config
    from fatbulls import main

    config = kwargs.get('config', None)
    if config is None:
        config = {}
    else:
        if isinstance(config, dict):
            try:
                del config["base"]["strategy_file"]
                logging.warning("delete strategy_file successfully!")
            except KeyError as e:
                logging.info("base strategy_file not found")
    fatbulls_config_path = kwargs.get('config_path', None)
    if fatbulls_config_path is None:
        fatbulls_config_path = os.path.join(os.path.dirname(__file__), 'resource/fatbulls_config.yml')
    config = parse_config(config, config_path=fatbulls_config_path)
    clear_all_cached_functions()

    return main.run(config)


@time_cost
def run_portfolio_backtest(**kwargs):
    """
    投资组合回测

    :Keyword Arguments:
        * **config** (dict) -- 组合回测配置字典

    :return: dict

    """

    pass


__version__ = '0.0.1'

