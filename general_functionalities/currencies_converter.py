import time
import logging
import diskcache
import streamlit as st
from main import server_url
from utils import server_requests

cache = diskcache.Cache('cache')

def get_cached_currencies():
    if 'currencies' in cache:
        return cache['currencies']
    else:
        currencies = server_requests.get_request(f'{server_url}/currencies/retrieve-all-currencies/')
        currencies = [f'{currency['code']} - {currency['name']}' for currency in currencies]
        cache.set('currencies', currencies, expire=3600)
        return currencies

currencies = get_cached_currencies()

from_currency = st.selectbox(
    label='From',
    options=currencies,
    index=None,
    help='Choose currency to convert from'
)

to_currency = st.selectbox(
    label='To',
    options=currencies,
    index=None,
    help='Choose currency to convert to'
)

amount = st.number_input(
    label='Choose amount',
    min_value=1.0,
    value=1.0,
    step=1.0,
)

if from_currency and to_currency and amount:
    params = {
        'from_currency': from_currency.split()[0],
        'to_currency': to_currency.split()[0],
        'amount': amount
    }

    try:
        conversion_result = server_requests.get_request(f'{server_url}/currencies/convert-currencies/', params=params)
        # st.write('Conversion result:', conversion_result)
        output = f'Conversion result: {conversion_result}'

        def stream_data():
            for char in output:
                yield char
                time.sleep(0.02)

        st.write_stream(stream_data())
    except Exception as e:
        logging.error(e)
        st.error(e)
        st.stop()
