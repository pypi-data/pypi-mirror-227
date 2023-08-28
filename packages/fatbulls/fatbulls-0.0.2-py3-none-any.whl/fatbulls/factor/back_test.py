#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2023 datavita.com.cn, Inc. All Rights Reserved
#
########################################################################


"""
File: backtest.py
Author: wuyiyang(wuyiyang@hcyjs.com), wangjiangfeng(wangjiangfeng@hcyjs.com)
Date: 2023/8/15 11:18:01
"""
import os
import fqdatac
import logging
import pandas as pd
import numpy as np
from typing import List
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, Future
from . import FactorBackTestException
from ..models.factor_model import BackTestConfig
from ..context import FatbullsFactorContext

"""基础变量"""
FIRST_DAY = 0
LAST_ONE_DAY = -1
LAST_ONE_MONTH = -22
LAST_THREE_MONTH = -64
LAST_ONE_YEAR = -245
LAST_THREE_YEAR = -490
LAST_FIVE_YEAR = -1225
DAYS_PER_YEAR = 244


"""
'output_dirpath': output_path,   # 可选
        'backtest_name': 'test_backtest',
        'sd': '20170101',
        'ed': '20201231',
        'task_num': 'WaitForOne',  # 可选
        'univ_name': 'cnall',      # 可选
        'fdays': 1,                # 可选
        'rettype': 'vwap30',       # 可选
        'directory_list': [
            '/data/quant/factors/DTech/DTech_volume',
            '/data/quant/factors/DTech/DTech_amt',
            '/data/quant/factors/DTech/DTech_high',
            '/data/quant/factors/DTech/DTech_ret',
            '/data/quant/factors/DTech/DTech_logret',
            '/data/quant/factors/DTech/DTech_opn',
            '/data/quant/factors/DTech/DTech_vwap'
        ],
"""


class FactorBackTestBase(object):
    """ 回测引擎基类 """

    def __init__(self):
        self.today = datetime.now().strftime("%Y%m%d")
        self.backtest_day = datetime.now().strftime("%Y%m%d")


