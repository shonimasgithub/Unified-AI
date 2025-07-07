import streamlit as st
import openai
from io import BytesIO
from PIL import Image
import requests
from io import BytesIO

# Streamlit app title
st.title("Text-to-Image Generator")

# Sidebar for API key input
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")

def generate_image(prompt, api_key):
    """Generate an image from text using OpenAI's API (new interface)."""
    try:
        openai.api_key = api_key

        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        # Extract the image URL from the response
        image_url = response['data'][0]['url']
        
        # Download the image from the URL
        img_data = requests.get(image_url).content
        img = Image.open(BytesIO(img_data))
        return img

    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Input prompt
prompt = st.text_area("Enter a text prompt for the image:", placeholder="e.g., A futuristic cityscape at sunset")

# Generate button
if st.button("Generate Image"):
    if not api_key:
        st.warning("Please provide your OpenAI API key in the sidebar.")
    elif not prompt.strip():
        st.warning("Please enter a text prompt.")
    else:
        st.info("Generating image... Please wait.")
        img = generate_image(prompt, api_key)

        if img:
            # Display the generated image
            st.image(img, caption="Generated Image", use_column_width=True)

            # Provide a download link for the image
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format="PNG")
            img_byte_arr = img_byte_arr.getvalue()
            st.download_button(
                label="Download Image",
                data=img_byte_arr,
                file_name="generated_image.png",
                mime="image/png"
            )

# Footer
st.markdown("---")
st.markdown(
    
)
