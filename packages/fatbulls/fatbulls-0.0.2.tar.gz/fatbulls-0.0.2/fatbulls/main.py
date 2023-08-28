#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2023 datavita.com.cn, Inc. All Rights Reserved
#
########################################################################


"""
File: main.py
Author: wangjiangfeng(wangjiangfeng@hcyjs.com)
Date: 2023/8/14 17:30:51
"""

import logging
import pandas as pd
from .context import FatbullsFactorContext
from .utils import init_fqdatac_env
from .utils.logger import init_logging
from .factor.back_test import FactorBackTestEngine
from .factor.back_test import BackTestConfig
from .factor.se import fac_backtest


def set_pandas_options():
    pd.set_option("display.max_columns", 100)
    pd.set_option("display.width", 1000)
    pd.set_option("display.max_colwidth", 100)
    pd.set_option("display.float_format", lambda x: "%.4f" % x)


def init_fqdatac(fqdatac_uri):
    if fqdatac_uri in ["disabled", "DISABLED"]:
        return
    try:
        import fqdatac
    except ImportError:
        return
    if isinstance(fqdatac.client.get_client(), fqdatac.client.DummyClient):
        init_fqdatac_env(fqdatac_uri)
        try:
            fqdatac.init()
        except Exception as e:
            logging.warning('fqdatac init failed, some apis will not function properly: {}'.format(str(e)))


def _execute_factor_backtest(backtest_config: BackTestConfig, report_path: str = ''):
    fac_backtest.run(backtest_config.backtest_name,
                     sd=backtest_config.sd,
                     ed=backtest_config.ed,
                     task_num=backtest_config.task_num,
                     univ_name=backtest_config.univ_name,
                     fdays=backtest_config.fdays,
                     rettype=backtest_config.rettype,
                     directory_list=backtest_config.factor_dirs,
                     output_path=report_path
    )


def run(config=None, app_name='fatbulls_factor_backtest', user_funcs=None, set_pandas=True):
    try:
        if set_pandas:
            """pandas 设置"""
            set_pandas_options()
        if config.factor.base_log_path:
            app_dir = config.factor.base_log_path
        else:
            app_dir = None
        init_logging(app_name, app_dir)
        init_fqdatac(getattr(config.base, 'fqdatac_uri', None))
        fat_ctx = FatbullsFactorContext(config)
        factor_conf = fat_ctx.get_factor_config()
        fat_ctx.get_base_report_dirpath()
        logging.info("---start factor evaluation---")
        _execute_factor_backtest(factor_conf, fat_ctx.get_base_report_dirpath())
        logging.warning(f"All done")
        # engine = FactorBackTestEngine(factor_conf)
        # """第一步初始化"""
        # engine.initialize()
        # """数据加载与预处理"""
        # engine.load_factors()
        # """执行回测逻辑"""
        # engine.run(max_workers=10)
        #
        #
        # # 整个回测过程
        # logging.info("start factor evaluation")
        # evaluator = FactorEvaluator(
        #     sd=loader.sd,
        #     ed=loader.ed,
        #     backtest_name=loader.backtest_name,
        #     univ_name=loader.univ_name,
        #     fdays=loader.fdays,
        #     rettype=loader.rettype,
        #     directory_list=loader.directory_list,
        #     raw=loader.container,
        #     fwdret=loader.fwdret1,
        #     output_path=factor_conf.base_report_dirpath,
        #     task_num=factor_conf.task_num
        # )
        # evaluator.initialize()
        # evaluator.nextfactor()
        # while evaluator.whole_processing:
        #     logging.info(f"factor evaluation for factor{evaluator.curfac}")
        #     evaluator.evaluate()
        #     evaluator.fac_report()
        #     evaluator.nextfactor()
        # evaluator.output()
    except Exception as e:
        raise e


