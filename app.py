import streamlit as st
import requests

'''# Star Smiles'''

st.header('Tooth disease prediction')

with st.form(key='image_for_api'):

    image = st.file_uploader('Upload your image')
    submit = st.form_submit_button('Predict')

if submit:

    if image is not None:
        img_bytes = image.getvalue()

    url = f'http://127.0.0.1:8000/predict'
    response = requests.post(url, files={'img': img_bytes})

    prediction = response.json()
    threshold = 0.5
    pred = None

    st.header('Results:')
    for type in prediction:
        st.write(f'The probability of {type} is {round(100*prediction[type], 2)}%')
        if prediction[type]>threshold:
            threshold = prediction[type]
            pred = type

    if pred is None:
        st.subheader('The model can not predict with enough confidence')
    else:
        st.subheader(f'The prediction is {pred}')



    #st.write(f'{response.content}')
    #prediction = response.json()
    #st.header(f'result: {prediction}')