class FactorBackTestEngine(FactorBackTestBase):
    """因子回测主引擎"""

    def __init__(self, backtest_config: BackTestConfig):
        """回测参数初始化"""
        FactorBackTestBase.__init__(self)
        self.start_date = backtest_config.sd
        self.end_date = backtest_config.ed
        self.task_num = backtest_config.task_num
        self.backtest_name = backtest_config.backtest_name
        self.univ_name = backtest_config.univ_name
        self.forward_days = backtest_config.fdays
        self.return_type = backtest_config.rettype
        self.factor_dirs = backtest_config.factor_dirs

        """Context"""
        self._fbctx = FatbullsFactorContext.get_instance()

        """回测fqdatac相关数据"""
        self.alldays = None
        self.univ = None
        self.cnall = None

        """ 回测数据容器 """
        self.factors = {}
        self.factor_data = {}

        """对照股票的return数据"""
        self.forward_return1 = None
        self.forward_return = None

    def initialize(self):
        """
        第一步：初始化文件检查
        """
        self._check_date()
        self._fbctx.set_alldays(fqdatac.get_daysrange(self.start_date, self.end_date))
        self._fbctx.set_univ_userselect(Universe(self.univ_name, self.start_date, self.end_date))
        self._fbctx.set_univ_cnall(Universe('cnall', self.start_date, self.end_date))

    def load_factors(self):
        """
        第二步： 数据加载预处理
        将因子load进container
        查路径里的文件是否齐全 是否重复
        """
        logging.info("start factor loading")
        for dirpath in self.factor_dirs:
            factor_name = os.path.basename(dirpath)
            factor = Factor(factor_name, dirpath)
            self.factors[factor_name] = factor
            self.factor_data[factor_name] = factor.load_data(use_cache=False)
            logging.info("factor:{} successfully loaded".format(factor_name))
        self._only_univ_filter()
        logging.info("start fwdret loading")
        self._load_fwdret()

    def _only_univ_filter(self):
        """
        只保留当天在universe中的股票进行测试
        """
        univ = self._fbctx.get_univ_userselect()
        for k, v in self.factor_data.items():
            for dt in list(v.keys()):
                v[dt] = v[dt][v[dt]["K"].isin(list(univ.data[dt]["K"]))]

    def _load_fwdret(self):
        """
        获取对照的股票return数据
        """
        self.forward_return = fqdatac.get_bfwd(
            sd=self.start_date,
            ed=self.end_date,
            univ_name=self.univ_name,
            ret_type=self.return_type,
            dayshift=self.forward_days,
        )
        if self.forward_days == 1:
            self.forward_return1 = self.forward_return.copy()
        else:
            self.forward_return1 = fqdatac.get_bfwd(
                sd=self.start_date,
                ed=self.end_date,
                univ_name=self.univ_name,
                ret_type=self.return_type,
                dayshift=1,
            )

    def run(self, max_workers=10):
        """回测主函数"""
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures: List[Future] = []
            for factor_name in self.factors.keys():
                factor_data = pd.concat(self.factor_data[factor_name].values(), ignore_index=True)
                factor_data = pd.merge(factor_data, self.forward_return, on=['K', 'D', 'T'], how='left')
                future = executor.submit(FactorCalculateTask(factor_name, factor_data))
                futures.append(future)
                del factor_data
            executor.shutdown(wait=True)
            self.save_report(futures)

    def save_report(self, futures: List[Future]):
        cols = ['Coverage', 'ICs', 'SCs']
        ls_cols = ['Summary', 'Turnover', 'LSreturns', 'Wealth', 'HitRate']
        sheet_names = cols + [f'top_{s}'for s in ls_cols] + [f'bottom_{s}' for s in ls_cols]
        combine_data = dict()
        for future in futures:
            backtest_result = future.result()
            for sheet_name in sheet_names:
                if 'Summary' in sheet_name:
                    if sheet_name not in combine_data:
                        combine_data[sheet_name] = list()
                    combine_data[sheet_name].append(backtest_result[sheet_name])
                else:
                    if sheet_name not in combine_data:
                        combine_data[sheet_name] = pd.DataFrame()
                    df_right = backtest_result[sheet_name].set_index(['D', 'T'])
                    combine_data[sheet_name] = pd.concat([combine_data[sheet_name], df_right], axis=1)
        report_path = self.get_report_path()
        file_name = "BT_factor_report_{}_{}_{}_{}_{}.xlsx".format(self.today, self.task_num, self.univ_name,
                                                                  self.start_date, self.end_date)
        file_name = "{}/{}".format(report_path, file_name)
        with pd.ExcelWriter(file_name) as writer:
            for sheet_name in combine_data:
                if 'Summary' in sheet_name:
                    df_sheet = pd.DataFrame.from_dict(combine_data[sheet_name])
                else:
                    df_sheet = combine_data[sheet_name].reset_index(['D', 'T'])
                df_sheet.to_excel(writer, sheet_name=sheet_name)

    def _check_date(self):
        try:
            assert fqdatac.get_day(self.end_date, -60) >= self.start_date
            assert self.end_date <= fqdatac.get_day(self.backtest_day, -1)
        except AssertionError:
            raise FactorBackTestException("invalid date range inputs")

    def get_report_path(self):
        report_path = self._fbctx.get_base_report_dirpath()
        report_path = os.path.join(report_path, self.task_num)
        if not os.path.exists(report_path):
            os.makedirs(report_path, exist_ok=True)
        return report_path


