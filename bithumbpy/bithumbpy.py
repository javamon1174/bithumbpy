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

    def _get(self, url, params=None):
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            logging.error('get(%s) failed(%d)' % (url, resp.status_code))
            if resp.text is not None:
                logging.error('resp: %s' % resp.text)
            return None
        return json.loads(resp.text)

    def _get_sign(self, path, params, nonce):
        data = path + chr(0) + urllib.parse.urlencode(params) + chr(0) + nonce
        h = hmac.new(bytes(self.api_secret.encode('utf-8')), data.encode('utf-8'), hashlib.sha512)
        api_sign = base64.b64encode(h.hexdigest().encode('utf-8'))
        return api_sign.decode('utf-8')

    def _post(self, url, params):
        BASE_URL = 'https://api.bithumb.com'
        path = url[len(BASE_URL):]
        nonce = str(int(time.time() * 1000))
        headers = {
            'Api-Key': self.api_key,
            'Api-Sign': self._get_sign(path, params, nonce),
            'Api-Nonce': nonce
        }
        resp = requests.post(url, headers=headers, data=params)
        if resp.status_code != 200:
            logging.error('_post(%s) failed(%d)' % (url, resp.status_code))
            if resp.text is not None:
                logging.error('resp: %s' % resp.text)
            return None
        return json.loads(resp.text)

    ###############################################################
    # Public API
    ###############################################################

    def ticker(self, currency):
        URL = 'https://api.bithumb.com/public/ticker/'
        try:
            if currency != 'ALL' and currency not in self.all_currency:
                logging.error('invalid currency: %s' % currency)
                return None
            return self._get(URL + currency)
        except Exception as e:
            logging.error('ticker() failed(%s)' % str(e))
            return None

    def orderbook(self, currency, group_orders=1, count=5):
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

    def transaction_history(self, currency, cont_no=None, count=20):
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
    def info_account(self, currency):
        URL = 'https://api.bithumb.com/info/account'
        try:
            if currency not in self.all_currency:
                logging.error('invalid currency: %s' % currency)
                return None
            params = { 'currency': currency }
            return self._post(URL, params)
        except Exception as e:
            logging.error('info_account() failed(%s)' % str(e))
            return None

    def info_balance(self, currency):
        URL = 'https://api.bithumb.com/info/balance'
        try:
            if currency != 'ALL' and currency not in self.all_currency:
                logging.error('invalid currency: %s' % currency)
                return None
            params = { 'currency': currency}
            return self._post(URL, params)
        except Exception as e:
            logging.error('info_balance() failed(%s)' % str(e))
            return None

    def info_wallet_address(self, currency):
        URL = 'https://api.bithumb.com/info/wallet_address'
        try:
            if currency not in self.all_currency:
                logging.error('invalid currency: %s' % currency)
                return None
            params = { 'currency': currency }
            return self._post(URL, params)
        except Exception as e:
            logging.error('info_wallet_address() failed(%s)' % str(e))
            return None


    def info_ticker(self, currency):
        URL = 'https://api.bithumb.com/info/ticker'
        try:
            if currency not in self.all_currency:
                logging.error('invalid currency: %s' % currency)
                return None
            params = {
                'order_currency': currency,
                'payment_currency': 'KRW'
            }
            return self._post(URL, params)
        except Exception as e:
            logging.error('info_ticker() failed(%s)' % str(e))
            return None

    def info_orders(self, currency, order_id, type, count=None, after=None):
        URL = 'https://api.bithumb.com/info/orders'
        try:
            if currency not in self.all_currency:
                logging.error('invalid currency: %s' % currency)
                return None
            if type not in ['bid', 'ask']:
                logging.error('invalid type: %s' % type)
                return None
            params = {
                'currency': currency,
                'order_id': order_id,
                'type': type
            }
            if after is not None:
                params['after'] = after
            if count is not None:
                params['count'] = count
            return self._post(URL, params)
        except Exception as e:
            logging.error('info_orders() failed(%s)' % str(e))
            return None

    def info_user_transactions(self, currency, searchGb, offset=None, count=None):
        URL = 'https://api.bithumb.com/info/user_transactions'
        try:
            if currency not in self.all_currency:
                logging.error('invalid currency: %s' % currency)
                return None
            if searchGb not in [0, 1, 2, 3, 4, 5, 9]:
                logging.error('invalid searchGb: %d' % searchGb)
                return None
            params = {
                'currency': currency,
                'searchGb': searchGb
            }
            if offset is not None:
                params['offset'] = offset
            if count is not None:
                params['count'] = count
            return self._post(URL, params)
        except Exception as e:
            logging.error('info_user_transactions() failed(%s)' % str(e))
            return None

    def trade_place(self, currency, units, price, type):
        URL = 'https://api.bithumb.com/trade/place'
        try:
            if currency not in self.all_currency:
                logging.error('invalid currency: %s' % currency)
                return None
            if type not in ['bid', 'ask']:
                logging.error('invalid type: %s' % type)
                return None
            params = {
                'order_currency': currency,
                'Payment_currency': 'KRW',
                'type': type,
                'price': price,
                'units': units
            }
            return self._post(URL, params)
        except Exception as e:
            logging.error('trade_place() failed(%s)' % str(e))
            return None

    def info_order_detail(self, currency, order_id, type):
        URL = 'https://api.bithumb.com/info/order_detail'
        try:
            if currency not in self.all_currency:
                logging.error('invalid currency: %s' % currency)
                return None
            if type not in ['bid', 'ask']:
                logging.error('invalid type: %s' % type)
                return None
            params = {
                'currency': currency,
                'type': type,
                'order_id': order_id
            }
            return self._post(URL, params)
        except Exception as e:
            logging.error('info_order_detail() failed(%s)' % str(e))
            return None

    def trade_cancel(self, currency, order_id, type):
        URL = 'https://api.bithumb.com/trade/cancel'
        try:
            if currency not in self.all_currency:
                logging.error('invalid currency: %s' % currency)
                return None
            if type not in ['bid', 'ask']:
                logging.error('invalid type: %s' % type)
                return None
            params = {
                'currency': currency,
                'type': type,
                'order_id': order_id
            }
            return self._post(URL, params)
        except Exception as e:
            logging.error('trade_cancel() failed(%s)' % str(e))
            return None

    # not tested
    def trade_btc_withdrawal(self, currency, units, address, destination):
        URL = 'https://api.bithumb.com/trade/btc_withdrawal'
        try:
            if currency not in self.all_currency:
                logging.error('invalid currency: %s' % currency)
                return None
            params = {
                'currency': currency,
                'address': address,
                'destination': destination,
                'units': units
            }
            return self._post(URL, params)
        except Exception as e:
            logging.error('trade_btc_withdrawal() failed(%s)' % str(e))
            return None


    def trade_krw_deposit(self):
        URL = 'https://api.bithumb.com/trade/krw_deposit'
        try:
            params = {}
            return self._post(URL, params)
        except Exception as e:
            logging.error('trade_krw_deposit() failed(%s)' % str(e))
            return None

    # not tested
    def trade_krw_withdrawal(self, bank, account, price):
        URL = 'https://api.bithumb.com/trade/krw_withdrawal'
        try:
            params = {
                'bank': bank,
                'account': account,
                'price': price
            }
            return self._post(URL, params)
        except Exception as e:
            logging.error('trade_krw_withdrawal() failed(%s)' % str(e))
            return None

    def trade_market_buy(self, currency, units):
        URL = 'https://api.bithumb.com/trade/market_buy'
        try:
            if currency not in self.all_currency:
                logging.error('invalid currency: %s' % currency)
                return None
            params = {
                'currency': currency,
                'units': units
            }
            return self._post(URL, params)
        except Exception as e:
            logging.error('trade_market_buy() failed(%s)' % str(e))
            return None

    def trade_market_sell(self, currency, units):
        URL = 'https://api.bithumb.com/trade/market_sell'
        try:
            if currency not in self.all_currency:
                logging.error('invalid currency: %s' % currency)
                return None
            params = {
                'currency': currency,
                'units': units
            }
            return self._post(URL, params)
        except Exception as e:
            logging.error('trade_market_sell() failed(%s)' % str(e))
            return None

