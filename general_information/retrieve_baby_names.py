import logging
import streamlit as st
from main import server_url
from utils import server_requests

gender = st.selectbox(
    label='Choose a gender',
    options=['Boy', 'Girl', 'Both'],
    index=None,
    help='The gender of which baby names will be chosen'
)

num_of_baby_names = st.number_input(
    label='Choose number of baby names to display',
    min_value=0,
    max_value=1000,
    value=1,
    step=1,
    help='The number of baby names to be displayed - 0 to display all baby names'
)

if gender:
    params = {
        'gender': gender,
        'num_of_baby_names': num_of_baby_names
    }

    try:
        baby_names = server_requests.get_request(f'{server_url}/baby-names/retrieve-baby-names/', params=params)
        columns = st.columns(5)

        for i, baby_name in enumerate(baby_names):
            with columns[i % 5]:
                st.write(baby_name)
    except Exception as e:
        logging.error(e)
        st.error(e)
        st.stop()
