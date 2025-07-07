import streamlit as st
from PIL import Image
import os
import requests
import google.generativeai as genai
import PyPDF2
from dotenv import load_dotenv
from io import BytesIO
from youtube_transcript_api import YouTubeTranscriptApi
import re
from courses import ds_courses, web_courses, android_courses, ios_courses, uiux_courses
import base64

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Streamlit Page Setup
st.set_page_config(page_title="Unified AI", layout="wide")
st.title("🧠 Unified AI")

# Define Tabs
tabs = st.tabs([
    "Text Query", "Image Processing", "Image Generation",
    "Resume Upgradation", "YouTube Video Summarization"
])

# --------------------------- Text Query ---------------------------
def text_query_tab():
    with tabs[0]:
        st.header("📝 Text Query")

        def get_gemini_response(query):
            try:
                model = genai.GenerativeModel("gemini-1.5-pro-latest")
                response = model.generate_content(query)
                return response.text
            except Exception as e:
                return f"Error: {str(e)}"

        input_query = st.text_input("Enter your question:")
        if st.button("Ask Question") and input_query:
            response = get_gemini_response(input_query)
            st.subheader("Response:")
            st.write(response)

# --------------------------- Image Processing ---------------------------
def image_processing_tab():
    with tabs[1]:
        st.header("📷 Image Processing")

        def process_image(uploaded_file, prompt):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash-latest")
                image_bytes = uploaded_file.getvalue()
                response = model.generate_content([prompt, {"mime_type": uploaded_file.type, "data": image_bytes}])
                return response.text
            except Exception as e:
                return f"Error: {str(e)}"

        uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
        prompt = st.text_input("Describe what you want to analyze:")
        
        if st.button("Analyze Image") and uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            with st.spinner("Analyzing..."):
                response = process_image(uploaded_file, prompt)
                st.subheader("Analysis Result:")
                st.write(response)

# --------------------------- Image Generation ---------------------------
def image_generation_tab():
    with tabs[2]:
        st.header("🎨 Image Generation")
        prompt = st.text_area("Enter a prompt for image generation:")
        
        if st.button("Generate Image") and prompt.strip():
            with st.spinner("Generating image..."):
                headers = {"Authorization": f"Bearer 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"}
                data = {"inputs": prompt}
                response = requests.post(
                    "https://api-inference.huggingface.co/models/kothariyashhh/GenAi-Texttoimage",
                    headers=headers, json=data
                )
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    st.image(img, caption="Generated Image", use_column_width=True)
                else:
                    st.error(f"Error: {response.status_code}, {response.text}")

# --------------------------- Resume Upgradation ---------------------------
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def detect_field(resume_text):
    ds_keywords = ['machine learning', 'data science', 'python', 'pandas', 'numpy', 'scikit-learn']
    web_keywords = ['html', 'css', 'javascript', 'react', 'django', 'flask']
    android_keywords = ['android', 'kotlin', 'java']
    ios_keywords = ['ios', 'swift', 'objective-c']
    uiux_keywords = ['ui', 'ux', 'figma', 'sketch', 'adobe xd']

    text_lower = resume_text.lower()

    if any(keyword in text_lower for keyword in ds_keywords):
        return 'Data Science'
    elif any(keyword in text_lower for keyword in web_keywords):
        return 'Web Development'
    elif any(keyword in text_lower for keyword in android_keywords):
        return 'Android Development'
    elif any(keyword in text_lower for keyword in ios_keywords):
        return 'IOS Development'
    elif any(keyword in text_lower for keyword in uiux_keywords):
        return 'UI/UX Design'
    else:
        return 'General'

def recommend_courses(field):
    if field == 'Data Science':
        return ds_courses
    elif field == 'Web Development':
        return web_courses
    elif field == 'Android Development':
        return android_courses
    elif field == 'IOS Development':
        return ios_courses
    elif field == 'UI/UX Design':
        return uiux_courses
    else:
        return []

def resume_upgradation_tab():
    with tabs[3]:
        st.header("📄 Resume Upgradation")

        uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")
        if uploaded_file is not None:
            resume_text = extract_text_from_pdf(uploaded_file)
            field = detect_field(resume_text)
            courses = recommend_courses(field)
            
            st.subheader("Extracted Resume Text")
            st.text_area("Resume Text", resume_text, height=300)
            st.markdown(f"**Detected Field:** {field}")
            
            st.subheader("Recommended Courses")
            if courses:
                for course_name, course_link in courses:
                    st.markdown(f"- [{course_name}]({course_link})")
            else:
                st.write("No specific courses available for the detected field.")

# --------------------------- YouTube Video Summarization ---------------------------
def youtube_summarization_tab():
    with tabs[4]:
        st.header("🎥 YouTube Video Summarization")
        
        def extract_video_id(url):
            match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
            return match.group(1) if match else None
        
        def get_video_transcript(video_url):
            video_id = extract_video_id(video_url)
            if not video_id:
                return "Invalid YouTube URL."
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                return " ".join([entry["text"] for entry in transcript])
            except Exception as e:
                return f"Error: {str(e)}"

        def summarize_text_with_gemini(text):
            try:
                model = genai.GenerativeModel("gemini-1.5-pro-latest")
                response = model.generate_content(f"Summarize this YouTube transcript:\n{text}")
                return response.text
            except Exception as e:
                return f"Error: {str(e)}"

        video_url = st.text_input("Enter YouTube Video URL:")
        if st.button("Summarize Video") and video_url:
            transcript = get_video_transcript(video_url)
            summary = summarize_text_with_gemini(transcript)
            st.subheader("📄 Video Summary:")
            st.write(summary)
text_query_tab()
image_processing_tab()
image_generation_tab()
resume_upgradation_tab()
youtube_summarization_tab()

