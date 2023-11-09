import streamlit as st
import streamlit as st
import tempfile
from pathlib import Path
from PIL import Image

# Set page config to wide mode
st.set_page_config(layout="wide")

# Function to process the video
def process_video(input_path):
    # Your CV model processing code here
    # For now, let's just return the same path for demonstration
    # Simulate processing time with sleep
    import time
    time.sleep(5)  # Remove this in your actual function
    return input_path


# Function to display the video in Streamlit
def display_video(video_path, key=None):
    st_video = open(video_path, 'rb')
    video_bytes = st_video.read()
    st.video(video_bytes, format="video/mp4")


st.title("CV Model Demonstration App")

# Create a temporary directory within the project directory
temp_dir = Path("temp_videos")
temp_dir.mkdir(parents=True, exist_ok=True)

# Upload file section
uploaded_file = st.file_uploader("Upload a video...", type=["mp4", "mov", "avi", "asf", "m4v"])

# If a file is uploaded, save it to a temporary directory and display it
if uploaded_file is not None:
    with st.spinner('Uploading...'):
        tfile = tempfile.NamedTemporaryFile(delete=False, dir=temp_dir, suffix='.mp4') 
        tfile.write(uploaded_file.read())
        video_path = tfile.name
        st.success('Upload successful!')
        tfile.close()

    # Create two columns for preview and processed videos
    col1, col2 = st.columns([1, 1])

    # Use the first column for the preview section
    with col1:
        st.header("Locations")
        # Opening the image
        image = Image.open('Assets/map.png')
        # Displaying the image on streamlit app
        st.image(image, caption='Some caption of this image')

    with col2:
        st.header("Video")
        with st.spinner('Extracting...'):
            # Process the video and get the path to the result
            processed_video_path = process_video(video_path)
            st.success('Extracting complete!')
            # Display the processed video
            display_video(processed_video_path)


