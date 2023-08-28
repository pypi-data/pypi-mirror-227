
import numpy as np
import pandas as pd

# df = pd.read_csv('./output/DTech_amt_merged.csv', sep=",", header='infer')

#
# coverage_max = len(df['K'].unique())
# total_days = len(df['D'].unique())
# df_days = df.groupby('K')['D'].count()
# coverage_min = len(df_days[df_days == total_days])
# df_coverage = pd.DataFrame({'coverage_max': [coverage_max], 'coverage_min': [coverage_min]})
# print(df_coverage)

#
# """基础部分之分10组"""
# grouped = df.groupby(by=['D', 'T'], as_index=False)
# df['q'] = df.groupby(by=['D', 'T'], as_index=False)[factor_name].transform(
#     lambda x: pd.qcut(x, 10, labels=["Q{}".format(i) for i in range(1, 11)]))
# df['q'] = df['q'].astype(str)
# df_q = df.query("q == 'Q1' or q == 'Q10'")
# # df_q = df[df.q.isin(['Q1', 'Q10'])]


"""计算SerialCorr"""

"""
@timer
def serial_corr():
    global df
    temp_df = df.sort_values(by='D', ascending=True)
    temp_df = df[['K', 'D', 'DTech_amt']]
    #获取前一天的因子序列
    prev_fac = pd.pivot_table(temp_df, columns='K', index="D", values='DTech_amt').shift(1)
    prev_fac = prev_fac.unstack().reset_index()
    prev_fac.columns = ['K', 'D', 'prev_fac']
    prev_fac = prev_fac.dropna(subset=['prev_fac'])
    #滚动计算相关性
    temp_df = pd.merge(temp_df, prev_fac, how='left', on=['K', 'D'])
    print(temp_df)
    serial_correlation = temp_df.groupby('D').apply(
        lambda x: x[['DTech_amt', 'prev_fac']].corr(method='spearman').iloc[0, 1])
    serial_correlation = serial_correlation.to_frame().reset_index().dropna()
    serial_correlation.columns = ['D', 'DTech_amt']
    return serial_correlation


s = time.time()
df_serial_corr = serial_corr()
print(np.mean(df_serial_corr['DTech_amt']))
e = time.time()
print(e - s)

# s = time.time()
# df['DT'] = df.apply(lambda row: "{} {}".format(row['D'], row['T']), axis=1)
# df_serial_klist = df[['K', 'DT', 'DTech_amt']].pivot(index=['K'], columns='DT', values='DTech_amt').reset_index()
# cols = df_serial_klist.columns.tolist()
# cols.remove('K')
# cols = list(zip(cols, cols[1:]))
# serial_corrs = []
# for col in cols:
#     corr = df_serial_klist[col[0]].corr(df_serial_klist[col[1]], method='pearson')
#     serial_corrs.append(corr)
# serial_corr = np.mean(serial_corrs)
# print(serial_corr)
# e = time.time()
# print(e - s)
"""

# df_serial_klist = grouped.agg(k_list=('K', list))
# df_serial_klist['k_list_prev_day'] = df_serial_klist['k_list'].shift(1)
# df_serial_klist['k_intersection'] = df_serial_klist.apply(lambda x: np.nan if x['k_list_prev_day'] is None else list(set(x['k_list']) & set(x['k_list_prev_day'])), axis=1)
# df_serial_klist = df_serial_klist.dropna(subset=['k_intersection'], axis=0)
# print(df_serial_klist[['D', 'T', 'k_intersection']])
# print(df_serial_klist.to_csv('./output/x.csv'))

