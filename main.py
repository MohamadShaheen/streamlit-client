import os
import logging
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

server_url = os.getenv('SERVER_URL')
session = requests.Session()

if not os.path.exists('logs'):
    os.mkdir('logs')
logging.basicConfig(
    filename='logs/streamlit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='[%d-%m-%Y] (%H:%M:%S)',
    force=True
)

def main():
    st.set_page_config(layout='wide')

    pages = {
        'Welcome': [
            st.Page('basic_pages/welcome.py', title='Welcome', default=True)
        ]
    }

    pg = st.navigation(pages)
    pg.run()

if __name__ == '__main__':
    main()
