"""Module for OandaDataProvider."""
import pandas as pd
from oandapyV20 import API
from oandapyV20.endpoints import instruments
from src.imatrade.adapter.data_provider import DataProvider


class OandaDataProvider(DataProvider):
    """Class for OandaDataProvider."""

    def __init__(self, api_key):
        self.api = API(access_token=api_key)

    def get_current_price(self, instrument):
        """Get current price from Oanda."""
        params = {"instruments": instrument}
        istrs = instruments.InstrumentsCandles(instrument=instrument, params=params)
        response = self.api.request(istrs)
        return float(response["candles"][0]["mid"]["c"])

    def get_historical_data(self, instrument, start, end, granularity="D"):
        """Get historical data from Oanda."""
        params = {
            "from": start,
            "to": end,
            "granularity": granularity,
            # "count": 5000,
        }

        istrs = instruments.InstrumentsCandles(instrument=instrument, params=params)
        response = self.api.request(istrs)
        data = []
        for candle in response["candles"]:
            data.append(
                [
                    candle["time"],
                    float(candle["mid"]["o"]),
                    float(candle["mid"]["h"]),
                    float(candle["mid"]["l"]),
                    float(candle["mid"]["c"]),
                ]
            )

        dataf = pd.DataFrame(data, columns=["time", "open", "high", "low", "close"])
        dataf["time"] = pd.to_datetime(dataf["time"])
        dataf["time"] = dataf["time"].dt.tz_localize(None)
        dataf.set_index("time", inplace=True)

        # Stocker le DataFrame dans un fichier Excel
        with pd.ExcelWriter(  # pylint: disable=abstract-class-instantiated
            f"data/{instrument}_{granularity}.xlsx"
        ) as writer:
            dataf.to_excel(writer, sheet_name="Sheet1")

        return dataf
