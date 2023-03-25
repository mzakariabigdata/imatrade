# src/imatrade/data_providers/oanda_data.py

import pandas as pd
import os
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
from imatrade.adapter.data_provider import DataProvider


class OandaDataProvider(DataProvider):
    def __init__(self, api_key):
        self.api = API(access_token=api_key)


    def get_historical_data(self, instrument, start, end, granularity='D'):
        params = {
            "from": start,
            "to": end,
            "granularity": granularity,
            # "count": 5000,
        }

        r = instruments.InstrumentsCandles(instrument=instrument, params=params)
        response = self.api.request(r)
        data = []
        for candle in response["candles"]:
            data.append([
                candle["time"],
                float(candle["mid"]["o"]),
                float(candle["mid"]["h"]),
                float(candle["mid"]["l"]),
                float(candle["mid"]["c"]),
            ])

        df = pd.DataFrame(data, columns=["time", "open", "high", "low", "close"])
        df["time"] = pd.to_datetime(df["time"])
        df["time"] = df["time"].dt.tz_localize(None)
        df.set_index("time", inplace=True)

        # Stocker le DataFrame dans un fichier Excel
        with pd.ExcelWriter(f'data/{instrument}_{granularity}.xlsx') as writer:
            df.to_excel(writer, sheet_name='Sheet1')

        return df