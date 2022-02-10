import time
import pyupbit
import datetime
import requests
import pandas

access = "sCC0XTSFjGfQNhfEKWPx4hYl0rX7mwo7CyOAy9C5"
secret = "CNLY2VMUixCzltK3i9r5mn50zWK6RxozsJ8bGxN5"
myToken = "xoxb-3035444588257-3016200511750-Jj4irFwWVy8mo3G6aJog9RxU"


#  
#            엑시인피니티  

coinlist = ["KRW-AXS"]



# with open("ticker.txt", 'r') as fp :
#     for ticker in fp.readlines() :
#         ticker = ticker.replace('\n', '')
#         #print(ticker)



def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def get_target_price(coinlist):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(coinlist, interval="minute15", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * 0.5
    return target_price


# def get_ma6(ticker):
#     """6일 이동 평균선 조회"""
#     df = pyupbit.get_ohlcv(ticker, interval="minute15", count=6)
#     ma6 = df['close'].rolling(6).mean().iloc[-1]
#     return ma6



def get_ma5(coinlist):
    """5일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(coinlist, interval="minute15", count=5)
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5

def get_ma15(coinlist):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(coinlist, interval="minute15", count=15)
    ma15 = df['close'].rolling(20).mean().iloc[-1]
    return ma15

def get_ma40(coinlist):
    """40일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(coinlist, interval="minute15", count=40)
    ma40 = df['close'].rolling(40).mean().iloc[-1]
    return ma40







def rsi(ohlc: pandas.DataFrame, period: int = 14): 
    delta = ohlc["close"].diff() 
    ups, downs = delta.copy(), delta.copy() 
    ups[ups < 0] = 0 
    downs[downs > 0] = 0 
    
    AU = ups.ewm(com = period-1, min_periods = period).mean() 
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean() 
    RS = AU/AD 
    
    return pandas.Series(100 - (100/(1 + RS)), name = "RSI") 


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


# # 시작 메세지 슬랙 전송
# post_message(myToken,"#stock", "autotrade start")



    
while True:
    try:
        for i in range(len(coinlist)):
            data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute15")
            now_rsi = rsi(data, 14).iloc[-1] 


            ma40 = get_ma5(coinlist[i])
            ma15 = get_ma15(coinlist[i])
            

            target_price = pyupbit.get_current_price(coinlist[i])
            cur_price = pyupbit.get_current_price(coinlist[i])
            avr_price = upbit.get_avg_buy_price(coinlist[i])
            

            print("(코인명: ", coinlist[i], ") == 체결가:", avr_price, " == ", "(시간: ", datetime.datetime.now(), ") (RSI:", now_rsi , ") (현재:", cur_price, ") (수익률:"  ")" ) 
                        
        time.sleep(1)







        # 시장가 매수 함수 
        def buy(coin): 
            money = upbit.get_balance("KRW") 
            
            # if (hold[i] == False) : 
            
            if (money > 5000) : 
                res = upbit.buy_market_order(coin, money*0.9995) 
                hold[i] == True
            
            # elif (money > 50001) and (money < 100000): 
            #     res = upbit.buy_market_order(coin, money*0.5) 
            #     hold[i] == True

            # elif (money > 100001) and (money < 200000): 
            #     res = upbit.buy_market_order(coin, money*0.4) 
            #     hold[i] == True

            # elif (money > 200001) and (money < 300000): 
            #     res = upbit.buy_market_order(coin, money*0.3) 
            #     hold[i] == True
            
            # else :
            #     res = upbit.buy_market_order(coin, money*0.2) 
            #     hold[i] == True

            return
                
        time.sleep(1)



        # 시장가 매도 함수 
        def sell(coin): 
            amount = upbit.get_balance(coin) 
            cur_price = pyupbit.get_current_price(coin)

            total = amount * cur_price 
                

            # if (hold[i] == True) : 
       
            if total > 5000 : 
                res = upbit.sell_market_order(coin, amount) 
                hold[i] == False                    

            # elif (total > 50001) and (total < 100000): 
            #     res = upbit.sell_market_order(coin, amount*0.5) 
            #     hold[i] == False

            # elif (total > 100001) and (total < 200000): 
            #     res = upbit.sell_market_order(coin, amount*0.4)         
            #     hold[i] == False
            
            # elif (total > 200001) and (total < 300000): 
            #     res = upbit.sell_market_order(coin, amount*0.3) 
            #     hold[i] == False

            # else :
            #     res = upbit.sell_market_order(coin, amount*0.2) 
            #     hold[i] == False

            return


        time.sleep(1)



        lower29 = [] 
        higher70 = [] 
        hold = []
        higher5348 = []



        #initiate 
        for i in range(len(coinlist)): 
            lower29.append(False) 
            higher70.append(False)
            hold.append(False)
            higher5348.append(False)






        ################################################################################################################################################
        ################################################################################################################################################
        ################################################################################################################################################
        ################################################################################################################################################
        ################################################################################################################################################
        
        # 코인 미 보유시 < 구매로직 >

            if (hold[i] == False):


                # rsi가 29를 찍었는지 확인
                if (now_rsi <= 29) : 
                    lower29[i] = True
                    
    
                if (now_rsi <= 52) : 
                    higher70[i] = False 


                ###################################################################################################################################
                # (rsi가 29찍고 31까지 올라오면 매수)
                if ((now_rsi >= 31) and (lower29[i] == True)) : 
                    buy(coinlist[i])*0.5
                    lower29[i] = False             
                    hold[i] == True

                    print()
                    print()
                    print()
                    print("(과매도 매수 [코인]: ", coinlist[i], ") == 체결가:", avr_price, " == ", ") (시간: ", datetime.datetime.now(), ") (RSI:", now_rsi , ")")
                    print("(과매도 매수 [코인]: ", coinlist[i], ") == 체결가:", avr_price, " == ", ") (시간: ", datetime.datetime.now(), ") (RSI:", now_rsi , ")")
                    print()
                    print()
                    print()
                    #post_message(myToken,"#stock", coinlist[i] +"매수완료" +cur_price)
                
                    time.sleep(1)


                ###################################################################################################################################
                # # (40일선 위에 있을떄, 변동성 돌파 매수)
                if ((target_price < cur_price) and (ma40 < cur_price)) : 
                    buy(coinlist[i])             
                    hold[i] == True

                    print()
                    print()
                    print()
                    print("(변동성돌파 매수 [코인]: ", coinlist[i], ") == 체결가:", avr_price, " == ", ") (시간: ", datetime.datetime.now(), ")" )
                    print("(변동성돌파 매수 [코인]: ", coinlist[i], ") == 체결가:", avr_price, " == ", ") (시간: ", datetime.datetime.now(), ")" )
                    print()
                    print()
                    print()
                    #post_message(myToken,"#stock", coinlist[i] +"매수완료" +cur_price)
                    time.sleep(1)

            





        ################################################################################################################################################
        ################################################################################################################################################
        ################################################################################################################################################
        ################################################################################################################################################
        ################################################################################################################################################



            #else:



            ########################################################################################################
            # (rsi가 70이상 찍고오면  60프로만 매도.)
                elif ((now_rsi >= 70) and (higher70[i] == False)) :  
                    sell(coinlist[i])
                    higher70[i] = True 
                    hold[i] == False

                    print()
                    print()
                    print()
                    print("(과매수 매도 [코인]: ", coinlist[i], ") == 체결가:", avr_price, " == ", ") (시간: ", datetime.datetime.now(), ") (RSI:", now_rsi , ") (수익률:",  ")")
                    print("(과매수 매도 [코인]: ", coinlist[i], ") == 체결가:", avr_price, " == ", ") (시간: ", datetime.datetime.now(), ") (RSI:", now_rsi , ") (수익률:",  ")")
                    print()
                    print()
                    print()

                    time.sleep(1)



                # # ########################################################################################################
                # # # (rsi가 40 찍고 내려오면 매도)
                # if ((now_rsi >= 30) and (higher5348[i] == False)) :  
                #     sell(coinlist[i])
                #     higher5348[i] = True 
                #     hold[i] == False

                #     print()
                #     print()
                #     print()                
                #     print("(rsi5348매도 [코인]: ", coinlist[i], ") == 체결가:", avr_price, " == ", ") (시간: ", datetime.datetime.now(), ") (RSI:", now_rsi , ") (수익률:",  ")")
                #     print("(rsi5348매도 [코인]: ", coinlist[i], ") == 체결가:", avr_price, " == ", ") (시간: ", datetime.datetime.now(), ") (RSI:", now_rsi , ") (수익률:",  ")")
                #     print()
                #     print()
                #     print()

                #     time.sleep(1)



                # ########################################################################################################
                # # (매수가보다 현재가격이 약간 높아야 본절)
                if (cur_price*1.005 == avr_price) :  
                    sell(coinlist[i])
                    hold[i] == False
                    

                    print()
                    print()
                    print()                
                    print("(rsi5348매도 [코인]: ", coinlist[i], ") == 체결가:", avr_price, " == ", ") (시간: ", datetime.datetime.now(), ") (RSI:", now_rsi , ") (수익률:",  ")")
                    print("(rsi5348매도 [코인]: ", coinlist[i], ") == 체결가:", avr_price, " == ", ") (시간: ", datetime.datetime.now(), ") (RSI:", now_rsi , ") (수익률:",  ")")
                    print()
                    print()
                    print()

                    time.sleep(1)

                ########################################################################################################
                # (매수가격보다 현재가가 0.05% 하락시 손절)
                if (cur_price == (avr_price*0.995)) :  
                    sell(coinlist[i])*0.6
                    hold[i] == False

                    print()
                    print()
                    print()
                    print("(손절 [코인]: ", coinlist[i], ") == 체결가:", avr_price, " == ", ") (시간: ", datetime.datetime.now(), ") (RSI:", now_rsi , ") (수익률:",  ")")
                    print("(손절 [코인]: ", coinlist[i], ") == 체결가:", avr_price, " == ", ") (시간: ", datetime.datetime.now(), ") (RSI:", now_rsi , ") (수익률:",  ")")
                    print()
                    print()
                    print()

                    time.sleep(1)



                
            
        print("")
        

    except Exception as e:
        print(e)
    # post_message(myToken,"#stock", e)
        time.sleep(1)


