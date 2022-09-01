from calalyst.utils.run_algo import run_algorithm
import pandas as pd


def initialize(context):
    context.bittrex = context.exchanges["bitfinex"]
    context.poloniex = context.exchanges["poloniex"]


run_algorithm(
    initialize=initialize,
    handle_data=handle_data,
    analyze=analyze,
    capital_base=100,
    live=False,
    base_currency="btc",
    exchange_name="bitfinex, poloniex",
    data_frequency="minute",
    start=pd.to_datetime(),
)
