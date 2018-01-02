#!/usr/bin/python
# -*- coding:utf-8 -*-
"""停牌股票peg、ps、一周涨跌幅、相对最高最低计算"""


from initialize import Mongo
from pymongo import UpdateOne
import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# 加载日行情数据
def __get_mktdata_list(mongo, equity_list):
    mkt_data_map = dict()
    ma_data_map = dict()
    mkt_data_collection = mongo.gettable('z3_stk_mkt_day_inter_new')
    today = datetime.datetime.now()
    yesterday = int((today + datetime.timedelta(days=-7)).strftime('%Y%m%d'))
    mkt_data_list = []
    ma_data_list = []
    for equity in equity_list:
        innercode = equity.get('_id')
        mkt_idx = equity.get('mkt_idx')
        if not mkt_idx:
            continue
        tmp_data = mkt_data_collection.find({'ex_status': 1, 'innerCode': innercode}).sort([('end_date', -1)]).limit(7)
        if tmp_data.count() > 0:
            ma_data_list.append(tmp_data[0])
        if tmp_data.count() == 7:
            first_date = tmp_data[0].get('end_date')
            date_minus = int(today.strftime('%Y%m%d')) - int(first_date)

            if date_minus > 7:
                continue
            mkt_data_list.append(tmp_data[-1])
    for mkt_data in mkt_data_list:
        innercode = mkt_data.get('innerCode')
        close_px = mkt_data.get('close_px')
        if not close_px:
            continue
        if not mkt_data_map.get(innercode):
            mkt_data_map[innercode] = close_px

    for ma_data in ma_data_list:
        innercode = ma_data.get('innerCode')
        ma_data_map[innercode] = ma_data
    return mkt_data_map, ma_data_map


def run():
    mongo = Mongo()
    collection = mongo.gettable('z3_equity')
    equity_list = collection.find({'mkt_idx.is_stop': True}, {'mkt_idx': 1, 'fin_idx': 1, 'mkt2_idx': 1})
    mkt_data_map, ma_data_map = __get_mktdata_list(mongo, equity_list)
    print len(mkt_data_map)
    requests = []
    equity_list.rewind()
    columns = ['low_10day', 'high_10day', 'low_20day', 'high_20day', 'low_30day', 'high_30day',
               'low_60day', 'high_60day', 'low_120day', 'high_120day', 'low_52week', 'high_52week']
    ma_columns = ['ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma120', 'ma250']
    for equity in equity_list:
        innercode = equity.get('_id')
        mkt_idx = equity.get('mkt_idx')
        if not mkt_idx:
            continue
        tcap = mkt_idx.get('tcap')
        value = {}
        mkt2_idx = equity.get('mkt2_idx')

        # pe_ttm
        if mkt_idx.get('pe_ttm'):
            value['mkt_idx.pe_ttm'] = round(mkt_idx.get('pe_ttm'), 4)

        # expect_price_chng_pct
        if mkt_idx.get('expect_price_chng_pct'):
            value['mkt_idx.expect_price_chng_pct'] = round(mkt_idx.get('expect_price_chng_pct'), 2)

        # pb
        pb = mkt_idx.get('pb')
        if pb:
            pb = round(pb, 4)
        elif mkt2_idx:
            net_asset = mkt2_idx.get('net_asset')
            if net_asset and net_asset != 0:
                pb = round(tcap / net_asset, 4)
        value['mkt_idx.pb'] = pb

        # pc
        pc = mkt_idx.get('pc')
        if pc:
            pc = round(pc, 4)
        elif mkt2_idx:
            cash_ttm = mkt2_idx.get('cash_ttm')
            if cash_ttm and cash_ttm != 0:
                pc = round(tcap / cash_ttm, 4)
        value['mkt_idx.pc'] = pc

        # peg
        peg = None
        pettm = None
        if mkt2_idx:
            mic_ttm = mkt2_idx.get('mic_ttm')
            if mic_ttm and mic_ttm != 0:
                pettm = tcap / mic_ttm
                if pettm < 0:
                    pettm = None
            es_3year = mkt2_idx.get('es_3year')
            if es_3year and es_3year != 0:
                if pettm:
                    peg = round(pettm / es_3year, 4)
                else:
                    peg = None
        if pettm:
            value['mkt_idx.pe_ttm'] = round(pettm, 4)
        else:
            value['mkt_idx.pe_ttm'] = None
        value['mkt_idx.peg'] = peg

        # ps
        fin_idx = equity.get('fin_idx')
        ps = None
        if fin_idx:
            sale = fin_idx.get('sale')
            if sale and sale != 0:
                ps = round(tcap / sale, 2)
        value['mkt_idx.ps'] = ps

        # chng_pct_week
        close_px = mkt_data_map.get(innercode)
        prev_close_px = mkt_idx.get('prev_close_px')
        chng_pct_week = None
        if prev_close_px and prev_close_px != 0:
            if close_px and close_px != 0:
                chng_pct_week = round((prev_close_px - close_px) / close_px, 2)
            for column in columns:
                val = mkt2_idx.get(column)
                prefix = 'mkt_idx.rela_' + column
                if val and val != 0:
                    value[prefix] = round((prev_close_px - val) / val, 4)
                else:
                    value[prefix] = None
        value['mkt_idx.chng_pct_week'] = chng_pct_week
        value['mkt_idx.rela_volume'] = None

        # rela_ma
        ma_data = ma_data_map.get(innercode)
        if ma_data:
            close_px = ma_data.get('close_px')
            if close_px:
                for column in ma_columns:
                    prefix = 'mkt_idx.rela_' + column
                    ma_val = ma_data.get(column)
                    if ma_val and ma_val != 0:
                        value[prefix] = round((close_px - ma_val) / ma_val, 2)
        if value:
            requests.append(UpdateOne({'_id': innercode}, {'$set': value}))
    if requests:
        collection.bulk_write(requests, ordered=False)


def main():
    run()


if __name__ == '__main__':
    main()

