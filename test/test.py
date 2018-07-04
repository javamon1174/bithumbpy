import logging
import apikey
from bithumbpy import Bithumbpy

KEY = apikey.KEY
SECRET = apikey.SECRET

logging.basicConfig(level=logging.DEBUG)
bithumb = Bithumbpy(api_key=KEY, api_secret=SECRET)

###############################################################
# Public API
###############################################################

# ticker
# logging.debug(bithumb.ticker('ALL'))
# logging.debug(bithumb.ticker('ADA'))

# orderbook
# logging.debug(bithumb.orderbook('BTC'))
# logging.debug(bithumb.orderbook('ETH', group_orders=0))
# logging.debug(bithumb.orderbook('ETH', count=10))
# logging.debug(bithumb.orderbook('ETH', group_orders=0, count=50))
# logging.debug(bithumb.orderbook('AAA'))

# transaction_history
# logging.debug(bithumb.transaction_history('BTC'))
# logging.debug(bithumb.transaction_history('ADA', count=1))
# logging.debug(bithumb.transaction_history('ADA', cont_no=10000))
# logging.debug(bithumb.transaction_history('ADA', count=10, cont_no=10000))
# logging.debug(bithumb.transaction_history('AAA'))

###############################################################
# Private API
###############################################################
# info/account
# logging.debug(bithumb.info_account('QTUM'))

# info/balance
# logging.debug(bithumb.info_balance())
# logging.debug(bithumb.info_balance('AE'))

# info/wallet_address
# logging.debug(bithumb.info_wallet_address())
# logging.debug(bithumb.info_wallet_address('QTUM'))

# info/ticker
# logging.debug(bithumb.info_ticker('ALL'))
# logging.debug(bithumb.info_ticker('AE'))

# info/orders
# logging.debug(bithumb.info_orders('VEN', '1530713502924607', 'ask'))
# logging.debug(bithumb.info_ticker('AE'))

# info/user_transactions
# logging.debug(bithumb.info_user_transactions('AE', 0))

# trade/place
# logging.debug(bithumb.trade_place('VEN', 1.0, 3500, 'ask'))

# info/order_detail
# logging.debug(bithumb.info_order_detail('VEN', '1530713673955645', 'ask'))

# trade/cancel
# logging.debug(bithumb.trade_cancel('VEN', '1530713673955645', 'ask'))

# trade/btc_withdrawal
# logging.debug(bithumb.trade_btc_withdrawal('VEN', '1530713673955645', 'ask'))

# trade/krw_deposit
# logging.debug(bithumb.trade_krw_deposit())

# trade/krw_withdrawal
# logging.debug(bithumb.trade_krw_withdrawal('002', 'your account', 100000000))

# trade/market_buy
# logging.debug(bithumb.trade_market_buy('QTUM', 1))

# trade/market_sell
# logging.debug(bithumb.trade_market_sell('VEN', 1))