#
# """4.1 计算IC相关性"""
# df_ic = grouped.apply(lambda x: x['DTech_high'].corr(x[fwtret], 'spearman'))
# df_ic.columns = ['D', 'T', col_name]
# # df_ic.to_csv("ic.csv")
# # print(df_ic)
#
# """4.2 LongShort部分之计算Coverage"""
# df_coverage = grouped.agg({'K': 'count'})
# df_coverage = df_coverage.rename(columns={"K": col_name})
# df_coverage = df_coverage[['D', 'T', col_name]]
# # df_coverage.to_csv("coverage.csv")
# # print(df_coverage)
#
# """4.3 LongShort部分之计算turnover"""
# df_turnover = df_q.groupby(['D', 'T'], as_index=False).agg({"K": list})
# df_turnover.columns = ['D', 'T', 'K_list']
# df_turnover['K_list_prev'] = df_turnover.sort_values(by=['D', 'T'], ascending=True)['K_list'].shift(1)
# df_turnover[col_name] = df_turnover.apply(lambda x: calc_turnover(x['K_list'], x['K_list_prev']), axis=1)
# df_turnover = df_turnover[['D', 'T', col_name]]
# # df_turnover.to_csv("turnover.csv")
# # print(df_turnover)
#
# """4.4 LongShort部分之计算LSreturn"""
# df_lsreturn = df_q.groupby(by=['D', 'T', 'q'], as_index=False)[fwtret].mean()
# df_lsreturn = df_lsreturn.pivot(index=['D', 'T'], columns='q', values=fwtret).reset_index()
# df_lsreturn['LSreturn'] = df_lsreturn.apply(lambda row: row['Q10'] - row['Q1'], axis=1)
# df_lsreturn = df_lsreturn[['D', 'T', 'LSreturn']]
# # print(df_lsreturn)
#
# """4.5 LongShort部分之计算HitRate"""
# df_hitrate = df_q.groupby(by=['D', 'T'], as_index=False).apply(calc_hitrate)
# df_hitrate.columns = ['D', 'T', col_name]
# # df_hitrate.to_csv("hitrate.csv")
# # print(df_hitrate)
#
# """4.6 Longshort部分之Wealth模块"""
# df_lsreturn['wealth'] = df_lsreturn['LSreturn'].apply(lambda x: x+1).cumprod()
# # print(df_lsreturn)
#
# df_wealth = df_lsreturn[['D', 'T', 'wealth']]
# df_wealth.columns = ['D', 'T', col_name]
#
# df_lsreturn = df_lsreturn[['D', 'T', 'LSreturn']]
# df_lsreturn.columns = ['D', 'T', col_name]
#
#
# # df_lsreturn.to_csv("lsreturn.csv")
# """4.7 Longshort部分之Summary模块"""
#
# with pd.ExcelWriter('output.xlsx') as writer:
#     df_ic.to_excel(writer, sheet_name='ICs')
#     df_coverage.to_excel(writer, sheet_name='coverage')
#     df_turnover.to_excel(writer, sheet_name='turnover')
#     df_lsreturn.to_excel(writer, sheet_name='LSreturns')
#     df_hitrate.to_excel(writer, sheet_name='HitRate')
#     df_wealth.to_excel(writer, sheet_name='wealth')
#

##############################
# 计算summary部分
##############################

"""
def max_drawdown(xs: list) -> float:
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


df = pd.read_csv("./output/DTech_amt_single.csv")
df = df.sort_values(by=['D', 'T'], axis=0, ascending=True)

N = df.shape[0]

FIRST_DAY = 0
LAST_ONE_DAY = -1
LAST_ONE_MONTH = -22
LAST_THREE_MONTH = -64
LAST_ONE_YEAR = -245
LAST_THREE_YEAR = -490
LAST_FIVE_YEAR = -1225
DAYS_PER_YEAR = 244

summary = {}
"""

"""
低于一年是的
1~3年的话  cagr=cagr3 = cagr5
3~5年的话 cagr=cagr5
"""

"""
btm_w = df.iloc[0, df.columns.get_loc('wealth')]
btm_d1 = df.iloc[LAST_ONE_DAY, df.columns.get_loc('wealth')]
btm_m1 = df.iloc[LAST_ONE_MONTH, df.columns.get_loc('wealth')]
btm_m3 = df.iloc[LAST_THREE_MONTH, df.columns.get_loc('wealth')]
btm_y1 = df.iloc[LAST_ONE_YEAR, df.columns.get_loc('wealth')]
btm_y3 = df.iloc[LAST_THREE_YEAR, df.columns.get_loc('wealth')]
btm_y5 = df.iloc[LAST_FIVE_YEAR, df.columns.get_loc('wealth')]

return_Z = btm_d1/btm_w - 1
summary['return_1m'] = (btm_d1 - 1) if N < abs(LAST_ONE_MONTH) else (btm_d1/btm_m1 - 1)
summary['return_3m'] = (btm_d1 - 1) if N < abs(LAST_THREE_MONTH) else (btm_d1/btm_m3 - 1)
return_Z1y = (btm_d1 - 1) if N < abs(LAST_ONE_YEAR) else (btm_d1/btm_y1 - 1)
return_Z3y = (btm_d1 - 1) if N < abs(LAST_THREE_YEAR) else (btm_d1/btm_y3 - 1)
return_Z5y = (btm_d1 - 1) if N < abs(LAST_FIVE_YEAR) else (btm_d1/btm_y5 - 1)

summary['cagr'] = (return_Z + 1) ** (DAYS_PER_YEAR / N) - 1
summary['cagr_1y'] = summary['cagr'] if N < abs(LAST_ONE_YEAR) else return_Z1y
summary['cagr_3y'] = summary['cagr'] if N < abs(LAST_THREE_YEAR) else ((return_Z3y + 1) ** (DAYS_PER_YEAR / abs(LAST_THREE_YEAR)) - 1.0)
summary['cagr_5y'] = summary['cagr'] if N < abs(LAST_FIVE_YEAR) else ((return_Z5y + 1) ** (DAYS_PER_YEAR / abs(LAST_FIVE_YEAR)) - 1.0)
summary['volatility'] = df['LSreturn'].std(ddof=1) * np.sqrt(DAYS_PER_YEAR)
summary['sharpe_ratio'] = summary['cagr'] / summary['volatility']
summary['rank_ic_mean'] = df['ic'].mean()
summary['rank_ic_std'] = df['ic'].std(ddof=1)
summary['rank_ic_std'] = summary['rank_ic_mean'] / summary['rank_ic_std']
summary['hit_rate'] = df['hitrate'].mean() * 100.0
summary['max_drawdown'] = max_drawdown(df['wealth'].tolist())

summary['turnover'] = df['turnover'].mean() * 100
"""



