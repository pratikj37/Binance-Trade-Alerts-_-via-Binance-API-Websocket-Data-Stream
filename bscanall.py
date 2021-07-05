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

def difference_to_color(difference):
    	if(difference <= 0.1):
		print(Fore.YELLOW)
	elif(difference > 0.1 and difference < 0.8):
		print(Fore.WHITE)
	elif(difference >= 0.8 and difference <= 1.4):
		print(Fore.MAGENTA)
	elif(difference > 1.4 and difference <= 2.5):
		print(Fore.BLUE)
	elif(difference > 2.5 and difference <= 4.0):
		print(Fore.GREEN)
	elif(difference > 4.0 and difference <= 5.0):
		print(Fore.CYAN)
	elif(difference > 5.0):
		print(Fore.RED)
	else:
		print(Fore.WHITE)

def process_message(msg):
    	global first_run_flag
	for currency in msg:
		x = currency_container(currency)
		
		if(x.symbol[-len(PAIRS):] == PAIRS): #only gets specified pairs
			if(first_run_flag == 0):
				price_list.append(x) 
			elif(first_run_flag == 1 and x.symbol in coin):
				ct = time.time()
				for stored_currency in price_list:
					if(x.symbol == stored_currency.symbol and (ct - stored_currency.time_stamp) > 1):
						priceDiff = ((x.bid_price - stored_currency.bid_price) / stored_currency.bid_price) * 100
						volDiff = ((x.volume - stored_currency.volume) / stored_currency.volume) * 100
						
						if(priceDiff > ONE_S_PRICE_DIFFERENCE_THRESHOLD and volDiff > VOLUME_DIFFERENCE_THRESHOLD and x.volume > MINIMUM_VOLUME_THRESHOLD):
							flag = "PRICE AND VOL!"
							sym = "SYM: " + str(stored_currency.symbol)
							pDiff = "P DIFF: " + str(round(priceDiff, 1))
							vDiff = "DIFF: " + str(round(volDiff, 1))
							vol = "VOL: " + str(round(x.volume, 1))
							cur = "CUR:" + str(x.bid_price)
							pre = "PRE:" + str(stored_currency.bid_price)
							difference_to_color(priceDiff)
							print(Fore.RED)
							print(Back.WHITE)
							T = dt.datetime.now()
							if(TRADING_VIEW_LINK == 1):
								print(flag, sym, pDiff, vDiff, vol, T,pre, cur, 'https://www.tradingview.com/chart/?symbol=Binance:'+str(stored_currency.symbol),sep = " || ")
							else:
								print(flag, sym, pDiff, vDiff, vol, T,pre, cur, sep = " || ")
							print(Back.BLACK)
						elif(priceDiff > ONE_S_PRICE_DIFFERENCE_THRESHOLD and x.volume > MINIMUM_VOLUME_THRESHOLD):
							flag = "PRICE!"
							sym = "SYM: " + str(stored_currency.symbol)
							pDiff = "DIFF: " + str(round(priceDiff, 1))
							vol = "VOL: " + str(round(x.volume, 1))
							cur = "CUR:" + str(x.bid_price)
							pre = "PRE:" + str(stored_currency.bid_price)
							difference_to_color(priceDiff)
							T = dt.datetime.now()
							if(TRADING_VIEW_LINK == 1):
								print(flag, sym, pDiff, vol,T,pre, cur, 'https://www.tradingview.com/chart/?symbol=Binance:'+str(stored_currency.symbol), sep = " || ")
							else:
								print(flag, sym, pDiff, vol,T,pre, cur, sep = " || ")
						elif(volDiff > VOLUME_DIFFERENCE_THRESHOLD and x.volume > MINIMUM_VOLUME_THRESHOLD):
							flag = "VOLUME!"
							sym = "SYM: " + str(stored_currency.symbol)
							vDiff = "DIFF: " + str(round(volDiff, 1))
							vol = "VOL: " + str(round(x.volume, 1))
							cur = "CUR:" + str(x.bid_price)
							pre = "PRE:" + str(stored_currency.bid_price)
							difference_to_color(volDiff)
							T = dt.datetime.now()
							if(TRADING_VIEW_LINK == 1):
								print(flag, sym, vDiff, vol,T,pre, cur, 'https://www.tradingview.com/chart/?symbol=Binance:'+str(stored_currency.symbol), sep = " || ")
							else:
								print(flag, sym, vDiff, vol,T,pre, cur, sep = " || ")
								
						if((ct - stored_currency.ten_sec_time_stamp) >= 10):
							ten_second_price_diff = ((x.bid_price - stored_currency.ten_sec_start_bid_price) / stored_currency.ten_sec_start_bid_price) * 100
							if(ten_second_price_diff > TEN_S_PRICE_DIFFERENCE_THRESHOLD):
								flag = "10S FLAG!"
								sym = "SYM: " + str(stored_currency.symbol)
								ten_second_pDiff = "DIFF: " + str(round(ten_second_price_diff, 1))
								cur = "CUR:" + str(x.bid_price)
								pre = "PRE:" + str(stored_currency.bid_price)
								difference_to_color(ten_second_price_diff)
								T = dt.datetime.now()
								if(TRADING_VIEW_LINK == 1):
									print(flag, sym, ten_second_pDiff,T,pre, cur, 'https://www.tradingview.com/chart/?symbol=Binance:'+str(stored_currency.symbol),sep = "  ||  ")
								else:
									print(flag, sym, ten_second_pDiff,T,pre, cur, sep = "  ||  ")
							stored_currency.ten_sec_start_bid_price = x.bid_price
							stored_currency.ten_sec_time_stamp = ct
							
						if((ct - stored_currency.fifteen_sec_time_stamp) >= 15):
							fifteen_second_price_diff = ((x.bid_price - stored_currency.fifteen_sec_start_bid_price) / stored_currency.fifteen_sec_start_bid_price) * 100
							if(fifteen_second_price_diff > FIFTEEN_S_PRICE_DIFFERENCE_THRESHOLD):
								flag = "15S FLAG!"
								sym = "SYM: " + str(stored_currency.symbol)
								fifteen_second_pDiff = "DIFF: " + str(round(fifteen_second_price_diff, 1))
								cur = "CUR:" + str(x.bid_price)
								pre = "PRE:" + str(stored_currency.bid_price)
								difference_to_color(fifteen_second_price_diff)
								T = dt.datetime.now()
								if(TRADING_VIEW_LINK == 1):
									print(flag, sym, fifteen_second_pDiff,T,pre, cur, 'https://www.tradingview.com/chart/?symbol=Binance:'+str(stored_currency.symbol), sep = "  ||  ")
								else:
									print(flag, sym, fifteen_second_pDiff,T,pre, cur, sep = "  ||  ")
							stored_currency.fifteen_sec_start_bid_price = x.bid_price
							stored_currency.fifteen_sec_time_stamp = ct
							
						if((ct - stored_currency.twenty_sec_time_stamp) >= 20):
							twenty_second_price_diff = ((x.bid_price - stored_currency.twenty_sec_start_bid_price) / stored_currency.twenty_sec_start_bid_price) * 100
							if(twenty_second_price_diff > TWENTY_S_PRICE_DIFFERENCE_THRESHOLD):
								flag = "20S FLAG!"
								sym = "SYM: " + str(stored_currency.symbol)
								twenty_second_pDiff = "DIFF: " + str(round(twenty_second_price_diff, 1))
								cur = "CUR:" + str(x.bid_price)
								pre = "PRE:" + str(stored_currency.bid_price)
								difference_to_color(twenty_second_price_diff)
								T = dt.datetime.now()
								if(TRADING_VIEW_LINK == 1):
									print(flag, sym, twenty_second_pDiff,T,pre, cur, 'https://www.tradingview.com/chart/?symbol=Binance:'+str(stored_currency.symbol), sep = "  ||  ")
								else:
									print(flag, sym, twenty_second_pDiff,T,pre, cur, sep = "  ||  ")
							stored_currency.twenty_sec_start_bid_price = x.bid_price
							stored_currency.twenty_sec_time_stamp = ct
						
						if((ct - stored_currency.thirty_sec_time_stamp) >= 30):
							thirty_second_price_diff = ((x.bid_price - stored_currency.thirty_sec_start_bid_price) / stored_currency.thirty_sec_start_bid_price) * 100
							if(thirty_second_price_diff > THIRTY_S_PRICE_DIFFERENCE_THRESHOLD):
								flag = "30S FLAG!"
								sym = "SYM: " + str(stored_currency.symbol)
								thirty_second_pDiff = "DIFF: " + str(round(thirty_second_price_diff, 1))
								cur = "CUR:" + str(x.bid_price)
								pre = "PRE:" + str(stored_currency.bid_price)
								difference_to_color(thirty_second_price_diff)
								T = dt.datetime.now()
								if(TRADING_VIEW_LINK == 1):
									print(flag, sym, thirty_second_pDiff,T,pre, cur, 'https://www.tradingview.com/chart/?symbol=Binance:'+str(stored_currency.symbol), sep = "  ||  ")
								else:
									print(flag, sym, thirty_second_pDiff,T,pre, cur, sep = "  ||  ")
							stored_currency.thirty_sec_start_bid_price = x.bid_price
							stored_currency.thirty_sec_time_stamp = ct
						
						if((ct - stored_currency.one_min_time_stamp) >= 60):
							one_min_price_diff = ((x.bid_price - stored_currency.one_min_start_bid_price) / stored_currency.one_min_start_bid_price) * 100
							if(one_min_price_diff > ONE_M_PRICE_DIFFERENCE_THRESHOLD):
								flag = "60S FLAG!"
								sym = "SYM: " + str(stored_currency.symbol)
								one_min_pDiff = "DIFF: " + str(round(one_min_price_diff, 1))
								cur = "CUR:" + str(x.bid_price)
								pre = "PRE:" + str(stored_currency.bid_price)
								difference_to_color(one_min_price_diff)
								T = dt.datetime.now()
								if(TRADING_VIEW_LINK == 1):
									print(flag, sym, one_min_pDiff,T,pre, cur, 'https://www.tradingview.com/chart/?symbol=Binance:'+str(stored_currency.symbol), sep = "  ||  ")
								else:
									print(flag, sym, one_min_pDiff,T,pre, cur, sep = "  ||  ")
							stored_currency.one_min_start_bid_price = x.bid_price
							stored_currency.one_min_time_stamp = ct
						
						if((ct - stored_currency.two_min_time_stamp) >= 120):
							two_min_price_diff = ((x.bid_price - stored_currency.two_min_start_bid_price) / stored_currency.two_min_start_bid_price) * 100
							if(two_min_price_diff > TWO_M_PRICE_DIFFERENCE_THRESHOLD):
								flag = "120S FLAG!"
								sym = "SYM: " + str(stored_currency.symbol)
								two_min_pDiff = "DIFF: " + str(round(two_min_price_diff, 1))
								cur = "CUR:" + str(x.bid_price)
								pre = "PRE:" + str(stored_currency.bid_price)
								difference_to_color(two_min_price_diff)
								T = dt.datetime.now()
								if(TRADING_VIEW_LINK == 1):
									print(flag, sym, two_min_pDiff,T,pre, cur, 'https://www.tradingview.com/chart/?symbol=Binance:'+str(stored_currency.symbol), sep = "  ||  ")
								else:
									print(flag, sym, two_min_pDiff,T,pre, cur, sep = "  ||  ")
							stored_currency.two_min_start_bid_price = x.bid_price
							stored_currency.two_min_time_stamp = ct
						
						if((ct - stored_currency.five_min_time_stamp) >= 300):
							five_min_price_diff = ((x.bid_price - stored_currency.five_min_start_bid_price) / stored_currency.five_min_start_bid_price) * 100
							if(five_min_price_diff > FIVE_M_PRICE_DIFFERENCE_THRESHOLD):
								flag = "300S FLAG!"
								sym = "SYM: " + str(stored_currency.symbol)
								five_min_pDiff = "DIFF: " + str(round(five_min_price_diff, 1))
								cur = "CUR:" + str(x.bid_price)
								pre = "PRE:" + str(stored_currency.bid_price)
								difference_to_color(five_min_price_diff)
								T = dt.datetime.now()
								if(TRADING_VIEW_LINK == 1):
									print(flag, sym, five_min_pDiff,T,pre, cur, 'https://www.tradingview.com/chart/?symbol=Binance:'+str(stored_currency.symbol), sep = "  ||  ")
								else:
									print(flag, sym, five_min_pDiff,T,pre, cur, sep = "  ||  ")
							stored_currency.five_min_start_bid_price = x.bid_price
							stored_currency.five_min_time_stamp = ct
							
						if((ct - stored_currency.ten_min_time_stamp) >= 600):
							ten_min_price_diff = ((x.bid_price - stored_currency.ten_min_start_bid_price) / stored_currency.ten_min_start_bid_price) * 100
							if(ten_min_price_diff > TEN_M_PRICE_DIFFERENCE_THRESHOLD):
								flag = "600S FLAG!"
								sym = "SYM: " + str(stored_currency.symbol)
								ten_min_pDiff = "DIFF: " + str(round(ten_min_price_diff, 1))
								cur = "CUR:" + str(x.bid_price)
								pre = "PRE:" + str(stored_currency.bid_price)
								difference_to_color(ten_min_price_diff)
								T = dt.datetime.now()
								if(TRADING_VIEW_LINK == 1):
									print(flag, sym, ten_min_pDiff,T,pre, cur,'https://www.tradingview.com/chart/?symbol=Binance:'+str(stored_currency.symbol), sep = "  ||  ")
								else:
									print(flag, sym, ten_min_pDiff,T,pre, cur, sep = "  ||  ")
							stored_currency.ten_min_start_bid_price = x.bid_price
							stored_currency.ten_min_time_stamp = ct
							
						if((ct - stored_currency.fifteen_min_time_stamp) >= 900):
							fifteen_min_price_diff = ((x.bid_price - stored_currency.fifteen_min_start_bid_price) / stored_currency.fifteen_min_start_bid_price) * 100
							if(fifteen_min_price_diff > FIFTEEN_M_PRICE_DIFFERENCE_THRESHOLD):
								flag = "900S FLAG!"
								sym = "SYM: " + str(stored_currency.symbol)
								fifteen_min_pDiff = "DIFF: " + str(round(fifteen_min_price_diff, 1))
								cur = "CUR:" + str(x.bid_price)
								pre = "PRE:" + str(stored_currency.bid_price)
								difference_to_color(fifteen_min_price_diff)
								T = dt.datetime.now()
								if(TRADING_VIEW_LINK == 1):
									print(flag, sym, fifteen_min_pDiff,T,pre, cur, 'https://www.tradingview.com/chart/?symbol=Binance:'+str(stored_currency.symbol),sep = "  ||  ")
								else:
									print(flag, sym, fifteen_min_pDiff,T,pre, cur, sep = "  ||  ")
							stored_currency.fifteen_min_start_bid_price = x.bid_price
							stored_currency.fifteen_min_time_stamp = ct
							
						stored_currency.bid_price = x.bid_price
						stored_currency.ask_price = x.ask_price
						stored_currency.volume = x.volume
						stored_currency.time_stamp = ct	
	first_run_flag = 1 

if __name__ == "__main__":
    	price_list = []
	first_run_flag = 0
	init()

	print(Style.BRIGHT)
	print("Initialising scanner...")
	try:
		client = Client(PUBLIC_API_KEY, PRIVATE_API_KEY)
		bm = BinanceSocketManager(client)
		conn_key = bm.start_ticker_socket(process_message)
		bm.start()
		print("Initialised successfully!")
		print(Style.BRIGHT)
		print(COLOUR_CODED_VALUES)
	except:
		print("Error - exiting...")
		sys.exit(0)


#TIMER TO DISPLAY COLOR RANGE EVERY 
while True:
	delta_minutes = (dt.datetime.now() - T).seconds
	if delta_minutes >= DELAY_FOR_COLOR_RANGE:
		print(Style.BRIGHT)
		print(COLOUR_CODED_VALUES)
	sleep(DELAY_FOR_COLOR_RANGE) 
