#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2023 datavita.com.cn, Inc. All Rights Reserved
#
########################################################################


"""
File: fac_backtest.py
Author: wuyiyang(wuyiyang@hcyjs.com), ....
Date: 2023/8/28 10:54:43
"""

import logging
from . import  fac_class as fac


def backtest_main(
        backtest_name: str,
        sd: str,
        ed: str,
        task_num: str,
        univ_name: str = "cnall",
        fdays: int = 1,
        rettype: str = "vwap30 to vwap30",
        directory_list: list = [],
        output_path: str = ''
):
    # 实例化
    loader = fac.FactorBTLoader(
        sd=sd,
        ed=ed,
        backtest_name=backtest_name,
        univ_name=univ_name,
        fdays=fdays,
        rettype=rettype,
        directory_list=directory_list,
    )

    # 数据加载与预处理
    logging.info("start factor loading")
    for d in directory_list:
        loader.load(
            directory=d,
        )
        logging.info(f"factor {d.split('/')[-1]} successfully loaded")
    loader.onlyuniv()

    logging.info("start fwdret loading")
    loader.fwdret_load()

    # 整个回测过程
    logging.info("start factor evaluation")
    evaluator = fac.FactorEvaluator(
        sd=loader.sd,
        ed=loader.ed,
        backtest_name=loader.backtest_name,
        univ_name=loader.univ_name,
        fdays=loader.fdays,
        rettype=loader.rettype,
        directory_list=loader.directory_list,
        raw=loader.container,
        fwdret=loader.fwdret1,
        output_path=output_path,
        task_num=task_num,
    )
    evaluator.initialize()
    evaluator.nextfactor()
    while evaluator.whole_processing:
        # evaluator.nextfile()
        # while evaluator.fac_processing:
        #     evaluator.evaluate()
        #     evaluator.save_lastfile()
        #     evaluator.nextfile()
        logging.info(f"factor evaluation for factor{evaluator.curfac}")
        evaluator.evaluate()
        evaluator.fac_report()
        evaluator.nextfactor()
        logging.info("--next factor")
    evaluator.output()


def run(
        backtest_name: str,
        sd: str,
        ed: str,
        task_num: str = "b",
        univ_name: str = "cnall",
        fdays: int = 1,
        rettype: str = "vwap30",
        directory_list: list = [],
        output_path: str = '/data/quant/report/factor_backtest'
):
    fac.FQDataLoader()
    backtest_main(
        backtest_name=backtest_name,
        sd=sd,
        ed=ed,
        task_num=task_num,
        univ_name=univ_name,
        fdays=fdays,
        rettype=rettype,
        directory_list=directory_list,
        output_path=output_path
    )