"""
CAGR算法

对于X1年：获取X1年 最后一个交易日 4.6中计算得到的Wealth值W 返回W ** （M/252）- 1, M为当年加入计算的交易日天数

对于XN年，分别获取回测期内 XN-1年 最后一个交易日和XN年最后一个交易日（XN年最后一个交易日不一定是当年真正的最后一个交易日，因为回测期没有到XN年的末尾） 4.6中计算得到的Wealth值W1，W2，返回（W2/W1） ** （M/252）- 1, M为当年加入计算的交易日天数

对于其他年份y，分别获取 y-1年 最后一个交易日和y年最后一个交易日4.6中计算得到的Wealth值W1，W2，返回（W2/W1）- 1
"""

"""
df['Y'] = df['D'].apply(lambda day: str(day)[0:4])
df_cagr_agg = df.groupby(by=['Y'], as_index=False).agg(M=('D', 'count'), D_min=('D', 'min'), D_max=('D', 'max'))
df_cagr_agg = pd.merge(df_cagr_agg, df[['D', 'wealth']], left_on='D_min', right_on='D')
df_cagr_agg = df_cagr_agg.rename(columns={"wealth": "D_min_wealth"})
df_cagr_agg.drop('D', axis=1, inplace=True)
df_cagr_agg = pd.merge(df_cagr_agg, df[['D', 'wealth']], left_on='D_max', right_on='D')
df_cagr_agg = df_cagr_agg.rename(columns={"wealth": "D_max_wealth"})
df_cagr_agg.drop('D', axis=1, inplace=True)
df_cagr_agg['D_max_wealth_1'] = df_cagr_agg['D_max_wealth'].shift(1)



df['Y'] = df['D'].apply(lambda day: str(day)[0:4])
df_cagr_agg = df.groupby(by=['Y'], as_index=False).agg(M=('D', 'count'), D_max=('D', 'max'))
df_cagr_agg = pd.merge(df_cagr_agg, df[['D', 'wealth']], left_on='D_max', right_on='D')
df_cagr_agg = df_cagr_agg.rename(columns={"wealth": "D_max_wealth"})
df_cagr_agg.drop('D', axis=1, inplace=True)
df_cagr_agg['D_max_wealth_1'] = df_cagr_agg['D_max_wealth'].shift(1)
for _, row in df_cagr_agg.iterrows():
    cagr_year_key = "cagr_year_{}".format(row['Y'])
    if str(row['D_max_wealth_1']) == 'nan':
        summary[cagr_year_key] = row['D_max_wealth'] ** (row['M']/float(DAYS_PER_YEAR)) - 1.0
    else:
        summary[cagr_year_key] = (row['D_max_wealth']/row['D_max_wealth_1']) ** (row['M']/float(DAYS_PER_YEAR)) - 1.0

df_ic_agg = df.groupby(by=['Y'], as_index=False).agg(rank_ic_mean_year=('ic', 'mean'))
for _, row in df_ic_agg.iterrows():
    summary["rank_ic_mean_year_{}".format(row['Y'])] = row['rank_ic_mean_year']

"""
from fatbulls.context import FatbullsFactorContext

