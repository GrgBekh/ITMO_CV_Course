import streamlit as st
import pandas as pd
from pathlib import Path
import pydeck as pdk
import tempfile
import os
from ultralytics import YOLO
import moviepy.editor as moviepy

# Page config and title
st.set_page_config(layout="wide")
st.title("🔥 CV Model Demonstration App")


# Create a temporary directory within the project directory
temp_dir = Path("temp_videos")
temp_dir.mkdir(parents=True, exist_ok=True)


# Initialize session state variables if they don't exist
if 'video_processed' not in st.session_state:
    st.session_state['video_processed'] = False

if 'locations' not in st.session_state:
    st.session_state['locations'] = None

if 'model' not in st.session_state:
    st.session_state['model'] = None

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

# Upload file section
uploaded_file = st.file_uploader("Upload a video...", type=["mp4", "mov", "avi", "asf", "m4v"])

# Prepare the model
if not st.session_state['model']:
    with st.spinner('Model preparation...'):
        # model weights for inference
        model_path = "weights/35epochs.pt"
        model = YOLO(model_path)
        st.session_state['model'] = model


# Define locations variables
if not st.session_state['locations']:
    # Sample data for locations
    locations = [
        {"name": "Location 1", "lat": 54.921094, "lon": 61.192561, "video_path": ""},
        {"name": "Location 2", "lat": 54.981479, "lon": 61.111365, "video_path": "ITMO_CV_Course\\temp_videos\\tmpx6vfyuvc.mp4"},
    ]
    df = pd.DataFrame(locations)

    # Sample data for the trajectory
    trajectory = [
        {"name": "Trajectory 1", "path": [[61.363556, 54.980254], [61.111365, 54.981479],[61.192561, 54.921094], [61.363556, 54.980254]]},
    ]
    df_trajectory = pd.DataFrame(trajectory)

    # Save the session
    st.session_state['locations'] = (df, df_trajectory)


# Upload the file and send it to the model
if uploaded_file is not None and not st.session_state['video_processed']:
    with st.spinner('Extracting...'):
        # Upload a file
        tfile = tempfile.NamedTemporaryFile(delete=False, dir=temp_dir, suffix='.mp4')
        tfile.write(uploaded_file.read())
        video_path = tfile.name
        tfile.close()

        # Process the file
        proc_filename = f"{os.path.split(video_path)[-1][:-4]}_processed"
        results = st.session_state['model'].predict(source=video_path, conf=0.01, hide_conf=True, max_det=1, classes=0, save=True, project="temp_videos", name=proc_filename)
        clear_filename = os.path.split(video_path)[-1]

        output_path = f"temp_videos\\{proc_filename}\\{clear_filename[:-4]}.avi"

        # Convert to mp4 format so streamlit will show the vid
        clip = moviepy.VideoFileClip(output_path)
        clip.write_videofile(output_path.replace('avi', 'mp4'))

        # Set the output filepath to show (dataframe locations used)
        st.session_state['locations'][0]["video_path"] = output_path.replace('avi', 'mp4')
        st.success('Sucessfully extracted!')

        # Save the session
        st.session_state['video_processed'] = True


# Check if the video has been processed
if st.session_state['video_processed']:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.header("Locations")
        create_map(st.session_state['locations'][0], st.session_state['locations'][1])

    with col2:
        st.header("Video")
        # Display buttons for each location and play the corresponding video when clicked
        for index, row in st.session_state['locations'][0].iterrows():
            if st.button(f"Play video from {row['name']}"):
                st.video(row['video_path'])
