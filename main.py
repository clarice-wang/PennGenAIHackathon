import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate

os.environ['OPENAI_API_KEY'] = apikey


template = """
    Below is a historical event you must tell a story about.

    Your goal is to:
    - Write a story about this historical event.
    - If a moment was specified, the story should focus on that particular moment.
    - This story should be factually correct.
    - Tell the story in language suited for the given audience.
    - Separate the story into five main segments, clearly marked by their segment number.

    For example:
    - The event is WWI, the specific moment is 'How It Started', and the target audience is 'Elementary (6-9 years old)'.
    - The story should be about what events led up to WWI, told in very simple sentencing using vocab words easily understood by an elementary school student.
    
    Below is the historical event, specific moment in the event, and target audience:
    EVENT: {event}
    MOMENT: {moment}
    AUDIENCE: {audience}

    YOUR RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=['event','char'],
    template=template,
)

def load_LLM():
    """logic for loading the chain you want to use should go here"""
    llm = OpenAI(temperature=0.9)
    return llm

llm = load_LLM()

##### PAGE LAYOUT BEGINS #####

st.set_page_config(page_title="Storybook AI", page_icon=":book:")
st.header("📖 Storybook AI")

event_text = st.text_area(label="", placeholder="Enter a historical event...", key="event_input")

col1, col2 = st.columns(2)

with col1:
    # st.markdown("## header")

    option_moment = st.selectbox(
        'Is there any specific moment the story should focus on?',
        ('How It Started', 'How It Ended', 'Random Moment', 'Other...')
    )
    # make optional if user response was alr specific

    if option_moment == "Other...": 
        option_moment = st.text_input("Enter your other option...")

with col2:
    option_audience = st.selectbox(
        'What age group is your audience in?',
        ('Kinder (3-6 years old)', 'Elementary (6-9 years old)', 'Middle (10+ years old)')
    )
    # st.markdown("**bold**")
    # st.image(image='andreasson2.jpeg', width=500, caption='https://saraandreasson.com/')
    
# char_text = st.text_area(label="", placeholder="Enter a main character...", key="char_input")

# def get_text():
#     input_text = st.text_area(label="", placeholder="Your Email...", key="email_input")
#     return input_text

if st.button('Generate!'):
    prompt_with_input = prompt.format(event=event_text, moment=option_moment, audience=option_audience)
    
    # story = llm(prompt_with_input)
    story = "temp story"

    col1, col2 = st.columns(2)

    with col1:
        st.write(story)

    with col2:
        st.write('images go here')