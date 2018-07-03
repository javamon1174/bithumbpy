# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
import logging
import math
import requests
import time
import urllib.parse

# https://www.bithumb.com/u1/US127

class Bithumbpy():
    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.all_currency = self._load_all_currency()

    def _load_all_currency(self):
        try:
            ticker = self.ticker('ALL')

            if ticker == None:
                return None

            if int(ticker['status']) != 0:
                logging.error('invalid status: %d' % int(ticker['status']))
                return None

            all_currency = []
            for key in ticker['data'].keys():
                all_currency.append(key)
            return all_currency
        except Exception as e:
            logging.error('_load_all_currency failed(%s)' % str(e))
            return None

    def _get(self, url, headers=None, data=None, params=None, result_code=200):
        resp = requests.get(url, headers=headers, data=data, params=params)
        if resp.status_code != result_code:
            logging.error('get(%s) failed(%d)' % (url, resp.status_code))
            if resp.text is not None:
                logging.error('resp: %s' % resp.text)
            return None
        return json.loads(resp.text)


    ###############################################################
    # Public API
    ###############################################################

    def ticker(self, currency='ALL'):
        URL = 'https://api.bithumb.com/public/ticker/'
        try:
            if currency != 'ALL' and currency not in self.all_currency:
                logging.error('invalid currency: %s' % currency)
                return None
            return self._get(URL + currency)
        except Exception as e:
            logging.error('ticker() failed(%s)' % str(e))
            return None

    def orderbook(self, currency='ALL', group_orders=1, count=5):
        URL = 'https://api.bithumb.com/public/orderbook/'
        try:
            if currency != 'ALL' and currency not in self.all_currency:
                logging.error('invalid currency: %s' % currency)
                return None
            if group_orders not in [0, 1]:
                logging.error('invalid group_orders: %d' % group_orders)
                return None
            if count < 1 or count > 50:
                logging.error('invalid count: %d' % count)
                return None
            params = {
                'group_orders': group_orders,
                'count': count
            }
            return self._get(URL + currency, params=params)
        except Exception as e:
            logging.error('orderbook() failed(%s)' % str(e))
            return None

    def transaction_history(self, currency='BTC', cont_no=None, count=20):
        URL = 'https://api.bithumb.com/public/transaction_history/'
        try:
            if currency not in self.all_currency:
                logging.error('invalid currency: %s' % currency)
                return None
            if count < 1 or count > 100:
                logging.error('invalid count: %d' % count)
                return None
            params = { 'count': count }
            if cont_no != 0:
                params['cont_no'] = cont_no
            return self._get(URL + currency, params=params)
        except Exception as e:
            logging.error('transaction_history() failed(%s)' % str(e))
            return None

    ###############################################################
    # Private API
    ###############################################################

    # TODO: implement me
    def info_account(self):
        raise NotImplementedError

    def info_balance(self):
        raise NotImplementedError

    def info_wallet_address(self):
        raise NotImplementedError

    def info_ticker(self):
        raise NotImplementedError

    def info_orders(self):
        raise NotImplementedError

    def info_user_transactions(self):
        raise NotImplementedError

    def info_order_detail(self):
        raise NotImplementedError

    def trade_place(self):
        raise NotImplementedError

    def trade_cancel(self):
        raise NotImplementedError

    def trade_btc_withdrawal(self):
        raise NotImplementedError

    def trade_krw_dposit(self):
        raise NotImplementedError

    def trade_market_buy(self):
        raise NotImplementedError

    def trade_market_sell(self):
        raise NotImplementedError

