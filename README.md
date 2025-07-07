# Unified-AI
Comprehensive AI  Driven web Appllication
Unified AI: An All-in-One AI-Powered Web Application

Overview:
Unified AI is an integrated web-based application developed using Streamlit, designed to combine multiple AI-driven features into a single, user-friendly platform. The goal is to allow users to interact with powerful AI services for a variety of tasks without switching between multiple tools.

Key Features:

Text Query:

Users can ask any question directly in the app.

The input is sent to Google Gemini AI using a generative model.

The AI processes the query and returns a relevant, detailed response.

Image Processing:

Users can upload an image and provide a custom prompt.

Gemini AI analyzes the image based on the given context.

The processed result or description is displayed within the app.

Image Generation:

Users enter a text description or idea.

The app connects with the Hugging Face API to generate an image based on the prompt.

The generated image is displayed for download or further use.

Resume Upgradation:

Users can upload a PDF resume.

The system uses PyPDF2 to extract text.

It identifies the candidate’s field (e.g., Data Science, Web Development) and suggests relevant online courses to improve skills.

YouTube Video Summarization:

Users provide a YouTube video URL.

The YouTube Transcript API fetches the video transcript.

Gemini AI summarizes the content and displays a concise version for quick understanding.

Technical Stack:

Frontend & Framework: Streamlit for building the interactive web interface.

AI & NLP: Google Gemini AI for text generation, image analysis, and summarization tasks.

API Integrations: Hugging Face API for AI-based image generation.

File & Data Handling: PyPDF2 for PDF processing, YouTube Transcript API for extracting subtitles, and environment variables for secure API key storage using .env and dotenv.

Libraries Used: requests, PIL.Image, BytesIO, re, os, base64 for handling HTTP requests, images, binary data, regex operations, and encoding/decoding.

Security & Deployment:

API keys are securely managed using environment variables (.env file) and loaded at runtime.

Input validation ensures that only valid files and formats are processed.

The project is suitable for deployment on platforms like Streamlit Cloud, AWS, or Google Cloud.

