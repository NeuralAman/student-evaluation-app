import streamlit as st

def load_custom_css(css_file_path):
    with open(css_file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
