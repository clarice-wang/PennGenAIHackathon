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

# hysterical version
# template = """
#     Below is a historical event you must tell a story about.

#     Your goal is to:
#     - Write a story about this historical event.
#     - If a moment was specified, the story should focus on that particular moment.
#     - This story should be narrated by the given character.
#     - This story should be factually correct.
#     - Use a storyteller tone as if you were writing a children's book.
#     - Separate the story into five main segments, clearly marked by their segment number.

#     For example:
#     - The event is WWI, the main character is Scooby-Doo, and the specific moment is 'How It Started'
#     - The story should be about what events led up to WWI.
#     - The story should be told in the voice of Scooby-Doo, including his catchphrase "ruh-roh" after unfortunate events.
    
#     Below is the historical event, main character, and specific moment in the event:
#     EVENT: {event}
#     CHARACTER: {char}
#     MOMENT: {moment}

#     YOUR RESPONSE:
# """

prompt = PromptTemplate(
    input_variables=['event','char'],
    template=template,
)

def load_LLM():
    """logic for loading the chain you want to use should go here"""
    llm = OpenAI(temperature=0.9)
    return llm

llm = load_LLM()

st.set_page_config(page_title="Storybook AI", page_icon=":book:")
st.header("Storybook AI")

col1, col2 = st.columns(2)

with col1:
    st.markdown("## header")
    st.write("col1")
    option_audience = st.selectbox(
        'What age group is your audience in?',
        ('Kinder (3-6 years old)', 'Elementary (6-9 years old)', 'Middle (10+ years old)')
    )

    option_moment = st.selectbox(
        'What part of this event would you like the story to focus on?',
        ('How It Started', 'How It Ended', 'Random Moment')
    )
    # make optional if user response was alr specific

with col2:
    st.write("col2")
    st.markdown("**bold**")
    st.image(image='andreasson2.jpeg', width=500, caption='https://saraandreasson.com/')


# st.write(1+2)
    
event_text = st.text_area(label="", placeholder="Enter a historical event...", key="event_input")
# char_text = st.text_area(label="", placeholder="Enter a main character...", key="char_input")

# def get_text():
#     input_text = st.text_area(label="", placeholder="Your Email...", key="email_input")
#     return input_text

if event_text:
    # st.write("Let's learn more about ", event_text, "!")

    # prompt_with_event = prompt.format(event=event_text, char=char_text, moment=option_moment)
    prompt_with_event = prompt.format(event=event_text, moment=option_moment, audience=option_audience)
    
    story = llm(prompt_with_event)

    st.write(story)

# if char_text:
    # st.write("Featuring ", char_text, ":)")

# if __name__ == '__main__':
#     import openai
#     client = openai.OpenAI()
#     completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Hello!"}
#     ]
#     )

#     print(completion.choices[0].message)