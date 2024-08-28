import logging
import diskcache
import streamlit as st
from main import server_url
from utils import server_requests

cache = diskcache.Cache('cache')

def get_cached_baby_names(gender: str):
    if f'baby_names_{gender}' in cache:
        return cache[f'baby_names_{gender}']
    else:
        try:
            baby_names = server_requests.get_request(f'{server_url}/baby-names/retrieve-baby-names/', params={'gender': gender})
            cache.set(f'baby_names_{gender}', baby_names, expire=3600)
            return baby_names
        except Exception as e:
            logging.error(e)
            st.error(e)
            st.stop()

if 'gender' not in st.session_state:
    st.session_state.gender = None

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
    if gender != st.session_state.gender:
        num_of_baby_names = 1
        st.session_state.gender = gender

    if num_of_baby_names == 0:
        baby_names = get_cached_baby_names(gender=gender)
    else:
        baby_names = get_cached_baby_names(gender=gender)[:num_of_baby_names]

    columns = st.columns(5)

    for i, baby_name in enumerate(baby_names):
        with columns[i % 5]:
            st.write(baby_name)
