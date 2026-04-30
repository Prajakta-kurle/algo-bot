import websocket
import json
from strategy import check_exit

def on_message(ws, message):
    data = json.loads(message)

    symbol = data.get("symbol")
    price = data.get("last_price")

    if symbol and price:
        check_exit(symbol, price)

def on_open(ws):
    print("WebSocket Connected")

    ws.send(json.dumps({
        "action": "subscribe",
        "symbols": ["NSE:NIFTY", "NSE:BANKNIFTY"]
    }))

def start_ws():
    ws = websocket.WebSocketApp(
        "wss://api-feed.dhan.co",
        on_message=on_message,
        on_open=on_open
    )
    ws.run_forever()