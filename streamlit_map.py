import streamlit as st
import pandas as pd
from pathlib import Path
import pydeck as pdk
import tempfile

st.set_page_config(layout="wide")
st.title("🔥 CV Model Demonstration App")

# Sample data: list of latitudes, longitudes, names, and video file paths
locations = [
    {"name": "Location 1", "lat": 54.921094, "lon":
        61.192561, "video_path": "ITMO_CV_Course\\temp_videos\\tmpx6vfyuvc.mp4"},
    {"name": "Location 2", "lat": 54.981479, "lon":
        61.111365, "video_path": "ITMO_CV_Course\\temp_videos\\tmpx6vfyuvc.mp4"},
    # Add more locations and corresponding videos here
]

# Convert the locations to a DataFrame
df = pd.DataFrame(locations)

# Sample data for the trajectory
# This should be a list of lists, where each inner list represents a [longitude, latitude] pair
trajectory_data = [
    {"name": "Trajectory 1", "path": [[61.363556, 54.980254], [61.111365, 54.981479],[61.192561, 54.921094], [61.363556, 54.980254]]},
    # Add more trajectories here
]

# Convert trajectory data to a DataFrame
df_trajectory = pd.DataFrame(trajectory_data)

# Function to process the video
def process_video(input_path):
    # Your CV model processing code here
    import time
    time.sleep(5)  # Remove this in your actual function
    return input_path


# Function to create a map with points and text labels
def create_map(df_points, df_trajectory):
        # Create a PathLayer for the trajectory
    path_layer = pdk.Layer(
        "PathLayer",
        data=df_trajectory,
        get_path="path",
        get_color=[255, 0, 0],  # Red color for the trajectory
        width_scale=20,
        width_min_pixels=2,
        pickable=True,
        auto_highlight=True,
    )

    # Create a ScatterplotLayer for the locations
    scatterplot_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_points,
        get_position='[lon, lat]',
        get_color='[255, 0, 0, 160]',  # Red color
        get_radius=500,  # Radius in meters
        pickable=True,
        auto_highlight=True,
    )

    # Create a TextLayer for the location names
    text_layer = pdk.Layer(
        "TextLayer",
        data=df_points,
        get_position='[lon, lat]',
        get_text='name',
        get_color='[255,255,255,255]',  # White color
        get_size=12,
        get_alignment_baseline="'top'",
    )

    # Set the view for the map
    view_state = pdk.ViewState(
        latitude=df_points["lat"].mean(),
        longitude=df_points["lon"].mean(),
        zoom=10
    )

    # Render the map with the layers
    st.pydeck_chart(pdk.Deck(layers=[path_layer, scatterplot_layer, text_layer], initial_view_state=view_state,
                    map_style='mapbox://styles/mapbox/dark-v10'))


# Initialize session state variables if they don't exist
if 'uploaded_video_path' not in st.session_state:
    st.session_state['uploaded_video_path'] = None

if 'video_processed' not in st.session_state:
    st.session_state['video_processed'] = False


# Create a temporary directory within the project directory
temp_dir = Path("temp_videos")
temp_dir.mkdir(parents=True, exist_ok=True)

# Upload file section
uploaded_file = st.file_uploader("Upload a video...", type=[
                                 "mp4", "mov", "avi", "asf", "m4v"])

# If a file is uploaded, save it to a temporary directory and display it
if uploaded_file is not None and not st.session_state['video_processed']:
    with st.spinner('Extracting...'):
        tfile = tempfile.NamedTemporaryFile(
            delete=False, dir=temp_dir, suffix='.mp4')
        tfile.write(uploaded_file.read())
        st.session_state['uploaded_video_path'] = tfile.name
        video_path = tfile.name
        tfile.close()
        
        process_video(video_path)
        st.session_state['video_processed'] = True
        st.success('Extracting successful!')

# Check if the video has been processed
if st.session_state['video_processed']:

    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("Locations")
        create_map(df, df_trajectory)

    with col2:
        st.header("Video")
        # Display buttons for each location and play the corresponding video when clicked
        for location in locations:
            if st.button(f"Play video from {location['name']}"):
                st.video(location['video_path'])
