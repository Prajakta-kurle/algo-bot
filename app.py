from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Algo Bot Running"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    return {"status": "ok"}