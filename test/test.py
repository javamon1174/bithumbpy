import logging
from bithumbpy import Bithumbpy

KEY = ''
SECRET = ''

logging.basicConfig(level=logging.DEBUG)
bithumb = Bithumbpy(api_key=KEY, api_secret=SECRET)

###############################################################
# Public API
###############################################################

# ticker
# logging.debug('================================')
# logging.debug(bithumb.ticker('QTUM'))
# logging.debug('================================')
# logging.debug(bithumb.ticker('ADA'))
# logging.debug('================================')
# logging.debug(bithumb.ticker('AAA'))
# logging.debug('================================')

# orderbook
# logging.debug('================================')
# logging.debug(bithumb.orderbook('BTC'))
# logging.debug('================================')
# logging.debug(bithumb.orderbook('ETH', group_orders=0))
# logging.debug('================================')
# logging.debug(bithumb.orderbook('ETH', count=10))
# logging.debug('================================')
# logging.debug(bithumb.orderbook('ETH', group_orders=0, count=50))
# logging.debug('================================')
# logging.debug(bithumb.orderbook('AAA'))
# logging.debug('================================')

# transaction_history
logging.debug('================================')
logging.debug(bithumb.transaction_history('BTC'))
logging.debug('================================')
logging.debug(bithumb.transaction_history('ADA', count=1))
logging.debug('================================')
logging.debug(bithumb.transaction_history('ADA', cont_no=10000))
logging.debug('================================')
logging.debug(bithumb.transaction_history('ADA', count=10, cont_no=10000))
logging.debug('================================')
logging.debug(bithumb.transaction_history('AAA'))
logging.debug('================================')

###############################################################
# Private API
###############################################################
# TODO