class FactorCalculateTask(object):
    """多线程执行引擎"""

    def __init__(self, factor_name: str, factor_data: dict, forward_return: pd.DataFrame):
        self.factor_name = factor_name
        self.factor_data = factor_data
        self.forward_return = forward_return
        self._factor_config = FatbullsFactorContext.get_instance().get_factor_config()
        self.forward_return_name = list(forward_return.columns)[-1]
        self.factor_forward = self.factor_name + '_' + self.forward_return_name
        self.grouped = None
        self.df_q = None
        self.df_backtest_res = None
        self.backtest_result = dict()

    def __call__(self, **kwargs):
        self._middle_calculate()
        self._calculate_ic()
        self._calculate_coverage()
        self._calculate_turnover()
        self._calculate_lsreturn_and_wealth()
        self._calculate_hitrate()
        self.df_backtest_res.to_csv("./output/{}_single.csv".format(self.factor_name))
        self._clean()
        return self.df_backtest_res

    def _calc_turnover(self, x, y):
        """计算交集"""
        if x is None or y is None:
            return 1.0
        return 1.0 - len(set(x).intersection(set(y))) / (len(x) + len(y))

    def _calc_hitrate(self, group_df):
        """计算HitRate"""
        row_size = group_df.shape[0]
        if row_size <= 0:
            return 0.0
        group_df_q1 = group_df[group_df.q == 'Q1']
        group_df_q10 = group_df[group_df.q == 'Q10']
        arr_pos = np.array(group_df_q1[self.forward_return_name])
        arr_neg = np.array(group_df_q10[self.forward_return_name])
        pos_count = np.sum(arr_pos > 0)
        neg_count = np.sum(arr_neg < 0)
        return float(pos_count + neg_count) / row_size

    def _middle_calculate(self):
        """中间计算：单因子加载所有csv文件"""
        df_factor_data = pd.concat(self.factor_data.values(), axis=0, ignore_index=True)
        df_all = pd.merge(df_factor_data, self.forward_return, on=['K', 'D', 'T'], how='left')
        df_all = df_all.dropna(subset=[self.factor_name])
        df_all = df_all.dropna(subset=[self.forward_return_name])
        self.grouped = df_all.groupby(by=['D', 'T'], as_index=False)
        df_all['q'] = df_all.groupby(by=['D', 'T'], as_index=False)[self.factor_name].transform(
            lambda x: pd.qcut(x, 10, labels=["Q{}".format(i) for i in range(1, 11)]))
        df_all['q'] = df_all['q'].astype(str)
        self.df_coverage_summary = df_all.groupby(by=['D', 'T'], as_index=False)
        self.df_q = df_all.query("q == 'Q1' or q == 'Q10'")

    def _clean(self):
        del self.df_q
        del self.grouped

    def _calculate_ic(self):
        """4.1 计算IC"""
        df_ic = self.grouped.apply(lambda x: x[self.factor_name].corr(x[self.forward_return_name], 'spearman'))
        df_ic.columns = ['D', 'T', 'ic']
        self.backtest_result['ic'] = df_ic
        self.df_backtest_res = df_ic

    def _calculate_coverage(self):
        """4.2 LongShort部分之计算覆盖率"""
        df_coverage = self.grouped.agg({'K': 'count'})
        df_coverage = df_coverage.rename(columns={"K": 'coverage'})
        df_coverage = df_coverage[['D', 'T', 'coverage']]
        self.backtest_result['coverage'] = df_coverage
        # self.df_backtest_res = pd.merge(self.df_backtest_res, df_coverage, on=['D', 'T'], how='left')

    def _calculate_turnover(self):
        """4.3 LongShort部分之计算换手率"""
        df_turnover = self.df_q.groupby(['D', 'T'], as_index=False).agg({"K": list})
        df_turnover.columns = ['D', 'T', 'K_list']
        df_turnover['K_list_prev'] = df_turnover.sort_values(by=['D', 'T'], ascending=True)['K_list'].shift(1)
        df_turnover['turnover'] = df_turnover.apply(lambda x: self._calc_turnover(x['K_list'], x['K_list_prev']),
                                                    axis=1)
        df_turnover = df_turnover[['D', 'T', 'turnover']]
        self.backtest_result['turnover'] = df_turnover
        # self.df_backtest_res = pd.merge(self.df_backtest_res, df_turnover, on=['D', 'T'], how='left')

    def _calculate_lsreturn_and_wealth(self):
        """4.4 LongShort部分之计算LSreturn And Wealth"""
        df_lsreturn = self.df_q.groupby(by=['D', 'T', 'q'], as_index=False)[self.forward_return_name].mean()
        df_lsreturn = df_lsreturn.pivot(index=['D', 'T'], columns='q', values=self.forward_return_name).reset_index()
        df_lsreturn['LSreturn'] = df_lsreturn.apply(lambda row: row['Q1'] - row['Q10'], axis=1)
        df_lsreturn['wealth'] = df_lsreturn['LSreturn'].apply(lambda x: x + 1).cumprod()
        df_lsreturn = df_lsreturn[['D', 'T', 'LSreturn', 'wealth']]
        self.backtest_result['lsreturn'] = df_lsreturn
        # self.df_backtest_res = pd.merge(self.df_backtest_res, df_lsreturn, on=['D', 'T'], how='left')

    def _calculate_hitrate(self):
        """4.5 LongShort部分之计算HitRate"""
        df_hitrate = self.df_q.groupby(by=['D', 'T'], as_index=False).apply(self._calc_hitrate)
        df_hitrate.columns = ['D', 'T', 'hitrate']
        self.backtest_result['hitrate'] = df_hitrate
        # self.df_backtest_res = pd.merge(self.df_backtest_res, df_hitrate, on=['D', 'T'], how='left')

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