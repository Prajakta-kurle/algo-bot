from flask import Flask, request
import threading
from strategy import create_trade
from websocket_client import start_ws
from config import MAX_TRADES

app = Flask(__name__)
trade_count = 0

@app.route('/')
def home():
    return "Algo Bot Running"

@app.route('/webhook', methods=['POST'])
def webhook():
    global trade_count

    data = request.json
    symbol = data.get("symbol")
    action = data.get("action")
    price = float(data.get("price"))

    if trade_count >= MAX_TRADES:
        return {"error": "Max trades reached"}

    create_trade(symbol, action, price)
    trade_count += 1

    return {"status": "trade placed"}

if __name__ == "__main__":
    threading.Thread(target=start_ws).start()

    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)