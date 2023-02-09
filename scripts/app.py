import streamlit as st
import numpy as np
from PIL import Image
from engine import predict

st.title('Vibrio Counter')
uploaded_file = st.file_uploader("Choose a file", type=["jpg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    st.image(img_array)
    data = predict(img_array)
    st.dataframe(data=data)