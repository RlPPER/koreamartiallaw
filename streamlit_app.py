import streamlit as st
from PIL import Image
import random
import os

# 디렉토리 설정 (이미지를 저장할 폴더)
image_dir = "uploaded_images"
os.makedirs(image_dir, exist_ok=True)

# Streamlit 웹 앱 제목 설정
st.title("Upload Image and Comment")

# 사이드바에 랜덤 이미지 3개 표시
def display_random_images():
    uploaded_files = os.listdir(image_dir)
    if len(uploaded_files) >= 3:
        random_images = random.sample(uploaded_files, 3)
        for image_name in random_images:
            image_path = os.path.join(image_dir, image_name)
            image = Image.open(image_path)
            st.sidebar.image(image, caption=image_name, use_column_width=True)

# 이미지 업로드
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# 코멘트 입력
comment = st.text_input("Enter your comment:")

# 이미지 업로드 및 저장 처리
if uploaded_file is not None:
    for file in uploaded_file:
        image_path = os.path.join(image_dir, file.name)
        with open(image_path, "wb") as f:
            f.write(file.getbuffer())

# 랜덤 이미지 3개 사이드바에 표시
display_random_images()

# 페이지네이션: 이미지 리스트와 페이지 정보 처리
uploaded_images = os.listdir(image_dir)
uploaded_images.sort()  # 정렬
per_page = 15
total_pages = len(uploaded_images) // per_page + (1 if len(uploaded_images) % per_page > 0 else 0)

# 페이지 선택
page = st.number_input("Choose a page:", min_value=1, max_value=total_pages, value=1)

# 현재 페이지의 이미지들 표시
start_idx = (page - 1) * per_page
end_idx = min(page * per_page, len(uploaded_images))

st.write(f"Showing images {start_idx + 1} to {end_idx} of {len(uploaded_images)}")

for image_name in uploaded_images[start_idx:end_idx]:
    image_path = os.path.join(image_dir, image_name)
    image = Image.open(image_path)
    st.image(image, caption=image_name, use_column_width=True)

# 코멘트가 있을 경우 출력
if uploaded_file is not None and comment:
    st.write(f"Your Comment: {comment}")
elif uploaded_file is not None:
    st.write("Please enter a comment.")
else:
    st.write("Please upload an image and enter a comment.")
