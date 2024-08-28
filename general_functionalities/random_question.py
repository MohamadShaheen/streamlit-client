import random
import logging
import diskcache
import streamlit as st
from utils import server_requests

server_url = 'http://localhost:8001'
cache = diskcache.Cache('cache')

def get_cached_questions():
    if 'questions' in cache:
        return cache['questions']
    else:
        try:
            questions = server_requests.get_request(f'{server_url}/questions/')
            cache.set('questions', questions, expire=3600)
            return questions
        except Exception as e:
            logging.error(e)
            st.error(e)
            st.stop()

if 'generated_question' not in st.session_state:
    st.session_state.generated_question = random.choice(get_cached_questions())

if 'answers' not in st.session_state:
    answers = st.session_state.generated_question['incorrect_answers'] + \
              [st.session_state.generated_question['correct_answer']]
    random.shuffle(answers)
    st.session_state.answers = answers

if 'disable_choices' not in st.session_state:
    st.session_state.disable_choices = False

generate_question_button = st.button(
    label='Generate Random Question',
    type='primary',
)

if generate_question_button:
    st.session_state.generated_question = random.choice(get_cached_questions())
    answers = st.session_state.generated_question['incorrect_answers'] + \
              [st.session_state.generated_question['correct_answer']]
    random.shuffle(answers)
    st.session_state.answers = answers
    st.session_state.disable_choices = False

st.markdown(f'''{st.session_state.generated_question['question']}  
**Category:** {st.session_state.generated_question['category']}  
**Difficulty:** {st.session_state.generated_question['difficulty']}
''')

user_answer = st.radio(
    label='None',
    options=st.session_state.answers,
    index=None,
    disabled=st.session_state.disable_choices,
    label_visibility='collapsed'
)

if user_answer and not st.session_state.disable_choices:
    if user_answer == st.session_state.generated_question['correct_answer']:
        st.write('Correct!')
    else:
        st.write('Incorrect!')
    st.session_state.disable_choices = True
