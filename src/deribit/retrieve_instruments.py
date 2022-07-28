import os
import sys
import requests

LP_DELTA_HEDGE_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)
sys.path.append(LP_DELTA_HEDGE_PATH + "/src")

from delta_hedge import Derivative


def retrieve_instruments(currency, expired=False):
    assert currency in ["ETH", "SOL", "BTC"]
    expired = "true" if expired else "false"
    instruments = requests.get(
        f"https://deribit.com/api/v2/public/get_instruments?currency={currency}&expired={expired}&kind=option"
    ).json()["result"]
    return instruments


def create_derivatives_for_instrument(instrument_data, ob_data):
    name = instrument_data["instrument_name"]
    assert name.endswith("C") or name.endswith("P")
    strike = instrument_data["strike"]
    best_bid = ob_data["best_bid_price"]
    best_ask = ob_data["best_ask_price"]
    info = {"instrument_data": instrument_data, "ob_data": ob_data}
    long_payoff_fun = None
    short_payoff_fun = None
    # call
    if name.endswith("C"):
        # long
        long_payoff_fun = lambda x: max(0, x - strike) - best_ask
        # short
        short_payoff_fun = lambda x: best_bid - max(0, x - strike)
    else:  # put
        # long
        long_payoff_fun = lambda x: max(0, strike - x) - best_ask
        # short
        short_payoff_fun = lambda x: best_bid - max(0, strike - x)
    long_deriv = Derivative(name + "_LONG", long_payoff_fun, info)
    short_deriv = Derivative(name + "_SHORT", short_payoff_fun, info)
    return long_deriv, short_deriv


def create_derivatives_from_instrument_data(data):
    assert type(data) == list
    derivatives = []
    for instrument in data:
        ob_data = requests.get(
            f"https://deribit.com/api/v2/public/get_order_book_by_instrument_id?instrument_id={instrument['instrument_id']}&depth=1"
        ).json()["result"]
        # skip instruments with no volume
        if len(ob_data["bids"]) == 0 or len(ob_data["asks"]) == 0:
            continue
        long_deriv, short_deriv = create_derivatives_for_instrument(instrument, ob_data)
        derivatives.append(long_deriv)
        derivatives.append(short_deriv)
    return derivatives


def retrieve_and_create_derivatives(currency, expired=False):
    instrumets = retrieve_instruments(currency, expired=expired)
    return create_derivatives_from_instrument_data(instrumets)
