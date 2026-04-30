from flask import Flask, request
from strategy import create_trade
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