import streamlit as st
import requests
from transformers import pipeline
import streamlit as st
from PIL import Image
import os

# Streamlit 웹 앱 제목 설정
st.title("What's Happening in Korea?: News & Photos on the Declaration of Martial Law")

# 이미지 업로드
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

# 코멘트 입력
comment = st.text_input("Enter your comment:")

# 이미지와 코멘트가 모두 업로드된 경우
if uploaded_file is not None and comment:
    # 이미지 열기
    image = Image.open(uploaded_file)
    
    # 이미지와 코멘트 출력
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write(f"Your Comment: {comment}")
elif uploaded_file is not None:
    # 이미지만 업로드된 경우
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("Please enter a comment.")
else:
    st.write("Please upload an image and enter a comment.")
