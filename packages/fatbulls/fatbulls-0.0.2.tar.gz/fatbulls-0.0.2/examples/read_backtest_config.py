#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2023 datavita.com.cn, Inc. All Rights Reserved
#
########################################################################


"""
File: read_backtest_config.py
Author: wangjiangfeng(wangjiangfeng@hcyjs.com)
Date: 2023/8/16 15:50:03
"""

from fatbulls.models.factor_model import BackTestConfig


if __name__ == "__main__":
    backtest_config = BackTestConfig('20230101', '20230701', factor_dirs=[
        '/data/quant/factors/DTech/DTech_volume',
        '/data/quant/factors/DTech/DTech_amt'])
    print(backtest_config.today)
    print(backtest_config.sd)
    print(backtest_config.ed)
    print(backtest_config.factor_dirs)
