import streamlit as st
<<<<<<< HEAD
import requests
import json
import http.client
import os
from dotenv import load_dotenv
from PIL import Image
import io
load_dotenv()
client_id = os.environ.get('NAVER_CLIENT_ID')
client_secret = os.environ.get('NAVER_CLIENT_SECRET')

# Translator 객체 생성
# CompletionExecutor 클래스 정의
class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def _send_request(self, completion_request):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request('POST', '/testapp/v1/api-tools/summarization/v2/40b7767cc1d846e3bf2bde48ccb690a5', json.dumps(completion_request), headers)
        response = conn.getresponse()
        result = json.loads(response.read().decode(encoding='utf-8'))
        conn.close()
        return result
    def execute_summarization(self, completion_request):
        return self._send_request(completion_request)

    def execute_translation(self, completion_request):
        return self._send_request(completion_request)

# 클로바 X 요약 함수
def summarize_clova(text):
    completion_executor = CompletionExecutor(
        host='clovastudio.apigw.ntruss.com',
        api_key=os.environ.get('CLOVA_API_KEY'),
        api_key_primary_val=os.environ.get('CLOVA_API_KEY_PRIMARY_VAL'),
        request_id=os.environ.get('CLOVA_REQUEST_ID')
    )

    # Summarization requests
    request_data = {
        "texts": [text],
        "segMinSize": 300,
        "includeAiFilters": True,
        "autoSentenceSplitter": True,
        "segCount": -1,
        "segMaxSize": 1000
    }

    summarization_response = completion_executor.execute_summarization(request_data)
    if 'status' in summarization_response and summarization_response['status']['code'] == '20000':
        return summarization_response['result']['text']
    else:
        return 'Summarization Error'

def translate_clova(text):
    completion_executor = CompletionExecutor(
        host='clovastudio.apigw.ntruss.com',
        api_key=os.environ.get('CLOVA_API_KEY'),
        api_key_primary_val=os.environ.get('CLOVA_API_KEY_PRIMARY_VAL'),
        request_id=os.environ.get('CLOVA_REQUEST_ID')
    )

    # Translation request using chat API
    preset_text = [
        {"role": "system", "content": "너는 최고의 영어 번역가야. 다음 한글을 영어로 자연스럽게 번역해줘."},
        {"role": "user", "content": text}
    ]

    translate_request_data = {
        'messages': preset_text,
        'topP': 0.6,
        'topK': 0,
        'maxTokens': 512,
        'temperature': 0.5,
        'repeatPenalty': 5.0,
        'stopBefore': [],
        'includeAiFilters': True,
        'seed': 0
    }

    translation_response = completion_executor.execute_translation(translate_request_data)
    if 'choices' in translation_response:
        return translation_response['choices'][0]['message']['content']
    else:
        st.write("Translation:", translation_response)

        return 'Translation Error'

# 뉴스 검색 함수
def search_news(query="계엄", display=8):
    encoded_query = query
    url = f"https://openapi.naver.com/v1/search/news.json?query={encoded_query}&display={display}"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        st.error(f"Failed to search news. Status code: {response.status_code}")
        return []

# 이미지 다운로드 함수
def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
        else:
            return None
    except Exception as e:
        st.error(f"Failed to download image: {e}")
        return None


# Streamlit 애플리케이션
st.title("What's happening in Korea? News and photos related to martial law")
st.subheader("This website is intended to share news related to the declaration of martial law in South Korea on December 2, 2024 I want to raise awareness about the critical situation in South Korea. I'm urgently seeking help. If you can assist, please contact me at stormkingrank1@gmail.com.")
# 검색 버튼 클릭 횟수 제한
if 'search_count' not in st.session_state:
    st.session_state['search_count'] = 0

if st.button("Search"):
    if st.session_state['search_count'] < 3:
        st.session_state['search_count'] += 1
        news_items = search_news()
        for item in news_items:
            st.subheader(item['title'])
            #st.write(item['description'])
            
            # 이미지 불러오기
            if 'image' in item and item['image']:
                image = download_image(item['image'])
                if image:
                    st.image(image, caption=item['title'], use_column_width=True)
            
            # 클로바 X 요약 함수 사용
            summary = summarize_clova(item['description'])
            st.write("Summary:", summary)
            
            # 클로바 X 번역 함수 사용
            #translated_summary = translate_clova(summary)
            #st.write("Translated Summary:", translated_summary)
            
            st.write(f"[Original Article]({item['link']})")
    else:
        st.warning("You have reached the maximum number of searches (3).")
        
        
        
=======
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
>>>>>>> 230ae12730a564a26c817ac82f5e19fc71b0f451
