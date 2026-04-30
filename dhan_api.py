import requests
import os
from config import symbol_map

DHAN_API_KEY = os.environ.get("DHAN_API_KEY")
CLIENT_ID = os.environ.get("CLIENT_ID")

def place_order(symbol, action, qty):
    url = "https://api.dhan.co/orders"

    payload = {
        "securityId": symbol_map.get(symbol),
        "transactionType": action,
        "quantity": qty,
        "orderType": "MARKET",
        "productType": "INTRADAY"
    }

    headers = {
        "access-token": DHAN_API_KEY,
        "client-id": CLIENT_ID
    }

    return requests.post(url, json=payload, headers=headers).json()