import time
from time import sleep
import sys
from binance.websockets import BinanceSocketManager
from binance.client import Client
from twisted.internet import reactor
from colorama import init, Fore, Back, Style
import datetime as dt

PUBLIC_API_KEY = ''														#API KEYS FROM BINANCE.COM (NOT REQUIRED!)
PRIVATE_API_KEY = ''														#API KEYS FROM BINANCE.COM (NOT REQUIRED!)
TRADING_VIEW_LINK = 0														#ENABLE TRADING VIEW LINK (DISABLED BY DEFAULT)
PAIRS = "USDT"															#BASE TRADING COIN: BTC/ETH/USDT/BNB/PERPETUAL
DELAY_FOR_COLOR_RANGE = 900													  #TIME TO DISPLAY COLOR RANGE CHART IN SECONDS
MINIMUM_VOLUME_THRESHOLD = 2400.0												  #MINIMUM VOLUME THRESHOLD
ONE_S_PRICE_DIFFERENCE_THRESHOLD = 1.0												#1S PRICE DIFFERENCE IN PERCENTAGE THRESHOLD
TEN_S_PRICE_DIFFERENCE_THRESHOLD = 0.75												#10S PRICE DIFFERENCE IN PERCENTAGE THRESHOLD
FIFTEEN_S_PRICE_DIFFERENCE_THRESHOLD = 1.0											#15S PRICE DIFFERENCE IN PERCENTAGE THRESHOLD
TWENTY_S_PRICE_DIFFERENCE_THRESHOLD = 1.4											#20S PRICE DIFFERENCE IN PERCENTAGE THRESHOLD
THIRTY_S_PRICE_DIFFERENCE_THRESHOLD = 1.8											#30S PRICE DIFFERENCE IN PERCENTAGE THRESHOLD
ONE_M_PRICE_DIFFERENCE_THRESHOLD = 2.1												#1M PRICE DIFFERENCE IN PERCENTAGE THRESHOLD
TWO_M_PRICE_DIFFERENCE_THRESHOLD = 2.5												#2M PRICE DIFFERENCE IN PERCENTAGE THRESHOLD
FIVE_M_PRICE_DIFFERENCE_THRESHOLD = 3.0												#5M PRICE DIFFERENCE IN PERCENTAGE THRESHOLD
TEN_M_PRICE_DIFFERENCE_THRESHOLD = 3.5												#10M PRICE DIFFERENCE IN PERCENTAGE THRESHOLD
FIFTEEN_M_PRICE_DIFFERENCE_THRESHOLD = 4.0											#15M PRICE DIFFERENCE IN PERCENTAGE THRESHOLD
VOLUME_DIFFERENCE_THRESHOLD = 1.0												  #VOLUME DIFFERENCE IN PERCENTAGE THRESHOLD

