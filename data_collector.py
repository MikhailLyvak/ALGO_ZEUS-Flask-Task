import os
import requests
import csv
from dataclasses import dataclass
import json
from datetime import datetime, timedelta
import time

DATA_FOLDER = "crypto_data"

def get_symbol_data(coin: str, interval: int = "1h") -> None:
    if interval == "1h":
        start_date = (datetime.now() - timedelta(days=3)).strftime("%Y.%m.%d")
        end_date = datetime.now().strftime("%Y.%m.%d")
    if interval == "4h":
        start_date = (datetime.now() - timedelta(days=14)).strftime("%Y.%m.%d")
        end_date = datetime.now().strftime("%Y.%m.%d")
    if interval == "1d":
        start_date = (datetime.now() - timedelta(days=50)).strftime("%Y.%m.%d")
        end_date = datetime.now().strftime("%Y.%m.%d")
    symbol = f"{coin}USDT"

    start = start_date.split(".")
    s_year, s_month, s_day = start[0], start[1], start[2]

    end = end_date.split(".")
    e_year, e_month, e_day = end[0], end[1], end[2]
    URL = "https://api.binance.com/api/v3/klines"

    startTime = str(
        int(datetime(int(s_year), int(s_month), int(s_day)).timestamp() * 1000)
    )
    endTime = str(
        int(datetime(int(e_year), int(e_month), int(e_day)).timestamp() * 1000)
    )
    limit = 1000

    request_params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": startTime,
        "endTime": endTime,
        "limit": limit,
    }

    response = json.loads(requests.get(URL, params=request_params).text)

    @dataclass
    class Coin:
        name: str
        interval: str
        time: str
        open_price: float
        close_price: float
        high_price: float
        low_price: float
        volume: float

    result_date = []

    for coin in response:
        result_date.append(
            Coin(
                name=symbol,
                interval=interval,
                time=datetime.fromtimestamp((coin[0] / 1000)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                open_price=float(coin[1]),
                close_price=float(coin[4]),
                high_price=float(coin[2]),
                low_price=float(coin[3]),
                volume=float(coin[5]),
            )
        )

    output_file = os.path.join(DATA_FOLDER, f"{interval}-{symbol}.csv")

    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Symbol",
                "Interval",
                "Time",
                "Open Price",
                "Close Price",
                "High Price",
                "Low Price",
                "Volume",
            ]
        )

        for item in result_date:
            writer.writerow(
                [
                    item.name,
                    item.interval,
                    item.time,
                    item.open_price,
                    item.close_price,
                    item.high_price,
                    item.low_price,
                    item.volume,
                ]
            )

    print(f"Data saved to {output_file}.")


def start_data_collection():
    while True:
        get_symbol_data("BTC", "1h")
        get_symbol_data("ETH", "1h")
        get_symbol_data("XRP", "1h")
        get_symbol_data("LTC", "1h")
        get_symbol_data("ADA", "1h")
        get_symbol_data("BTC", "4h")
        get_symbol_data("ETH", "4h")
        get_symbol_data("XRP", "4h")
        get_symbol_data("LTC", "4h")
        get_symbol_data("ADA", "4h")
        get_symbol_data("BTC", "1d")
        get_symbol_data("ETH", "1d")
        get_symbol_data("XRP", "1d")
        get_symbol_data("LTC", "1d")
        get_symbol_data("ADA", "1d")
        time.sleep(60)

