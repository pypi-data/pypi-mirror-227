#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2023 datavita.com.cn, Inc. All Rights Reserved
#
########################################################################


"""
File: run_factor_backtest.py
Author: wangjiangfeng(wangjiangfeng@hcyjs.com)
Date: 2023/8/15 09:50:03
"""
import sys
import os
sys.path.append('..')

import fatbulls
from pathlib import Path


# output_path = os.path.join(Path(__file__).absolute().parent.parent, "output")
output_path = "/data/quant/report/factor_backtest/"

config = {
    'factor': {
        'base_report_dirpath': output_path,   # 可选, 因子报告输出路径
        'backtest_name': 'test_backtest',  # 可选，回测名称，可以不唯一
        'sd': '20160101',    # 回测区间，开始时间
        'ed': '20230606',  # 回测区间，结束时间
        'task_num': '101',  # 回测任务ID, 唯一，调用方传入
        'univ_name': 'cnall',      # 可选，资产集名称，默认cnall, 包括所有股票
        'fdays': 1,                # 可选     # 未来N天的收益来做Y
        'rettype': 'vwap30',       # 可选, 收益率的类型，比如：vwap30为开盘前30分钟的成交量加权的平均价
        'factor_dirs': [
            # '/data/quant/factors/DTech/DTech_volume',  # 因子路径，最后一个目录代表因子名，内部为 {DAY}.csv
            '/data/quant/factors/DTech/DTech_amt',
            '/data/quant/factors/DTech/DTech_high',
            '/data/quant/factors/DTech/DTech_ret',
            '/data/quant/factors/DTech/DTech_opn',
            '/data/quant/factors/DTech/DTech_vwap'
        ],
        "base_log_path": "/data/user/wangjiangfeng/fatbulls"
    }
}

fatbulls.run_factor_backtest(config=config)
