import string
import secrets
import logging
import streamlit as st

column_text = st.columns(1)[0]
column_button = st.columns(1)[0]

def generate_password(length, allow_numbers, allow_lowercase, allow_uppercase, allow_symbols, allow_extra_symbols):
    SYMBOLS = '!@#$%^&*()+'
    EXTRA_SYMBOLS = '~`[];?,'

    allowed_chars = ''

    if allow_numbers:
        allowed_chars += string.digits
    if allow_lowercase:
        allowed_chars += string.ascii_lowercase
    if allow_uppercase:
        allowed_chars += string.ascii_uppercase
    if allow_symbols:
        allowed_chars += SYMBOLS
    if allow_extra_symbols:
        allowed_chars += EXTRA_SYMBOLS

    if allowed_chars == '':
        e = 'Error: 400, Details: Unable to create password because no characters were allowed'
        logging.error(e)
        st.error(e)
        st.stop()

    password = ''.join(secrets.choice(allowed_chars) for _ in range(length))
    with column_text:
        st.text_input(label='Password', label_visibility='collapsed', value=password)

length = st.selectbox(
    label='Length',
    options=list(range(6, 257)),
    index=14
)

column1, column2 = st.columns(2)

with column1:
    allow_numbers = st.checkbox(
        label='Allow Numbers **0-9**',
        value=True
    )

    allow_lowercase = st.checkbox(
        label='Allow Lowercase **a-z**',
        value=True
    )

    allow_uppercase = st.checkbox(
        label='Allow Uppercase **A-Z**',
        value=True
    )

with column2:
    allow_symbols = st.checkbox(
        label='Allow Symbols **!@#$%^&*()+**',
        value=True
    )

    allow_extra_symbols = st.checkbox(
        label='Allow Extra Symbols **~`[];?,**',
        value=False
    )

with column_button:
    st.markdown(
        '''
        <style>
        .stButton {
            display: flex;
            justify-content: center;
        }
        </style>
        ''',
        unsafe_allow_html=True
    )

    generate_password_button = st.button(
        label='Generate Password',
        type='primary'
    )

if generate_password_button:
    generate_password(length, allow_numbers, allow_lowercase, allow_uppercase, allow_symbols,
                      allow_extra_symbols)
else:
    with column_text:
        st.text_input(label='Password', label_visibility='collapsed', value='')
