import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.utilities import WikipediaAPIWrapper

os.environ['OPENAI_API_KEY'] = apikey


template = """
    ## Historical Storytelling Prompt

    ### Objective:
    Craft a narrative about a historical event, focusing on a specified moment. Your story must be accurate and tailored for the intended audience. It should be structured into exactly five segments, with each segment being a single sentence for brevity and clarity.

    ### Instructions:
    - **EVENT**: {event}
    - **MOMENT**: {moment}
    - **AUDIENCE**: {audience}
    - **WIKIPEDIA**: {wikipedia}

    ### Story Structure:
    - Begin the story by introducing the event.
    - Progress to the specified moment.
    - Include pivotal details that are age-appropriate.
    - Conclude with the impact or resolution of the moment.

    ### Your Response:
    Create a story with exactly five segments. Ensure there is a newline between each segment. Each segment should be one sentence long.

    [Begin the story with an introduction to the event.]
    NEW LINE
    [Continue with the build-up to the specified moment.]
    NEW LINE
    [Detail the key moment, focusing on pivotal actions or decisions.]
    NEW LINE
    [Describe the immediate consequences of the moment.]
    NEW LINE
    [Conclude with the broader impact or resolution of the event.]

    Please use simple language suitable for the age group (audience) and keep the information accurate according to the wikipedia research provided.
"""

prompt = PromptTemplate(
    input_variables=['event','moment','audience','wikipedia'],
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
    option_moment = st.selectbox(
        'Is there any specific moment the story should focus on?',
        ('How It Started', 'The Whole Story', 'Random Moment', 'Other...')
    )

    if option_moment == "Other...": 
        option_moment = st.text_input("Enter your other option...")

with col2:
    option_audience = st.selectbox(
        'What age group is your audience in?',
        ('Kinder (3-6 years old)', 'Elementary (6-9 years old)', 'Middle (10+ years old)')
    )

if st.button('Generate!'):
    wiki = WikipediaAPIWrapper()
    wiki_research = wiki.run(event_text)
    prompt_with_input = prompt.format(event=event_text, moment=option_moment, audience=option_audience, wikipedia=wiki_research)
    
    story = llm(prompt_with_input)
    story_segments = story.split("NEW LINE")  # text split, adjust as needed
    st.session_state.story_segments = story_segments
    st.session_state.current_segment = 0  # initialize or reset the current segment

# display the current segment and controls
if 'story_segments' in st.session_state and len(st.session_state.story_segments) > 0:
    col1, col2 = st.columns(2)
    with col1:
        st.write(st.session_state.story_segments[st.session_state.current_segment])

    with col2:
        st.write('images go here')  # placeholder for future image integration

    # progress bar
    progress = (st.session_state.current_segment + 1) / len(st.session_state.story_segments)
    st.progress(progress)

    # navigation buttons
    prev, _ ,next = st.columns([4, 4, 2])  # adjust spacing as needed
    if next.button('Next Page'):
        if st.session_state.current_segment < len(st.session_state.story_segments) - 1:
            st.session_state.current_segment += 1

    if prev.button('Prev Page'):
        if st.session_state.current_segment > 0:
            st.session_state.current_segment -= 1


# foreground and background specification