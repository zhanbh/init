# -*- coding:utf-8 -*-
DEBUG = True

# LOG_PATH = '/data/Shell/z3schedule.jrj.local/Py/initialize.log'
LOG_PATH = 'initialize.log'

FILEPATH = '/data/History/'

MIN5STEP = 5

MIN15STEP = 15

MIN30STEP = 30

MIN60STEP = 60

TABLENAME = 'z3_min_data'

# DB_INFO = {'IP': '10.88.4.24', 'PORT': 27017, 'DBNAME': 'z3dbus'}
DB_INFO = {'IP': '10.77.4.37', 'PORT': 27017, 'DBNAME': 'z3dbus'}
# DB_INFO = {'IP': '192.168.232.131', 'PORT': 27017, 'DBNAME': 'z3dbus_test'}

USER_INFO = {'username': 'z3dbusadmin', 'password': 'z3dbusadmin'}

Z3_TOPIC_INFO = {'topic_market.chng_pct': None, 'topic_market.stk_up_num': None, 'topic_market.stk_down_num': None}

Z3_TOPIC_CHANGE = {'topic_up_num': None, 'topic_down_num': None}

Z3_TOPIC_QUOTE = {'operator': 'REMOVE'}

Z3_EQUITY = {'mkt_idx.rela_volume': None, 'signal_normal.signal_normal_6': False,
             'signal_normal.signal_normal_7': False, 'signal_normal.signal_normal_22': False,
             'signal_normal.signal_normal_23': False, 'mkt_idx.chg': None,
             'mkt_idx.open_px': None, 'mkt_idx.high_px': None,
             'mkt_idx.low_px': None, 'mkt_idx.amount': None,
             'mkt_idx.prange': None, 'mkt_idx.exchr': None,
             'mkt_idx.tvol_lot': None, 'mkt_idx.new_vol_lot': None,
             'mkt_idx.sell': None, 'mkt_idx.buy': None,
             'mkt_idx.committee': None, 'mkt_idx.volume_ratio': None,
             'mkt_idx.volume': None, 'mkt_idx.price': None,
             'mkt_idx.cur_chng_pct': None, 'mkt_idx.is_limit_up': False,
             'mkt_idx.is_limit_down': False, 'mkt_idx.chng_pct_from_open': None,
             'signal_normal.signal_normal_17': False, 'signal_normal.signal_normal_26': False,
             'signal_normal.signal_normal_27': False, 'signal_normal.signal_normal_1': False,
             'signal_normal.signal_normal_2': False}

Z3_EQUITY_TRD_LAT_STAT = {'new_high_num': 0, 'new_low_num': 0, 'cross_ma5_up_num': 0, 'cross_ma5_down_num': 0,
                          'up_num': 0, 'down_num': 0, 'limit_up_num': 0, 'limit_down_num': 0, 'unchange_num': 0}

Z3_MIN_TX = {'operator': 'REMOVE'}

Z3_QUOTE_LEVEL1 = {'operator': 'REMOVE'}

# Z3_MIN_REALTIME = {'operator': 'REMOVE'}

Z3_INDU_CHANGE = {'indu_up_num': None, 'indu_down_num': None}

Z3_INDU_INFO = {'indu_market.chng_pct': None, 'indu_market.stk_up_num': None,
                'indu_market.stk_down_num': None, 'indu_market.keep_days_today': None}

Z3_INDU_QUOTE = {'operator': 'REMOVE'}

Z3_EQUITY_TRD_LAT_STAT1 = {'new_high_num': 0, 'new_low_num': 0, 'cross_ma5_up_num': 0, 'cross_ma5_down_num': 0,
                          'up_num': 0, 'down_num': 0, 'limit_up_num': 0, 'limit_down_num': 0, 'unchange_num': 0}

if DEBUG:
    TABLES = {'Z3_EQUITY_TRD_LAT_STAT': Z3_EQUITY_TRD_LAT_STAT}
else:
    TABLES = {'Z3_TOPIC_INFO': Z3_TOPIC_INFO, 'Z3_TOPIC_CHANGE': Z3_TOPIC_CHANGE, 'Z3_TOPIC_QUOTE': Z3_TOPIC_QUOTE,
              'Z3_EQUITY': Z3_EQUITY, 'Z3_EQUITY_TRD_LAT_STAT': Z3_EQUITY_TRD_LAT_STAT,
              'Z3_MIN_TX': Z3_MIN_TX, 'Z3_QUOTE_LEVEL1': Z3_QUOTE_LEVEL1}

