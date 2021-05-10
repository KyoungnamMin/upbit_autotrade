import time
import pyupbit
import datetime

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma20(ticker):
    """20일 이동 평균선 조회"""
    df20 = pyupbit.get_ohlcv(ticker, interval="day", count=20)
    ma20 = df20['close'].rolling(20).mean().iloc[-1]
    return ma20

def get_ma30(ticker):
    """30일 이동 평균선 조회"""
    df30 = pyupbit.get_ohlcv(ticker, interval="day", count=30)
    ma30 = df30['close'].rolling(30).mean().iloc[-1]
    return ma30

def get_ma60(ticker):
    """60일 이동 평균선 조회"""
    df60 = pyupbit.get_ohlcv(ticker, interval="day", count=60)
    ma60 = df60['close'].rolling(60).mean().iloc[-1]
    return ma60

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인

access = 'your key'
secret = 'your key'

upbit = pyupbit.Upbit(access, secret)
target_coin = "KRW-BTC"
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(target_coin)
        end_time = start_time + datetime.timedelta(days=1)

        # 09:00:00 < 현재 시간 < 08:59:50
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price(target_coin, 0.5)
            # 20일 이평선, 60일 이평선 조회
            ma20 = get_ma20(target_coin)
            ma30 = get_ma30(target_coin)
            ma60 = get_ma60(target_coin)
            current_price = get_current_price(target_coin)
            # 매수 타이밍
            # 변동성 돌파 전략target_price < current_price
            # 골든크로스 : current_price(양봉) > 20일 이평선(ma20) > 60일 이평선(ma60)
            # 정배열 ma20 > ma30 > ma60
            if target_price < current_price and ma20 > ma30 > ma60 and current_price > ma20 > ma60:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order(target_coin, krw*0.9995)
        else:
            # 장 마감 10초 전에 메도
            btc = get_balance("BTC")
            if btc > 0.00008:
                upbit.sell_market_order(target_coin, btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)