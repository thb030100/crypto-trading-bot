import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "ETHBUSD"
TRADE_QUANTITY = 0.01

closes = []
record = {}
in_position = False
position = 1

client = Client(config.API_KEY, config.API_SECRET, tld="us")


def order(symbol, quantity, side, order_type=ORDER_TYPE_MARKET):
    try:
        order = client.create_test_order(
            symbol=symbol, side=side, type=order_type, quantity=quantity
        )
        print(order)
        return True
    except Exception as e:
        return False


def on_message(ws, message):
    json_message = json.loads(message)
    candle = json_message["k"]
    is_candle_closed = candle["x"]
    close_price = candle["c"]

    if is_candle_closed:
        print("candle closed at {}".format(close_price))
        closes.append(float(close_price))

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.rsi(np_closes, RSI_PERIOD)
            print("all rsi caculated so far ")
            print(rsi)

            if rsi < RSI_OVERSOLD:
                if in_position:
                    print("do nothing since it is oversold")
                else:
                    print("buy")
                    order_successed = order(TRADE_SYMBOL, TRADE_QUANTITY, SIDE_BUY)
                    if order_successed:
                        in_position = True
                        record[str(position)]["price_buy"] = close_price
            if rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("sell")
                    order_successed = order(TRADE_SYMBOL, TRADE_QUANTITY, SIDE_SELL)
                    if order_successed:
                        in_position = False
                        record[str(position)]["price_sell"] = close_price
                        position += 1

                else:
                    print("do nothing since it is overbought")


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")


ws = websocket.WebSocketApp(
    SOCKET, on_close=on_close, on_open=on_open, on_message=on_message
)

ws.run_forever()
