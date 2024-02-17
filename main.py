import os
from apikey import apikey, baseten_api_key

import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.utilities import WikipediaAPIWrapper

import requests
import base64
from PIL import Image
from io import BytesIO

# Replace the empty string with your model id below
model_id = "4w7pnv1w"
baseten_api_key = os.environ["BASETEN_API_KEY"]
BASE64_PREAMBLE = "data:image/png;base64,"

# Function used to convert a base64 string to a PIL image
def b64_to_pil(b64_str):
    return Image.open(BytesIO(base64.b64decode(b64_str.replace(BASE64_PREAMBLE, ""))))

def generate_image(prompt, negative_prompt, steps=30):
    # Make sure you have set the model_id and baseten_api_key before calling this function
    data = {
      "prompt": prompt,
      "negative_prompt": negative_prompt,
      "steps": steps
    }

    # Call model endpoint
    res = requests.post(
        f"https://model-{model_id}.api.baseten.co/production/predict",
        headers={"Authorization": f"Api-Key {baseten_api_key}"},
        json=data
    )

    # Check if the request was successful
    if res.status_code != 200:
        raise Exception(f"Request failed with status code: {res.status_code}")

    # Get output image
    output = res.json().get("output")
    if output is None:
        raise Exception("No output from the model")

    # Convert the base64 model output to an image
    img = b64_to_pil(output)
    img.save("output_image.png")
    return img

def cut_off_end(text):
    last_period_index = text.rfind('.')
    
    if last_period_index != -1:
        return text[:last_period_index+1]
    else:
        return text
    
##############################

os.environ['OPENAI_API_KEY'] = apikey

##### DEFINING PROMPTS #####

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

    [Begin the story with an introduction to the event.]\n
    [Continue with the build-up to the specified moment.]\n
    [Detail the key moment, focusing on pivotal actions or decisions.]\n
    [Describe the immediate consequences of the moment.]\n
    [Conclude with the broader impact or resolution of the event.]

    Please use simple language suitable for the age group (audience) and keep the information accurate according to the wikipedia research provided.
"""

image_prompt_template = """
    Create an image prompt that encapsulates the following story:

    Story:
    {story_text}

    What visual elements would best illustrate this narrative to be shown in a children's book?
    """

prompt = PromptTemplate(
    input_variables=['event','moment','audience','wikipedia'],
    template=template,
)

def generate_image_prompt(story_text, image_prompt_template):
    image_prompt_text = image_prompt_template.format(story_text=story_text)
    image_prompt = image_prompt_llm(image_prompt_text)
    return image_prompt

##### LOADING LLMS #####

def load_LLM():
    """logic for loading the chain you want to use should go here"""
    llm = OpenAI(temperature=0.9)
    return llm

llm = load_LLM()

def load_image_prompt_LLM():
    # You can use the same OpenAI LLM or a different configuration if needed
    image_prompt_llm = OpenAI(temperature=0.7)  # Adjust temperature as needed for image prompts
    return image_prompt_llm

image_prompt_llm = load_image_prompt_LLM()

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

story_segments = []
if st.button('Generate!'):
    wiki = WikipediaAPIWrapper()
    wiki_research = wiki.run(event_text)
    prompt_with_input = prompt.format(event=event_text, moment=option_moment, audience=option_audience, wikipedia=wiki_research)
    
    story = llm(prompt_with_input)
    story = cut_off_end(story)
    # st.write(story)

    story_segments = story.split("\n\n")  # text split, adjust as needed
    image_segments = []

    for seg in story_segments:
        image_prompt = generate_image_prompt(seg, image_prompt_template)
        image_segments.append(generate_image(image_prompt, "cartoon, for-children"))

    if 'story_segments' not in st.session_state:
        st.session_state.story_segments = []
    if 'image_segments' not in st.session_state:
        st.session_state.image_segments = []
    if 'current_segment' not in st.session_state:
        st.session_state.current_segment = 0

    st.session_state.story_segments = story_segments
    st.session_state.image_segments = image_segments

# display the current segment and controls
if 'story_segments' in st.session_state and len(st.session_state.story_segments) > 0:
    current_story_segment = st.session_state.story_segments[st.session_state.current_segment]
    current_image_segment = st.session_state.image_segments[st.session_state.current_segment]

    col1, col2 = st.columns(2)
    with col1:
        st.write(current_story_segment)

    with col2:
        st.image(current_image_segment)

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

    # if (st.session_state.current_segment == len(st.session_state.story_segments)):
    #     pdf_file_name = f"{event_text}.pdf"
    #     st.write(pdf_file_name)
    #     pdf_data = create_pdf(story_segments, image_segments)

    #     st.download_button(
    #         label="Download Story as PDF",
    #         data=pdf_data,
    #         file_name=pdf_file_name,
    #         mime="application/pdf"
    #     )