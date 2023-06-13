import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import plotly.graph_objects as go
import os
import threading
from data_collector import start_data_collection


DATA_FOLDER = "crypto_data"
app = Flask(__name__)

coins = ["BTC", "ETH", "XRP", "LTC", "ADA"]
intervals = ["1h", "4h", "1d"]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        coin = request.form.get("coin")
        interval = request.form.get("interval")
        return redirect(url_for("coin_details", coin=coin, interval=interval))
    else:
        coin = "BTC"
        interval = "1h"
        return redirect(url_for("coin_details", coin=coin, interval=interval))


@app.route("/coin/<coin>/<interval>")
def coin_details(coin, interval):
    filename = os.path.join(DATA_FOLDER, f"{interval}-{coin}USDT.csv")
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        return redirect(url_for("index"))

    num_candles = 50

    df = df.tail(num_candles)

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df["Time"],
                open=df["Open Price"],
                high=df["High Price"],
                low=df["Low Price"],
                close=df["Close Price"],
            )
        ]
    )

    chart_html = fig.to_html(full_html=False, include_plotlyjs="cdn")

    return render_template(
        "index.html",
        coins=coins,
        intervals=intervals,
        coin=coin,
        interval=interval,
        chart_html=chart_html,
    )


if __name__ == "__main__":
    data_collection_thread = threading.Thread(target=start_data_collection)
    data_collection_thread.start()

    app.run(debug=True)
