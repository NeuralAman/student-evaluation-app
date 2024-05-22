import asyncio
import re
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

from utils.file_handler import handle_file_upload
from utils.openai_api import evaluate_document_stream
from utils.evaluation import static_essay_assessment_criteria, evaluate_essay, evaluate_other, get_rubric_metrics
from utils.ui_helpers import load_custom_css

load_dotenv()

# Initialize session state
if 'evaluation_running' not in st.session_state:
    st.session_state.evaluation_running = False
if 'stop_signal' not in st.session_state:
    st.session_state.stop_signal = False
if 'response_text' not in st.session_state:
    st.session_state.response_text = ""
if 'uploaded_file_name' not in st.session_state:
    st.session_state.uploaded_file_name = ""
if 'score' not in st.session_state:
    st.session_state.score = 0


def main():
    st.title("Student Evaluation App")
    load_custom_css('assets/styles.css')

    st.header("Choose Subject")
    subject = st.selectbox("Select the subject of the document:",
                           ["Essay-Writing", "Maths", "Chemistry", "Physics", "English"])

    st.header("Upload your document")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "jpg", "png"])

    if uploaded_file is not None:
        if uploaded_file.name != st.session_state.uploaded_file_name:
            st.session_state.uploaded_file_name = uploaded_file.name
            st.session_state.response_text = ""  # Reset response text for new file
            st.session_state.evaluation_running = False
            st.session_state.stop_signal = False
            st.session_state.score = 0  # Reset score
            st.rerun()

        file_content = handle_file_upload(uploaded_file)

        st.header("Evaluation Criteria")
        if subject == "Essay-Writing":
            st.write(get_rubric_metrics(subject.lower()))
            # st.write(static_essay_assessment_criteria())

        st.header("Evaluation Results")
        evaluation_container = st.empty()

        if st.session_state.evaluation_running:
            if st.button("Stop Evaluation"):
                st.session_state.stop_signal = True

        else:
            if st.button("Start Evaluation"):
                st.session_state.evaluation_running = True
                st.session_state.stop_signal = False
                st.session_state.response_text = ""  # Reset response text
                st.session_state.score = 0  # Reset score
                st.rerun()

        if st.session_state.evaluation_running:
            with st.spinner('Evaluating...'):
                asyncio.run(display_streaming_response(subject, file_content, evaluation_container))

        # Display the final response text after evaluation completes
        if st.session_state.response_text:
            st.write(st.session_state.response_text)
            # if st.session_state.score > 90:
            #     display_congratulations_image()

            if st.button("Re-run Evaluation"):
                st.session_state.evaluation_running = False
                st.session_state.stop_signal = False
                st.session_state.response_text = ""
                st.session_state.score = 0  # Reset score
                st.rerun()


def extract_score(response_text):
    """Extract the overall score from the response text."""
    score_pattern = r'Final Rating: (\d+(\.\d+)?)/5'
    match = re.search(score_pattern, response_text, re.IGNORECASE)
    print(match.group(1))
    if match:
        return float(match.group(1)) * 20  # Convert to percentage
    return 0


async def display_streaming_response(subject, file_content, container):
    async for chunk in await evaluate_document_stream(subject, file_content):
        if st.session_state.stop_signal:
            break
        if chunk:
            st.session_state.response_text += chunk
            container.write(st.session_state.response_text)
    st.session_state.score = extract_score(st.session_state.response_text)
    st.session_state.evaluation_running = False
    st.session_state.stop_signal = False
    st.rerun()


def display_congratulations_image():
    """Display an image if the score is above 90%."""
    img = Image.open('assets/media/congratulation_image.png')
    st.image(img, caption='Congratulations! Excellent Score!')


if __name__ == "__main__":
    main()
