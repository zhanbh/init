#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
from initialize import Mongo

reload(sys)
sys.setdefaultencoding('utf-8')


# 计算历史连涨连跌，用于初始化数据
def count_series(date):
    mongo = Mongo()
    capinfo_collection = mongo.gettable('z3_cap_info_subs')
    capinfo_results = capinfo_collection.find({'type': 3, 'trade_date': {'$lte': date}}).sort('trade_date', 1)
    capinfo_dict = {}
    for capinfo in capinfo_results:
        day_array = capinfo.get('day_array')
        if not day_array:
            continue
        for day in day_array:
            if day.get('period') == 1:
                chgpct = day.get('chg_pct')
                break
        if not chgpct:
            continue

        innercode = capinfo.get('innerCode')
        # if innercode != 270500:
        #     continue
        trade_date = capinfo.get('trade_date')
        if innercode not in capinfo_dict:
            capinfo_dict[innercode] = {}
        child_dict = capinfo_dict.get(innercode)
        if not child_dict.get(trade_date):
            child_dict[trade_date] = chgpct

    for key, val in capinfo_dict.items():
        capinfo_dict[key] = sorted(val.items(), key=lambda d: d[0], reverse=True)

    for key, val in capinfo_dict.items():
        keep_days = 0
        first_info = val[0]
        up = first_info[1]
        if up > 0:
            keep_days = 1
        elif up < 0:
            keep_days = -1

        for day_info in val[1:]:
            chg_pct = day_info[1]
            if chg_pct > 0 and up > 0:
                keep_days += 1
                up = chg_pct
            elif chg_pct < 0 and up < 0:
                keep_days -= 1
                up = chg_pct
            else:
                break
        capinfo_collection.update({'_id': key + '-3-' + str(date)}, {'$set': {'keep_days': keep_days}}, upsert=False)


# 测试某个行业连涨跌天数是否准确
def test_series(innercode):
    mongo = Mongo()
    collection = mongo.gettable('z3_cap_info_subs')
    results = collection.find({'innerCode': innercode, 'type': 3}).sort('trade_date', -1)
    for result in results:
        day_array = result.get('day_array')
        chgpct = 0
        for day in day_array:
            if day.get('period') == 1:
                chgpct = day.get('chg_pct')
                break
        print str(result.get('trade_date')) + '===' + str(chgpct)


def main():
    count_series(20180112)
    # test_series('110100')

if __name__ == '__main__':
    main()

