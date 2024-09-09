import streamlit as st
import requests
from PIL import Image

# Custom CSS for a premium look and feel
st.markdown("""
    <style>
    /* Main background - Thinner yellow section */
    body {
        background: linear-gradient(135deg, #fefbcd 10%, #b2d8d8 90%);  /* Thinner yellow and more blue */
        color: #333333;
    }

    /* Header with blue color gradient and clear style */
    @keyframes fade-in {
        0% {
            opacity: 0;
        }
        100% {
            opacity: 1;
        }
    }

    h1 {
        font-family: 'Playfair Display', serif;
        color: #3a77c1;  /* Dark blue for the header */
        text-align: center;
        letter-spacing: 3px;
        padding: 20px 0;
        animation: fade-in 1.2s ease-in-out;
        font-size: 3.2em;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.3); /* Subtle shadow for clarity */
    }

    h2 {
        font-family: 'Roboto', sans-serif;
        color: #1f4e79;  /* Slightly lighter blue for subheader */
        text-align: center;
        letter-spacing: 1.5px;
        margin-bottom: 20px;
        animation: fade-in 1.5s ease-in-out;
        font-size: 1.8em;
    }

    /* Custom star and tooth icons */
    .custom-header {
        font-family: 'Playfair Display', serif;
        color: #3a77c1;
        text-align: center;
        letter-spacing: 3px;
        padding: 20px 0;
        font-size: 3.2em;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .custom-header .star-icon {
        color: #ffcc00;  /* Bright yellow for the star icon */
        margin-right: 10px;
        font-size: 1.5em;
    }
    .custom-header .tooth-icon {
        color: #1f4e79;  /* Dark blue for tooth icon */
        margin-left: 10px;
        font-size: 1.5em;
    }

    /* Subheader with subtle shadow */
    .subheader {
        font-family: 'Roboto', sans-serif;
        color: #ffffff;
        background-color: #1f4e79;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    /* Upload area style */
    .css-1dp5vir {
        background-color: #fff9e5 !important;
        border: 2px solid #b2d8d8;
        color: #1f4e79 !important;
        border-radius: 15px;
        padding: 15px;
        transition: background-color 0.3s ease;
    }

    /* Button design */
    .stButton button {
        background-color: #3a77c1;
        color: #ffffff;
        font-size: 18px;
        padding: 12px 30px;
        border-radius: 8px;
        font-family: 'Roboto', sans-serif;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(58, 119, 193, 0.3);
    }
    .stButton button:hover {
        background-color: #1f4e79;
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(58, 119, 193, 0.5);
    }

    /* Results box with soft shadow */
    .result-box {
        background-color: #1f4e79;
        color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        font-size: 18px;
        font-family: 'Roboto', sans-serif;
        margin-top: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    .result-box:hover {
        transform: scale(1.02); /* Slight enlargement on hover */
    }

    </style>
""", unsafe_allow_html=True)

# Header with star and tooth icons
st.markdown("""
    <div class="custom-header">
        <span class="star-icon">⭐</span>
        Star Smiles
        <span class="tooth-icon">🦷</span>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h2>Tooth Disease Prediction</h2>", unsafe_allow_html=True)

# Upload form
with st.form(key='image_for_api'):
    image = st.file_uploader('Upload your dental X-ray or tooth image', type=['jpg', 'png', 'jpeg'])
    submit = st.form_submit_button('Predict')

# Process and display results
if submit and image is not None:
    img_bytes = image.getvalue()
    url = f'http://127.0.0.1:8000/predict'
    response = requests.post(url, files={'img': img_bytes})
    prediction = response.json()

    st.markdown("<h3>Results:</h3>", unsafe_allow_html=True)

    # Display prediction results
    result_html = ""
    threshold = 0.5
    pred = None
    for tooth_disease, probability in prediction.items():
        probability_percent = round(100 * probability, 2)
        result_html += f"<p><b>{tooth_disease}</b>: {probability_percent}%</p>"
        if probability > threshold:
            threshold = probability
            pred = tooth_disease

    st.markdown(f"<div class='result-box'>{result_html}</div>", unsafe_allow_html=True)

# Handle missing image case
if not image and submit:
    st.warning("Please upload an image to get a prediction.")