class FactorCalculateTask(object):
    """多线程执行引擎"""

    def __init__(self, factor_name: str, factor_data: pd.DataFrame):
        self.factor_name = factor_name
        self.factor_data = factor_data
        self._factor_config = FatbullsFactorContext.get_instance().get_factor_config()
        self.forward_return_name = list(factor_data.columns)[-1]
        self.factor_forward = self.factor_name + '_' + self.forward_return_name
        self.grouped = None
        self.df_longshort = None
        self.backtest_result = dict()
        self.coverage = dict()

    def _middle_calculate(self):
        self.factor_data = self.factor_data.sort_values(by=['D', 'T', 'K'], axis=0, ascending=True)
        self.grouped = self.factor_data.groupby(by=['D', 'T'], as_index=False)
        self.factor_data['q'] = self.factor_data.groupby(by=['D', 'T'], as_index=False)[self.factor_name].transform(
            lambda x: pd.qcut(x, 10, labels=["Q{}".format(i) for i in range(1, 11)]))
        self.factor_data['q'] = self.factor_data['q'].astype(str)
        self.df_longshort = self.factor_data.query("q == 'Q1' or q == 'Q10'")

    def __call__(self, *args, **kwargs):
        self.backtest_result['factor_name'] = self.factor_name
        self._middle_calculate() # noqa
        self._coverage_summary()
        self.calculate_ic()
        self.calculate_coverage()
        self.calculate_turnover()
        self.calculate_lsreturn()
        self.calculate_hitrate()
        self.calculate_wealth()
        # calculate_serial_corr和summary计算顺序不能反
        self.calculate_serial_corr()
        self.summary()
        self.summary(summary_type="top")
        self.summary(summary_type="bottom")
        del self.factor_data
        return self.backtest_result

    def calculate_ic(self):
        """4.1 计算IC相关性, 不区分LongShort"""
        df_ic = self.grouped.apply(lambda x: x[self.factor_name].corr(x[self.forward_return_name], 'spearman'))
        df_ic.columns = ['D', 'T', self.factor_forward]
        self.backtest_result['ICs'] = df_ic
        del df_ic

    def calculate_coverage(self):
        """4.1 计算coverage, 不区分LongShort"""
        df_coverage = self.grouped.agg({'K': 'count'})
        df_coverage = df_coverage.rename(columns={"K": self.factor_name})
        df_coverage = df_coverage[['D', 'T', self.factor_name]].rename(columns={self.factor_name: self.factor_forward})
        self.backtest_result['Coverage'] = df_coverage
        del df_coverage

    def calculate_turnover(self):
        """
            4.1 urnover , 分为LongShort、Long、Short
            LongShort Turnover = 1 - (C1 + C10)/(S1 + S10)
            Long Turnover  = 1 - C10/S10
            Short Turnover = 1 - C1/S1
        """
        self.backtest_result['Turnover'] = self._calculate_turnover(self.df_longshort)
        self.backtest_result['top_Turnover'] = self._calculate_turnover(self.df_longshort.query("q == 'Q1'"))
        self.backtest_result['bottom_Turnover'] = self._calculate_turnover(self.df_longshort.query("q == 'Q10'"))

    def _calculate_turnover(self, df_q: pd.DataFrame):

        def _calc_turnover(x, y):
            """计算交集"""
            if x is None or y is None:
                return 1.0
            return 1.0 - len(set(x).intersection(set(y))) / (len(x) + len(y))

        df_q = df_q.groupby(['D', 'T'], as_index=False).agg({"K": list})
        df_q.columns = ['D', 'T', 'K_list']
        df_q['K_list_prev'] = df_q.sort_values(by=['D', 'T'], ascending=True)['K_list'].shift(1)
        df_q[self.factor_name] = df_q.apply(lambda x: _calc_turnover(x['K_list'], x['K_list_prev']), axis=1)
        df_q = df_q[['D', 'T', self.factor_name]].rename(columns={self.factor_name: self.factor_forward})
        return df_q

    def calculate_lsreturn(self):
        """4.4 LongShort部分之计算LSreturn"""
        df_lsreturn = self.df_longshort.groupby(by=['D', 'T', 'q'], as_index=False)[self.forward_return_name].mean()
        df_lsreturn = df_lsreturn.pivot(index=['D', 'T'], columns='q', values=self.forward_return_name).reset_index()
        df_lsreturn['LSreturns'] = df_lsreturn.apply(lambda row: row['Q10'] - row['Q1'], axis=1)
        self.backtest_result['LSreturns'] = df_lsreturn[['D', 'T', 'LSreturns']].rename(columns={"LSreturns": self.factor_forward})
        self.backtest_result['top_LSreturns'] = df_lsreturn[['D', 'T', 'Q10']].rename(columns={"Q10": self.factor_forward})
        self.backtest_result['bottom_LSreturns'] = df_lsreturn[['D', 'T', 'Q1']].rename(columns={"Q1": self.factor_forward})
        del df_lsreturn

    def calculate_hitrate(self):
        """4.5 LongShort部分之计算HitRate"""

        def _agg_calc_hitrate(arrs):
            pos_neg_len = len(arrs)
            if pos_neg_len == 0:
                return [0.0, 0.0, 0.0]
            pos_count = sum(1 if (arr[1] == 'Q1' and arr[0] > 0) else 0 for arr in arrs)
            pos_len = len([arr for arr in arrs if arr[1] == 'Q1'])
            neg_count = sum(1 if (arr[1] == 'Q10' and arr[0] < 0) else 0 for arr in arrs)
            neg_len = len([arr for arr in arrs if arr[1] == 'Q10'])
            hitrate = float((pos_count + neg_count) / pos_neg_len)
            top_hitrate = 0.0 if pos_len == 0 else float(pos_count / pos_len)
            bottom_hitrate = 0.0 if neg_len == 0 else float(neg_count / neg_len)
            return [hitrate, top_hitrate, bottom_hitrate]

        df_hitrate = self.df_longshort.copy()
        df_hitrate['FQ'] = df_hitrate.apply(lambda row: [row[self.forward_return_name], row['q']], axis=1)
        df_hitrate = df_hitrate.groupby(by=['D', 'T'], as_index=False).agg(
            hitRates=('FQ', _agg_calc_hitrate),
        )
        df_hitrate['HitRate'] = df_hitrate['hitRates'].map(lambda x: x[0])
        df_hitrate['top_HitRate'] = df_hitrate['hitRates'].map(lambda x: x[1])
        df_hitrate['bottom_HitRate'] = df_hitrate['hitRates'].map(lambda x: x[2])
        self.backtest_result['HitRate'] = df_hitrate[['D', 'T', 'HitRate']].rename(
            columns={"HitRate": self.factor_forward})
        self.backtest_result['top_HitRate'] = df_hitrate[['D', 'T', 'top_HitRate']].rename(
            columns={"top_HitRate": self.factor_forward})
        self.backtest_result['bottom_HitRate'] = df_hitrate[['D', 'T', 'bottom_HitRate']].rename(
            columns={"bottom_HitRate": self.factor_forward})
        del df_hitrate

    def calculate_wealth(self):
        """4.6 Longshort部分之Wealth模块"""
        df_lsreturn = self.backtest_result['LSreturns'].copy()
        df_lsreturn[self.factor_forward] = df_lsreturn[self.factor_forward].apply(lambda x: x+1).cumprod()
        df_lsreturn_top = self.backtest_result['top_LSreturns'].copy()
        df_lsreturn_top[self.factor_forward] = df_lsreturn_top[self.factor_forward].apply(lambda x: x+1).cumprod()
        df_lsreturn_bottom = self.backtest_result['bottom_LSreturns'].copy()
        df_lsreturn_bottom[self.factor_forward] = df_lsreturn_bottom[self.factor_forward].apply(lambda x: x+1).cumprod()
        self.backtest_result['Wealth'] = df_lsreturn
        self.backtest_result['top_Wealth'] = df_lsreturn_top
        self.backtest_result['bottom_Wealth'] = df_lsreturn_bottom
        del df_lsreturn, df_lsreturn_top, df_lsreturn_bottom

    def _coverage_summary(self):
        self.coverage['coverage_max'] = self.factor_data['K'].nunique()
        total_days = self.factor_data['D'].nunique()
        df_days = self.factor_data.groupby('K')['D'].count()
        coverage_min = len(df_days[df_days == total_days])
        self.coverage['coverage_min'] = coverage_min

    @staticmethod
    def _max_drawdown(xs: list) -> float:
        mdd = 0
        maxwealth = 1
        x = iter(xs)
        while True:
            try:
                value = next(x)
            except Exception as e:
                return mdd
            maxwealth = max(maxwealth, value)
            mdd = min(mdd, value/maxwealth - 1)

    def calculate_serial_corr(self):
        temp_df = self.factor_data.sort_values(by=['D', 'T'], ascending=True)
        temp_df = temp_df[['K', 'D', 'T', self.factor_name]]
        """获取前一天的因子序列"""
        prev_fac = pd.pivot_table(temp_df, columns='K', index=["D", "T"], values=self.factor_name).shift(1)
        prev_fac = prev_fac.unstack(['D', 'T']).reset_index()
        prev_fac.columns = ['K', 'D', 'T', 'prev_fac']
        prev_fac = prev_fac.dropna(subset=['prev_fac'])
        """滚动计算相关性"""
        temp_df = pd.merge(temp_df, prev_fac, how='left', on=['K', 'D', 'T'])
        serial_correlation = temp_df.groupby(['D', 'T']).apply(
            lambda x: x[[self.factor_name, 'prev_fac']].corr(method='spearman').iloc[0, 1])
        serial_correlation = serial_correlation.to_frame().reset_index().dropna()
        serial_correlation.columns = ['D', 'T', self.factor_forward]
        self.backtest_result['SCs'] = serial_correlation
        del temp_df

    def summary(self, summary_type="top"):
        summary = dict({
            'fac_name': self.factor_name,
            'backtest_sd': self._factor_config.sd,
            'backtest_ed': self._factor_config.ed
        })
        summary['coverage_max'] = self.coverage['coverage_max']
        summary['coverage_min'] = self.coverage['coverage_min']
        df_ic = self.backtest_result['ICs'].copy()
        if summary_type.lower() == 'top':
            df_wealth = self.backtest_result['top_Wealth'].copy()
            df_lsreturn = self.backtest_result['top_LSreturns'].copy()
            df_hitrate = self.backtest_result['top_HitRate'].copy()
            df_turnover = self.backtest_result['top_HitRate'].copy()
            summary_key = 'top_Summary'
        elif summary_type.lower() == 'bottom':
            df_wealth = self.backtest_result['bottom_Wealth'].copy()
            df_lsreturn = self.backtest_result['bottom_LSreturns'].copy()
            df_hitrate = self.backtest_result['bottom_HitRate'].copy()
            df_turnover = self.backtest_result['bottom_HitRate'].copy()
            summary_key = 'bottom_Summary'
        else:
            df_wealth = self.backtest_result['Wealth'].copy()
            df_lsreturn = self.backtest_result['LSreturns'].copy()
            df_ic = self.backtest_result['ICs'].copy()
            df_hitrate = self.backtest_result['HitRate'].copy()
            df_turnover = self.backtest_result['HitRate'].copy()
            summary_key = 'Summary'
        n_days = df_wealth.shape[0]
        btm_w = df_wealth.iloc[0, df_wealth.columns.get_loc(self.factor_forward)]
        btm_d1 = 1.0 if n_days < abs(LAST_ONE_DAY) else df_wealth.iloc[LAST_ONE_DAY, df_wealth.columns.get_loc(self.factor_forward)]
        btm_m1 = 1.0 if n_days < abs(LAST_ONE_MONTH) else df_wealth.iloc[LAST_ONE_MONTH, df_wealth.columns.get_loc(self.factor_forward)]
        btm_m3 = 1.0 if n_days < abs(LAST_THREE_MONTH) else df_wealth.iloc[LAST_THREE_MONTH, df_wealth.columns.get_loc(self.factor_forward)]
        btm_y1 = 1.0 if n_days < abs(LAST_ONE_YEAR) else df_wealth.iloc[LAST_ONE_YEAR, df_wealth.columns.get_loc(self.factor_forward)]
        btm_y3 = 1.0 if n_days < abs(LAST_THREE_YEAR) else df_wealth.iloc[LAST_THREE_YEAR, df_wealth.columns.get_loc(self.factor_forward)]
        btm_y5 = 1.0 if n_days < abs(LAST_FIVE_YEAR) else df_wealth.iloc[LAST_FIVE_YEAR, df_wealth.columns.get_loc(self.factor_forward)]
        return_z = btm_d1/btm_w - 1
        summary['return_1m'] = btm_d1/btm_m1 - 1
        summary['return_3m'] = btm_d1/btm_m3 - 1
        return_z1y = btm_d1/btm_y1 - 1
        return_z3y = btm_d1/btm_y3 - 1
        return_z5y = btm_d1/btm_y5 - 1
        summary['cagr'] = (return_z + 1) ** (DAYS_PER_YEAR / n_days) - 1
        summary['cagr_1y'] = summary['cagr'] if n_days < abs(LAST_ONE_YEAR) else return_z1y
        summary['cagr_3y'] = summary['cagr'] if n_days < abs(LAST_THREE_YEAR) else (
                (return_z3y + 1) ** (DAYS_PER_YEAR / abs(LAST_THREE_YEAR)) - 1.0)
        summary['cagr_5y'] = summary['cagr'] if n_days < abs(LAST_FIVE_YEAR) else (
                (return_z5y + 1) ** (DAYS_PER_YEAR / abs(LAST_FIVE_YEAR)) - 1.0)
        summary['volatility'] = df_lsreturn[self.factor_forward].std(ddof=1) * np.sqrt(DAYS_PER_YEAR)
        summary['sharpe_ratio'] = summary['cagr'] / summary['volatility']
        summary['rank_ic_mean'] = df_ic[self.factor_forward].mean()
        summary['rank_ic_std'] = df_ic[self.factor_forward].std(ddof=1)
        summary['ic_ir'] = summary['rank_ic_mean'] / summary['rank_ic_std']
        summary['hit_rate'] = df_hitrate[self.factor_forward].mean() * 100.0
        summary['max_drawdown'] = self._max_drawdown(df_wealth[self.factor_forward].tolist())
        summary['serial_corr'] = self.backtest_result['SCs'][self.factor_forward].mean()
        summary['turnover'] = df_turnover[self.factor_forward].mean() * 100
        cagr_res = self._cagr_summary(df_wealth)
        rank_ic_mean_res = self._rank_ic_mean_summary(df_ic)
        summary.update(cagr_res)
        summary.update(rank_ic_mean_res)
        self.backtest_result[summary_key] = summary
        del df_wealth, df_lsreturn, df_hitrate, df_turnover, df_ic

    def _cagr_summary(self, df_wealth):
        """
        CAGR算法
        """
        cagr_res = {}
        df_wealth['Y'] = df_wealth['D'].apply(lambda day: str(day)[0:4])
        df_cagr_agg = df_wealth.groupby(by=['Y'], as_index=False).agg(M=('D', 'count'), D_max=('D', 'max'))
        df_cagr_agg = pd.merge(df_cagr_agg, df_wealth[['D', self.factor_forward]], left_on='D_max', right_on='D')
        df_cagr_agg = df_cagr_agg.rename(columns={self.factor_forward: "D_max_wealth"})
        df_cagr_agg.drop('D', axis=1, inplace=True)
        df_cagr_agg['D_max_wealth_1'] = df_cagr_agg['D_max_wealth'].shift(1)
        for _, row in df_cagr_agg.iterrows():
            cagr_year_key = "cagr_year_{}".format(row['Y'])
            if str(row['D_max_wealth_1']) == 'nan':
                cagr_res[cagr_year_key] = row['D_max_wealth'] ** (
                        row['M'] / float(DAYS_PER_YEAR)) - 1.0
            else:
                cagr_res[cagr_year_key] = (row['D_max_wealth'] / row['D_max_wealth_1']) ** (
                        row['M'] / float(DAYS_PER_YEAR)) - 1.0
        return cagr_res

    def _rank_ic_mean_summary(self, df_ic):
        """
        计算 Rank IC Mean Summary
        :param df_ic:
        :return:
        """
        rank_ic_mean_res = {}
        df_ic['Y'] = df_ic['D'].apply(lambda day: str(day)[0:4])
        df_ic_agg = df_ic.groupby(by=['Y'], as_index=False).agg(rank_ic_mean_year=(self.factor_forward, 'mean'))
        for _, row in df_ic_agg.iterrows():
            rank_ic_mean_res["rank_ic_mean_year_{}".format(row['Y'])] = row['rank_ic_mean_year']
        return rank_ic_mean_res


