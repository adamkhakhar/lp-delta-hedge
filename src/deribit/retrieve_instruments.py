import os
import sys
import requests

x = requests.get("https://test.deribit.com/api/v2/public/get_instruments?currency=BTC&expired=false&kind=option").json()

print(x)