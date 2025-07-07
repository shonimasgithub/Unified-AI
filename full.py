import streamlit as st
from PIL import Image
import os
import io
from dotenv import load_dotenv
import google.generativeai as genai
from io import BytesIO
import requests

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="Unified AI", layout="wide")

# Unified header
st.title("Unified AI")

# Define the tabs
tabs = st.tabs(["Text Query", "Image Processing", "Image Generation", "Resume Upgradation", "YouTube Video Summarization"])

# Tab 1: Text Query
def text_query_tab():
    with tabs[0]:
        st.header("Text Query")
        
        def get_gemini_response(query):
            model = genai.GenerativeModel("gemini-pro")  # For question and query systems
            response = model.generate_content(query, stream=True)  # Using 'generate_content' instead of 'start_chat'
            return response

        input_query = st.text_input("Input: ", key="input")
        submit = st.button("Ask Question")
        
        if submit and input_query:
            response = get_gemini_response(input_query)  # Get Response from API
            st.subheader("The response is:")
            for chunk in response:
                st.write(chunk.text)

# Tab 2: Image Processing
def image_processing_tab():
    with tabs[1]:
        api_key = "AIzaSyBx1PnYJld4cifrCC3IOtY43HIYIj0Mkk8"
        genai.configure(api_key=api_key)
        st.header("Image Processing")
        
        def get_gemini_response(input_text, image, prompt):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash') 
                response = model.generate_content([input_text, image[0], prompt])
                return response.text
            except Exception as e:
                return f"Error: {str(e)}"

        def input_image_setup(uploaded_file):
            if uploaded_file is not None:
                bytes_data = uploaded_file.getvalue()
                image_parts = [
                    {"mime_type": uploaded_file.type, "data": bytes_data}
                ]
                return image_parts
            else:
                raise FileNotFoundError("No file uploaded")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Upload and Analyze")
            st.markdown("---")  # Horizontal line for separation
            input_text = st.text_input("Input Prompt: ", key="prompt")
            if not input_text:
                input_text = "explain"
            submit = st.button("Analyze Image")
            uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
            print(uploaded_file)
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image.", use_column_width=True)

        with col2:
            st.subheader("Analysis Result")
            st.markdown("---")  # Horizontal line for separation
            if submit:
                if uploaded_file is not None:
                    try:
                        print("\n\n\n")
                        print(uploaded_file)
                        print("\n\n\n")
                        image_data = input_image_setup(uploaded_file)
                        input_prompt = "You are an expert in understanding images. You will receive input images and you will have to answer questions based on the input image."
                        with st.spinner("Analyzing the image..."):
                            response = get_gemini_response(input_text, image_data, input_prompt)
                            st.write(response)
                    except FileNotFoundError as e:
                        st.error(f"Error: {str(e)}")
                    except Exception as e:
                        st.error(f"Unexpected error: {str(e)}")
                else:
                    st.error("Please upload an image to analyze.")

# Tab 3: Image Generation
def image_generation_tab():
    with tabs[2]:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.header("Image Generation")
            prompt = st.text_area("Enter a prompt for image generation:")
            generate = st.button("Generate Image")

            token = "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"
            
            # Button to generate the image
            if generate:
                if not prompt.strip():
                    st.error("Please enter a prompt!")
                else:
                    # st.info("Generating image, please wait...")
                    st.spinner("Generating image, please wait...")

                    # API request
                    try:
                        headers = {
                            "Authorization": f"Bearer {token}",
                            "Content-Type": "application/json",
                        }
                        data = {"inputs": prompt}
                        response = requests.post(
                            "https://api-inference.huggingface.co/models/kothariyashhh/GenAi-Texttoimage",
                            headers=headers,
                            json=data,
                        )

                        # Check for errors
                        if response.status_code != 200:
                            st.error(f"Error: {response.status_code}, {response.text}")
                        else:
                            # Display the image
                            img = Image.open(BytesIO(response.content))
                            st.image(img, caption="Generated Image", use_column_width=True)

                    except Exception as e:
                        st.error(f"An error occurred: {e}")


# Tab 4: Resume Upgradation
def resume_upgradation_tab():
    with tabs[3]:
        st.header("Resume Upgradation")
        uploaded_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx"])

        if uploaded_file:
            st.write("Uploaded Resume:", uploaded_file.name)
            upgrade = st.button("Upgrade Resume")
            if upgrade:
                # Placeholder for resume upgradation logic
                st.write("Upgraded resume details here.")

# Tab 5: YouTube Video Summarization
def youtube_summarization_tab():
    with tabs[4]:
        st.header("YouTube Video Summarization")
        video_url = st.text_input("Enter YouTube Video URL:")
        summarize = st.button("Summarize Video")

        if summarize and video_url:
            # Placeholder
            st.write("Video Summary:", "[Summary details here]")

text_query_tab()
image_processing_tab()
image_generation_tab()
resume_upgradation_tab()
youtube_summarization_tab()