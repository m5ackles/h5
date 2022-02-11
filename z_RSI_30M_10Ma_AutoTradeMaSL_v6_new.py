import time
import pyupbit
import datetime
import requests
import pandas

access = "sCC0XTSFjGfQNhfEKWPx4hYl0rX7mwo7CyOAy9C5"
secret = "CNLY2VMUixCzltK3i9r5mn50zWK6RxozsJ8bGxN5"
myToken = "xoxb-3035444588257-3016200511750-Jj4irFwWVy8mo3G6aJog9RxU"

coin_title = "KRW-AXS"  #솔라나     KRW-BORA = 보라    WEMIX = 위믹스
coinlist = ["KRW-AXS"]
lower28 = [] 
higher70 = [] 
higher80 = [] 

#initiate 
for i in range(len(coinlist)): 
    lower28.append(False) 
    higher70.append(False)

def rsi(ohlc: pandas.DataFrame, period: int = 14): 
    delta = ohlc["close"].diff() 
    ups, downs = delta.copy(), delta.copy() 
    ups[ups < 0] = 0 
    downs[downs > 0] = 0 
    
    AU = ups.ewm(com = period-1, min_periods = period).mean() 
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean() 
    RS = AU/AD 
    
    return pandas.Series(100 - (100/(1 + RS)), name = "RSI") 
 

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_target_sellprice(ticker, k):
    """급락 매도 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=2)
    target_sellprice = df.iloc[0]['close'] - (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_sellprice


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma10(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_ma5(ticker):
    """5일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=5)
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5

def get_ma7(ticker):
    """7일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=7)
    ma7 = df['close'].rolling(7).mean().iloc[-1]
    return ma7

def get_ma30(ticker):
    """30일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=30)
    ma30 = df['close'].rolling(30).mean().iloc[-1]
    return ma30


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# 시작 메세지 슬랙 전송
post_message(myToken,"#stock", "autotrade start")

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(coin_title)
        end_time = start_time + datetime.timedelta(days=1)

        # RSI 
        data = pyupbit.get_ohlcv(ticker=coin_title, interval="minute60") 
        now_rsi = rsi(data, 14).iloc[-1] 
        print(datetime.datetime.now(),"[ ", coin_title, " ] RSI : " , now_rsi)
        time.sleep(10)

        target_price = get_target_price(coin_title, 0.5)
        target_sellprice = get_target_price(coin_title, 0.6)
        ma15 = get_ma10(coin_title)
        ma5 = get_ma5(coin_title)
        ma7 = get_ma7(coin_title)
        ma30 = get_ma30(coin_title)
        current_price = get_current_price(coin_title)

        # 15일선 위에 있으며, 변동성돌파시 매수,  또는 RSI가 28찍고 30이상이면 매수~~~~~~~~~~~~~~
        if target_price < current_price and ma15 < current_price or now_rsi == 28:
            lower28[i] = True
        elif now_rsi >= 33 and lower28[i] == True:
            krw = get_balance("KRW")
            if krw > 5000:
                buy_result = upbit.buy_market_order(coin_title, krw*0.9995)
                post_message(myToken,"#stock", " buy : " +str(buy_result))
                lower28[i] = False               
                time.sleep(60)

        # Rsi가 72 이상을 찍었으면 매도
        elif now_rsi >= 70 and higher70[i] == False:            
            sell_result = upbit.sell_market_order(coin_title, btc)
            post_message(myToken,"#stock", " sell (Take Profit): " +str(sell_result))
            higher70[i] = True
            time.sleep(60)

        elif now_rsi <= 60 : 
            higher70[i] = False

        else:
            btc = get_balance("BTC")

            #목표가격보다 0.2프로 하락시 손절,  또는 7일선 아래로 급락발생시 매도
            if current_price < target_price*0.999 or ma7 < target_sellprice:
                sell_result = upbit.sell_market_order(coin_title, btc*0.9995)
                post_message(myToken,"#stock", " sell (Stop Loss) : " +str(sell_result))
            time.sleep(60)

        time.sleep(1)
    except Exception as e:
        print(e)
        post_message(myToken,"#stock", e)
        time.sleep(1)