import os
import streamlit as st
from dotenv import load_dotenv

# Load local .env when running the app on your computer
load_dotenv()

# First try the local .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# If running on Streamlit Cloud, get the key from Streamlit Secrets
if not GEMINI_API_KEY:
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please add it to your .env file locally "
        "or Streamlit Cloud Secrets."
    )

MODEL_NAME = "gemini-3.5-flash-lite"