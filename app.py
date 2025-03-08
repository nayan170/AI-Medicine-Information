from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import base64

# Load environment variables
load_dotenv()

# Configure the API key for Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini 1.5 Flash API and get response
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

# Function to prepare the image data for the model
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Function to set background image using a local file
def set_bg_hack_local(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("data:image/png;base64,{b64_encoded}");
             background-size: cover;
         }}
         /* Set all text color to black */
         .stApp, .stMarkdown, .stTextInput, .stButton, .stHeader, .stSubheader, .stWrite {{
             color: black !important;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# Define the input prompt
input_prompt = """
You are an expert pharmaceutical chemist. Your task is to analyze the image provided, identify the tablets shown, and provide detailed information about each one. Follow the steps below:

1. Examine the image carefully and identify all tablets depicted.
2. Describe the uses and functionalities of each tablet shown in the image.
3. Provide information on the intended purposes, features, and typical applications of the tablets.
4. If possible, include any notable specifications or distinguishing characteristics of each tablet.
5. Ensure clarity and conciseness in your descriptions, focusing on key details and distinguishing factors.
"""

# Initialize the Streamlit app
st.set_page_config(page_title="AI Medicine Information")

# Set the background image (assuming the image is named "background.jpg" and is in the same directory)
# set_bg_hack_local("background.jpg")

st.header("🧪 AI Medicine Information")

# Text input for additional instructions
input_text = st.text_input("Input Prompt: ", key="input")

# File uploader for the image
uploaded_file = st.file_uploader("Uploaded image...", type=["jpg", "jpeg", "png"])

# Display the uploaded image
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Uploaded Image", use_column_width=True)

# Button to trigger the analysis
submit = st.button("🩺 Analyze")

# If the submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_text, image_data, input_prompt)
    st.subheader("🔬 The Analysis Report")
    st.write(response)