class Factor:
    """Factor类,表示单个因子"""

    def __init__(self, factor_name, factor_path):
        self.factor_name = factor_name
        self.factor_path = factor_path
        self.files_shouldbe = self._load_factor_files(factor_path)
        self.data = None

    def _load_factor_files(self, path: str) -> list:  # noqa
        alldays = FatbullsFactorContext.get_instance().get_alldays()
        csvdays = [file.split(".")[0] for file in os.listdir(path) if file.endswith(".csv")]
        if len(csvdays) == 0:
            raise FileNotFoundError("no csv file found in path : {}".format(path))
        minday = min(csvdays)
        files_shouldbe = list()
        missing_files = list()
        for day in alldays:
            if day < minday:
                continue
            csv_file = os.path.join(path, "{}.csv".format(day))
            if os.path.isfile(csv_file):
                files_shouldbe.append(csv_file)
            else:
                missing_files.append(csv_file)
        if len(missing_files) > 0:
            raise FileNotFoundError("the following files are missing: {}".format(",".join(missing_files)))
        return files_shouldbe

    def load_data(self, use_cache=True):
        # 从数据库加载投资范围数据
        try:
            if use_cache and (self.data is not None) and (not self.data):
                return self.data
            self.data = {}
            cnall = FatbullsFactorContext.get_instance().get_univ_cnall()
            for filepath in self.files_shouldbe:
                dtcsv = pd.read_csv(filepath, header=0, sep=",")
                dtcsv["D"] = dtcsv["D"].astype(str)
                self._checkformat(filepath, dtcsv, cnall.data)  # 查一下文件结构是否符合规范
                self.data[dtcsv["D"].iloc[0]] = dtcsv  # 确保一个文件里只有一个D，已经查过了
        except Exception as e:
            raise FactorBackTestException(
                'load factor data error, factor_name:{}, msg: {}'.format(self.factor_name, str(e)))
        return self.data

    def _checkformat(self, filepath: str, df: pd.DataFrame, cnall):
        """
        查每个文件里的格式
        """
        # 查表头
        if not {"K", "D", "T", self.factor_name} == set(df.columns):
            raise KeyError("incorrect header format in file {}".format(filepath))

        # 查文件内是否有重复stock code
        df_dd = df.drop_duplicates(subset=["K"])
        if len(df_dd) < len(df):
            raise ValueError("duplicate stock codes in file {}".format(filepath))

        # 查文件内日期是否与文件名一致，是否有不同日期出现在一个文件
        dt = (filepath.split("/")[-1]).split(".")[0]
        try:
            assert max(df.D) == min(df.D) == dt
        except AssertionError:
            raise ValueError(
                "multiple dates in same file/filename doesn't match D column in file {}".format(filepath)
            )

        """ 查文件内的股票代码是否都是上市的股票 """
        stk_code = set(df_dd["K"])
        if not set(stk_code) <= set(cnall[dt]["K"]):
            raise ValueError("stock code beyond cnall exists in file {}".format(filepath))


class Universe:
    """Universe类,表示投资范围"""

    def __init__(self, name, start_date, end_date):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self._data = None

    def _partition_df(self, df: pd.DataFrame, col: str):  # noqa
        """Partition a DataFrame into a dictionary of DataFrames by column value."""
        return {k: v.reset_index(drop=True) for k, v in df.groupby(col, sort=False)}

    def load_data(self):
        # 从数据库加载投资范围数据
        try:
            univ = fqdatac.get_universe(sd=self.start_date, ed=self.end_date, univ_name=self.name)
            self._data = self._partition_df(univ, "D")
        except Exception as e:
            raise FactorBackTestException('load universe data error, universe:{}, msg: {}'.format(self.name, str(e)))

    @property
    def data(self):
        if self._data is None:
            self.load_data()
        return self._data