#coins
#coin = ['BNBUSDT','ADAUSDT','DOTUSDT','LTCUSDT','XRPUSDT','LINKUSDT','UNIUSDT','SXPUSDT','BCHUSDT','EOSUSDT','TRXUSDT','SUSHIUSDT','XLMUSDT','AAVEUSDT','FILUSDT','XTZUSDT','AVAXUSDT','FTMUSDT','YFIUSDT','GRTUSDT','DOGEUSDT','ATOMUSDT','1INCHUSDT','THETAUSDT','ETCUSDT','CRVUSDT','MATICUSDT','ALGOUSDT','SOLUSDT','VETUSDT','ALPHAUSDT','ENJUSDT','NEOUSDT','EGLDUSDT','KSMUSDT','IOTAUSDT','RSRUSDT','XMRUSDT','ONTUSDT','ZECUSDT','DASHUSDT','OCEANUSDT','RUNEUSDT','BANDUSDT','ZILUSDT','TOMOUSDT','SRMUSDT','SKLUSDT','BATUSDT','SNXUSDT','RENUSDT','COMPUSDT','NEARUSDT','BLZUSDT','IOSTUSDT','YFIIUSDT','OMGUSDT','ICXUSDT','QTUMUSDT','BZRXUSDT','AXSUSDT','ZRXUSDT','KAVAUSDT','HNTUSDT','FLMUSDT','TRBUSDT','BALUSDT','MKRUSDT','LRCUSDT','WAVESUSDT','KNCUSDT','BELUSDT','CTKUSDT','RLCUSDT','CVCUSDT','STORJUSDT','ZENUSDT','CHZUSDT','XEMUSDT','ANKRUSDT','SFPUSDT','LITUSDT','RVNUSDT','BTSUSDT','DODOUSDT','UNFIUSDT','BTCSTUSDT','AKROUSDT']
coin = ['BNBUSDT','ADAUSDT','DOTUSDT','LTCUSDT','XRPUSDT','LINKUSDT','UNIUSDT','SXPUSDT','BCHUSDT','EOSUSDT','TRXUSDT','SUSHIUSDT','XLMUSDT','AAVEUSDT','FILUSDT','XTZUSDT','AVAXUSDT','FTMUSDT','YFIUSDT','GRTUSDT','DOGEUSDT','ATOMUSDT','1INCHUSDT','THETAUSDT','ETCUSDT','CRVUSDT','MATICUSDT','ALGOUSDT','SOLUSDT','VETUSDT','ALPHAUSDT','ENJUSDT','NEOUSDT','EGLDUSDT','KSMUSDT','IOTAUSDT','RSRUSDT','XMRUSDT','ONTUSDT','ZECUSDT','DASHUSDT','OCEANUSDT','RUNEUSDT','BANDUSDT','ZILUSDT','TOMOUSDT','SRMUSDT','SKLUSDT','BATUSDT','SNXUSDT','RENUSDT','COMPUSDT','NEARUSDT','BLZUSDT','IOSTUSDT','YFIIUSDT','OMGUSDT','ICXUSDT','QTUMUSDT','BZRXUSDT','AXSUSDT','ZRXUSDT','KAVAUSDT','HNTUSDT','FLMUSDT','TRBUSDT','BALUSDT','MKRUSDT','LRCUSDT','WAVESUSDT','KNCUSDT','BELUSDT','CTKUSDT','RLCUSDT','CVCUSDT','STORJUSDT','ZENUSDT','CHZUSDT','XEMUSDT','ANKRUSDT','SFPUSDT','LITUSDT','RVNUSDT','BTSUSDT','DODOUSDT','UNFIUSDT','BTCSTUSDT','AKROUSDT','ONEUSDT','ALICEUSDT','LINAUSDT']

T = dt.datetime.now()																#START TIME (DO NOT CHANGE)
COLOUR_CODED_VALUES = (
		(Fore.BLACK)
		+(Style.NORMAL)
		+(Back.YELLOW + ' diff <= 0.1 ')
		+(Back.WHITE + ' > 0.1 & < 0.8 ')
		+(Back.MAGENTA + ' >= 0.8 & <= 1.4 ')
		+(Back.BLUE + ' > 1.4 & <= 2.5 ')
		+(Back.GREEN + ' > 2.5 & <= 4.0 ')
		+(Back.CYAN + ' > 4.0 & <= 5.0 ')
		+(Back.RED + ' diff > 5.0 ')
		+(Style.RESET_ALL)
	)

class currency_container:
	def __init__(self, currencyArray):
		self.symbol = currencyArray['s']																									#symbol
		self.bid_price = float(currencyArray['b'])																							#best bid price
		self.ask_price = float(currencyArray['a'])																							#best ask price
		self.open_price = float(currencyArray['o'])																							#open price
		self.high_price = float(currencyArray ['h'])																						#high price
		self.low_price = float(currencyArray['l'])																							#low price
		self.number_of_trades = float(currencyArray['n'])																					#total number of trades
		self.price_change = float(currencyArray['p'])																						#price change
		self.percent_change = float(currencyArray['P'])																						#% price change
		self.volume = float(currencyArray['q'])																								#volume
		initial_timestamp = time.time()																										#initial timestamp
		self.time_stamp = initial_timestamp																									
		self.ten_sec_time_stamp = initial_timestamp
		self.ten_sec_start_bid_price = float(currencyArray['b'])
		self.fifteen_sec_time_stamp = initial_timestamp
		self.fifteen_sec_start_bid_price = float(currencyArray['b'])
		self.twenty_sec_time_stamp = initial_timestamp
		self.twenty_sec_start_bid_price = float(currencyArray['b'])
		self.thirty_sec_time_stamp = initial_timestamp
		self.thirty_sec_start_bid_price = float(currencyArray['b'])
		self.one_min_time_stamp = initial_timestamp
		self.one_min_start_bid_price = float(currencyArray['b'])
		self.two_min_time_stamp = initial_timestamp
		self.two_min_start_bid_price = float(currencyArray['b'])
		self.five_min_time_stamp = initial_timestamp
		self.five_min_start_bid_price = float(currencyArray['b'])
		self.ten_min_time_stamp = initial_timestamp
		self.ten_min_start_bid_price = float(currencyArray['b'])
		self.fifteen_min_time_stamp = initial_timestamp
		self.fifteen_min_start_bid_price = float(currencyArray['b'])
