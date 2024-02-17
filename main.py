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
    Craft a narrative centered around a specific historical event, paying close attention to a particular moment if highlighted. Your story should adhere to the following criteria:
    - **Accuracy**: Base your story on factual information, primarily from the provided Wikipedia research.
    - **Audience Engagement**: Tailor the language and storytelling style to the specified audience's understanding and interests.
    - **Structure**: Organize your narrative into five distinct segments, each labeled with its corresponding segment number. Segments should comprise one to two sentences, ensuring clarity and conciseness.

    ### Guidelines:
    1. **Event and Moment**: Focus on the given event, especially the outlined moment, to anchor your story.
    2. **Language**: Use vocabulary and sentence structures appropriate for the audience age group. Aim for simplicity and clarity, avoiding complex jargon or concepts.
    3. **Segments**: Clearly delineate each part of your story using newlines, ensuring a smooth and logical flow from one segment to the next.

    ### Example:
    - **Event**: World War I
    - **Moment**: How It Started
    - **Audience**: Elementary (6-9 years old)
    - **Approach**: Narrate the causes leading to World War I in a manner easily graspable by young children, using straightforward language and breaking down complex ideas into digestible pieces.

    ### Template:
    Below are the details for your story creation:
    - **EVENT**: {event}
    - **MOMENT**: {moment}
    - **AUDIENCE**: {audience}
    - **WIKIPEDIA**: {wikipedia}

    ### Your Response:
    (Your crafted story goes here, following the structured guidelines provided above.)
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
    wiki = WikipediaAPIWrapper()
    wiki_research = wiki.run(event_text)
    prompt_with_input = prompt.format(event=event_text, moment=option_moment, audience=option_audience, wikipedia=wiki_research)
    
    # story = llm(prompt_with_input)
    story_segments = llm(prompt_with_input).split("\n\n")  # Example split, adjust as needed
    st.session_state.story_segments = story_segments
    st.session_state.current_segment = 0  # Initialize or reset the current segment
    # story = "temp story"

# display the current segment and controls
if 'story_segments' in st.session_state and len(st.session_state.story_segments) > 0:
    col1, col2 = st.columns(2)
    with col1:
        st.write(st.session_state.story_segments[st.session_state.current_segment])

    with col2:
        st.write('images go here')  # Placeholder for future image integration

    # progress bar
    progress = (st.session_state.current_segment + 1) / len(st.session_state.story_segments)
    st.progress(progress)

    # navigation buttons
    prev, _ ,next = st.columns([4, 4, 2])  # Adjust spacing as needed
    if next.button('Next Page'):
        if st.session_state.current_segment < len(st.session_state.story_segments) - 1:
            st.session_state.current_segment += 1

    if prev.button('Prev Page'):
        if st.session_state.current_segment > 0:
            st.session_state.current_segment -= 1