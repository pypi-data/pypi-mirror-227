#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2023 datavita.com.cn, Inc. All Rights Reserved
#
########################################################################


"""
File: run_single_calculate.py
Author: wangjiangfeng(wangjiangfeng@hcyjs.com)
Date: 2023/8/21 18:50:29
"""


import pandas as pd
import numpy as np
from fatbulls import time_cost

"""基础函数区域"""

FIRST_DAY = 0
LAST_ONE_DAY = -1
LAST_ONE_MONTH = -22
LAST_THREE_MONTH = -64
LAST_ONE_YEAR = -245
LAST_THREE_YEAR = -490
LAST_FIVE_YEAR = -1225
DAYS_PER_YEAR = 244


class FactorCalculateTask(object):

    def __init__(self, factor_name, forward_return_name, forward_days, return_type):
        self.factor_name = factor_name
        self.forward_return_name = forward_return_name
        self.factor_data = pd.read_csv('./output/{}_merged.csv'.format(factor_name), sep=",", header='infer')
        self.backtest_result = dict()
        self.output_colname = "{}_{}".format(factor_name, forward_return_name)
        self.coverage = {}

    def _middle_calculate(self):
        self.factor_data = self.factor_data.sort_values(by=['D', 'T', 'K'], axis=0, ascending=True)
        self.grouped = self.factor_data.groupby(by=['D', 'T'], as_index=False)
        self.factor_data['q'] = self.factor_data.groupby(by=['D', 'T'], as_index=False)[self.factor_name].transform(
            lambda x: pd.qcut(x, 10, labels=["Q{}".format(i) for i in range(1, 11)]))
        self.factor_data['q'] = self.factor_data['q'].astype(str)
        self.df_longshort = self.factor_data.query("q == 'Q1' or q == 'Q10'")

    @time_cost
    def run(self, *args, **kwargs):
        self._middle_calculate()
        self._coverage_summary()
        self.calculate_ic()
        self.calculate_coverage()
        self.calculate_turnover()
        self.calculate_lsreturn()
        self.calculate_hitrate()
        self.calculate_wealth()
        self.summary()
        self.summary(summary_type="top")
        self.summary(summary_type="bottom")
        return self.backtest_result

    def calculate_ic(self):
        """4.1 计算IC相关性, 不区分LongShort"""
        df_ic = self.grouped.apply(lambda x: x[self.factor_name].corr(x[self.forward_return_name], 'spearman'))
        df_ic.columns = ['D', 'T', self.output_colname]
        self.backtest_result['ICs'] = df_ic
        del df_ic

    def calculate_coverage(self):
        """4.1 计算coverage, 不区分LongShort"""
        df_coverage = self.grouped.agg({'K': 'count'})
        df_coverage = df_coverage.rename(columns={"K": self.factor_name})
        df_coverage = df_coverage[['D', 'T', self.factor_name]].rename(columns={self.factor_name: self.output_colname})
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
        df_q = df_q[['D', 'T', self.factor_name]].rename(columns={self.factor_name: self.output_colname})
        return df_q

    def calculate_lsreturn(self):
        """4.4 LongShort部分之计算LSreturn"""
        df_lsreturn = self.df_longshort.groupby(by=['D', 'T', 'q'], as_index=False)[self.forward_return_name].mean()
        df_lsreturn = df_lsreturn.pivot(index=['D', 'T'], columns='q', values=self.forward_return_name).reset_index()
        df_lsreturn['LSreturns'] = df_lsreturn.apply(lambda row: row['Q10'] - row['Q1'], axis=1)
        self.backtest_result['LSreturns'] = df_lsreturn[['D', 'T', 'LSreturns']].rename(columns={"LSreturns": self.output_colname})
        self.backtest_result['top_Returns'] = df_lsreturn[['D', 'T', 'Q10']].rename(columns={"Q10": self.output_colname})
        self.backtest_result['bottom_Returns'] = df_lsreturn[['D', 'T', 'Q1']].rename(columns={"Q1": self.output_colname})
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
            columns={"HitRate": self.output_colname})
        self.backtest_result['top_HitRate'] = df_hitrate[['D', 'T', 'top_HitRate']].rename(
            columns={"top_HitRate": self.output_colname})
        self.backtest_result['bottom_HitRate'] = df_hitrate[['D', 'T', 'bottom_HitRate']].rename(
            columns={"bottom_HitRate": self.output_colname})
        del df_hitrate

    def calculate_wealth(self):
        """4.6 Longshort部分之Wealth模块"""
        df_lsreturn = self.backtest_result['LSreturns'].copy()
        df_lsreturn[self.output_colname] = df_lsreturn[self.output_colname].apply(lambda x: x+1).cumprod()
        df_lsreturn_top = self.backtest_result['top_Returns'].copy()
        df_lsreturn_top[self.output_colname] = df_lsreturn_top[self.output_colname].apply(lambda x: x+1).cumprod()
        df_lsreturn_bottom = self.backtest_result['bottom_Returns'].copy()
        df_lsreturn_bottom[self.output_colname] = df_lsreturn_bottom[self.output_colname].apply(lambda x: x+1).cumprod()
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

    def _calculate_serial_corr(self):
        temp_df = self.factor_data.sort_values(by='D', ascending=True)
        temp_df = temp_df[['K', 'D', self.factor_name]]
        """获取前一天的因子序列"""
        prev_fac = pd.pivot_table(temp_df, columns='K', index="D", values='DTech_amt').shift(1)
        prev_fac = prev_fac.unstack().reset_index()
        prev_fac.columns = ['K', 'D', 'prev_fac']
        prev_fac = prev_fac.dropna(subset=['prev_fac'])
        """滚动计算相关性"""
        temp_df = pd.merge(temp_df, prev_fac, how='left', on=['K', 'D'])
        serial_correlation = temp_df.groupby('D').apply(
            lambda x: x[['DTech_amt', 'prev_fac']].corr(method='spearman').iloc[0, 1])
        serial_correlation = serial_correlation.to_frame().reset_index().dropna()
        serial_correlation.columns = ['D', 'DTech_amt']
        del temp_df
        return serial_correlation

    def summary(self, summary_type="top"):
        summary = dict()
        summary['coverage_max'] = self.coverage['coverage_max']
        summary['coverage_min'] = self.coverage['coverage_min']
        df_ic = self.backtest_result['ICs'].copy()
        if summary_type.lower() == 'top':
            df_wealth = self.backtest_result['top_Wealth'].copy()
            df_lsreturn = self.backtest_result['top_Returns'].copy()
            df_hitrate = self.backtest_result['top_HitRate'].copy()
            df_turnover = self.backtest_result['top_HitRate'].copy()
            summary_key = 'top_Summary'
        elif summary_type.lower() == 'bottom':
            df_wealth = self.backtest_result['bottom_Wealth'].copy()
            df_lsreturn = self.backtest_result['bottom_Returns'].copy()
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
        btm_w = df_wealth.iloc[0, df_wealth.columns.get_loc(self.output_colname)]
        btm_d1 = 1.0 if n_days < abs(LAST_ONE_DAY) else df_wealth.iloc[LAST_ONE_DAY, df_wealth.columns.get_loc(self.output_colname)]
        btm_m1 = 1.0 if n_days < abs(LAST_ONE_MONTH) else df_wealth.iloc[LAST_ONE_MONTH, df_wealth.columns.get_loc(self.output_colname)]
        btm_m3 = 1.0 if n_days < abs(LAST_THREE_MONTH) else df_wealth.iloc[LAST_THREE_MONTH, df_wealth.columns.get_loc(self.output_colname)]
        btm_y1 = 1.0 if n_days < abs(LAST_ONE_YEAR) else df_wealth.iloc[LAST_ONE_YEAR, df_wealth.columns.get_loc(self.output_colname)]
        btm_y3 = 1.0 if n_days < abs(LAST_THREE_YEAR) else df_wealth.iloc[LAST_THREE_YEAR, df_wealth.columns.get_loc(self.output_colname)]
        btm_y5 = 1.0 if n_days < abs(LAST_FIVE_YEAR) else df_wealth.iloc[LAST_FIVE_YEAR, df_wealth.columns.get_loc(self.output_colname)]
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
        summary['volatility'] = df_lsreturn[self.output_colname].std(ddof=1) * np.sqrt(DAYS_PER_YEAR)
        summary['sharpe_ratio'] = summary['cagr'] / summary['volatility']
        summary['rank_ic_mean'] = df_ic[self.output_colname].mean()
        summary['rank_ic_std'] = df_ic[self.output_colname].std(ddof=1)
        summary['ic_ir'] = summary['rank_ic_mean'] / summary['rank_ic_std']
        summary['hit_rate'] = df_hitrate[self.output_colname].mean() * 100.0
        summary['max_drawdown'] = self._max_drawdown(df_wealth[self.output_colname].tolist())
        summary['serial_corr'] = self._calculate_serial_corr()
        summary['turnover'] = df_turnover[self.output_colname].mean() * 100
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
        df_cagr_agg = pd.merge(df_cagr_agg, df_wealth[['D', self.output_colname]], left_on='D_max', right_on='D')
        df_cagr_agg = df_cagr_agg.rename(columns={self.output_colname: "D_max_wealth"})
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
        df_ic_agg = df_ic.groupby(by=['Y'], as_index=False).agg(rank_ic_mean_year=(self.output_colname, 'mean'))
        for _, row in df_ic_agg.iterrows():
            rank_ic_mean_res["rank_ic_mean_year_{}".format(row['Y'])] = row['rank_ic_mean_year']
        return rank_ic_mean_res


a = FactorCalculateTask('DTech_amt', 'fwd1_vwap30', 1, 'vwap30')
print(a.run())
