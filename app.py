import streamlit as st
import requests

# Custom CSS for a refined look with a very thin yellow bar
st.markdown("""
    <style>
    /* Main background - Very thin yellow section */
    body {
        background: linear-gradient(135deg, #fef5d1 0.0001%, #b2d8d8 99.9999%);
        color: #333333;
        margin: 0;
        padding: 0;
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
        color: #3a77c1;
        text-align: center;
        letter-spacing: 3px;
        padding: 15px 0;
        animation: fade-in 1.2s ease-in-out;
        font-size: 3em;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }

    h2 {
        font-family: 'Roboto', sans-serif;
        color: #1f4e79;
        text-align: center;
        letter-spacing: 1.5px;
        margin-bottom: 15px;
        animation: fade-in 1.5s ease-in-out;
        font-size: 1.6em;
        text-decoration: underline;
    }

    /* Custom star and tooth icons */
    .custom-header {
        font-family: 'Playfair Display', serif;
        color: #3a77c1;
        text-align: center;
        letter-spacing: 3px;
        padding: 15px 0;
        font-size: 3em;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .custom-header .star-icon {
        color: #ffcc00;
        margin-right: 10px;
        font-size: 1.5em;
    }
    .custom-header .tooth-icon {
        color: #1f4e79;
        margin-left: 10px;
        font-size: 1.5em;
    }

    /* Subheader with subtle shadow */
    .subheader {
        font-family: 'Roboto', sans-serif;
        color: #ffffff;
        background-color: #1f4e79;
        padding: 10px;
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
        transform: scale(1.02);
    }

    /* Result header styling */
    .result-header {
        font-size: 1.2em;
        font-family: 'Roboto', sans-serif;
        color: #1f4e79;
        margin-top: 20px;
        text-align: center;
    }

    /* Styling for highlighting the highest prediction */
    .highlight {
        color: #ffcc00;  /* Bright yellow */
        font-weight: bold;
        font-size: 1.8em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3); /* Subtle shadow */
    }
    .confidence {
        color: #3a77c1; /* Blue color for confidence percentage */
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Header with star and tooth icons (Updated with non-sparkling star)
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
    url = f'https://starsmiles-308707400221.europe-west1.run.app/predict'
    response = requests.post(url, files={'img': img_bytes})
    prediction = response.json()

    # Find the highest prediction
    highest_pred = max(prediction, key=prediction.get)
    highest_prob = round(100 * prediction[highest_pred], 2)

    # Display header and highest prediction with highlighting
    st.markdown(f"""
        <h3 class='result-header'>
            Results: The predicted condition is
            <span class="highlight">{highest_pred}</span>
            with a confidence of
            <span class="confidence">{highest_prob}%</span>
        </h3>
    """, unsafe_allow_html=True)

    # Display prediction results
    result_html = ""
    for tooth_disease, probability in prediction.items():
        probability_percent = round(100 * probability, 2)
        result_html += f"<p><b>{tooth_disease}</b>: {probability_percent}%</p>"

    st.markdown(f"<div class='result-box'>{result_html}</div>", unsafe_allow_html=True)

# Handle missing image case
if not image and submit:
    st.warning("Please upload an image to get a prediction.")
