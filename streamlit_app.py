import streamlit as st
from PIL import Image
import random

# Streamlit 웹 앱 제목 설정
st.title("What's Happening in Korea?: News & Photos on the Declaration of Martial Law")

# 이미지 업로드
uploaded_files = st.file_uploader("Choose images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# 코멘트 입력
comment = st.text_input("Enter your comment:(한마디 입력해주세요)")

# 이미지가 업로드된 경우
if uploaded_files:
    # 업로드된 이미지들을 리스트로 저장
    uploaded_images = [Image.open(file) for file in uploaded_files]

    # 사이드바에 랜덤 이미지 3개 표시
    latest_images = uploaded_images[-3:]  # 업로드된 순서대로 마지막 3개 이미지
    # 사이드바에 최신 3개 이미지 표시
    for image in latest_images:
        st.sidebar.image(image, caption="Latest Image", use_column_width=True)
    
    # 페이지네이션: 이미지 리스트와 페이지 정보 처리
    per_page = 15
    total_pages = len(uploaded_images) // per_page + (1 if len(uploaded_images) % per_page > 0 else 0)

    # 페이지 선택
    page = st.number_input("Choose a page:(To view previous photos, please adjust the page number)", min_value=1, max_value=total_pages, value=1)

    # 현재 페이지의 이미지들 표시
    start_idx = (page - 1) * per_page
    end_idx = min(page * per_page, len(uploaded_images))

    st.write(f"Showing images {start_idx + 1} to {end_idx} of {len(uploaded_images)}")

    for image in uploaded_images[start_idx:end_idx]:
        st.image(image, caption="Uploaded Image", use_column_width=True)

    # 코멘트가 있을 경우 출력
    if comment:
        st.write(f"Your Comment: {comment}")
    else:
        st.write("Please enter a comment.")
else:
    st.write("Please upload images and enter a comment.")
