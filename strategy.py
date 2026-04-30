import config
from dhan_api import place_order

active_trades = {}

def calculate_qty(entry, sl):
    risk_amount = config.current_capital * (config.RISK_PERCENT / 100)
    sl_distance = abs(entry - sl)
    return max(int(risk_amount / sl_distance), 1)

def create_trade(symbol, action, price):
    if action == "BUY":
        sl = price - config.SL_POINTS
        tp = price + config.SL_POINTS * config.RR_RATIO
    else:
        sl = price + config.SL_POINTS
        tp = price - config.SL_POINTS * config.RR_RATIO

    qty = calculate_qty(price, sl)

    active_trades[symbol] = {
        "entry": price,
        "sl": sl,
        "tp": tp,
        "action": action,
        "qty": qty
    }

    place_order(symbol, action, qty)
    print(f"ENTRY {symbol} {action} | Qty:{qty}")

def update_capital(trade, exit_price):
    entry = trade["entry"]
    qty = trade["qty"]
    action = trade["action"]

    pnl = (exit_price - entry) * qty if action == "BUY" else (entry - exit_price) * qty
    config.current_capital += pnl

    print(f"PnL: {pnl} | Capital: {config.current_capital}")

def check_exit(symbol, price):
    if symbol not in active_trades:
        return

    t = active_trades[symbol]
    entry, sl, tp, action = t["entry"], t["sl"], t["tp"], t["action"]

    # BUY
    if action == "BUY":
        if price <= sl:
            close_trade(symbol, price, "SL HIT")
        elif price >= tp:
            close_trade(symbol, price, "TP HIT")
        elif price > entry + config.SL_POINTS:
            t["sl"] = entry  # breakeven

    # SELL
    else:
        if price >= sl:
            close_trade(symbol, price, "SL HIT")
        elif price <= tp:
            close_trade(symbol, price, "TP HIT")
        elif price < entry - config.SL_POINTS:
            t["sl"] = entry

def close_trade(symbol, price, reason):
    trade = active_trades[symbol]
    exit_side = "SELL" if trade["action"] == "BUY" else "BUY"

    update_capital(trade, price)
    place_order(symbol, exit_side, trade["qty"])

    print(f"CLOSE {symbol} | {reason}")
    del active_trades[symbol]