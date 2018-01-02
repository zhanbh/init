# -*- coding:utf-8 -*-
"""初始化数据"""


import sys
import os
from pymongo.errors import ServerSelectionTimeoutError
from pymongo import MongoClient, UpdateOne
from settings import DB_INFO, USER_INFO, TABLES, LOG_PATH
import datetime
import time
import logging as logger
reload(sys)
sys.setdefaultencoding('utf-8')


logger.basicConfig(level=logger.DEBUG,
                   format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                   datefmt='%a, %d %b %Y %H:%M:%S',
                   filename=LOG_PATH,
                   filemode='a')


class Mongo():
    def __init__(self):
        self.client = MongoClient(DB_INFO.get('IP'), DB_INFO.get('PORT'))
        self.db = self.client.get_database(DB_INFO.get('DBNAME'))
        self.db.authenticate(name=USER_INFO.get('username'), password=USER_INFO.get('password'))

    def __del__(self):
        pass

    def gettable(self, tablename):
        return self.db.get_collection(tablename.upper())

    @staticmethod
    def insert(collection, value):
        collection.insert_one(value)

    @staticmethod
    def update(collection, value):
        collection.update_many({}, {'$set': value}, upsert=False)

    @staticmethod
    def remove(collection):
        collection.remove({})

    @staticmethod
    def removecolumn(collection, column):
        collection.update_many({}, {'$unset': {column: ''}}, upsert=False)


def run():
    calendar_list = []
    calendar_file_path = os.path.join(sys.path[0], 'calendar.dat')
    try:
        mongo = Mongo()
        # 交易日历
        exchange_calendar = mongo.gettable('z3_exchange_calendar')
        tmp_calendar_list = exchange_calendar.find({'open_close': 2})
        for calendar in tmp_calendar_list:
            calendar_list.append(calendar['trade_date'])
    except ServerSelectionTimeoutError:
        if not os.path.exists(calendar_file_path):
            return
        with open(calendar_file_path) as rfile:
            for calendar in rfile.readlines():
                calendar_list.append(calendar)


    calendar_dict = {}
    with open(calendar_file_path, 'w') as wfile:
        for calendar in calendar_list:
            wfile.write(str(calendar) + '\n')
            calendar_dict[int(calendar)] = 1
    calendar_date = int(time.strftime('%Y%m%d', time.localtime(time.time())))
    if calendar_date in calendar_dict:
        return

    for key, value in TABLES.items():
        if not value:
            continue
        logger.info('===init init===table = %s', key)
        collection = mongo.gettable(key)
        if collection.name == 'Z3_TOPIC_CHANGE':
            result = collection.find_one()
            value['_id'] = int(datetime.datetime.now().strftime("%Y%m%d"))
            value['topic_num'] = result.get('topic_num')
            Mongo.remove(collection)
            Mongo.insert(collection, value)
            logger.info('===update update===table = %s', key)
        elif collection.name == 'Z3_INDU_CHANGE':
            result = collection.find_one()
            value['_id'] = int(datetime.datetime.now().strftime("%Y%m%d"))
            value['indu_num'] = result.get('indu_num')
            Mongo.remove(collection)
            Mongo.insert(collection, value)
        else:
            if value.get('operator'):
                Mongo.remove(collection)
                logger.info('===remove remove===table = %s', key)
            else:
                Mongo.update(collection, value)
                logger.info('===update update===table = %s', key)
    # add by 20170731
    equity_profile_collection = mongo.gettable('z3_equity_profile')
    equity_profile_list = equity_profile_collection.find({'sec_type': 1, 'chi_spel': {'$ne': None}}, {'_id': 1, 'chi_spel': 1})
    requests = []
    for equity_profile in equity_profile_list:
        innercode = equity_profile.get('_id')
        chi_spel = equity_profile.get('chi_spel')
        requests.append(UpdateOne({'_id': innercode, 'type': 1}, {'$set': {'chi_spel': chi_spel}}))
    cap_info_subs_collection = mongo.gettable('z3_cap_info_subs')
    cap_info_subs_collection.bulk_write(requests, ordered=False)


def main():
    run()


if __name__ == '__main__':
    main()

