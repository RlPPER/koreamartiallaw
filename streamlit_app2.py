import streamlit as st
import requests
import json
import http.client
from googletrans import Translator
import os
from dotenv import load_dotenv
load_dotenv()
import urllib.request
client_id = os.environ.get('NAVER_CLIENT_ID')
client_secret = os.environ.get('NAVER_CLIENT_SECRET')

# Translator 객체 생성
translator = Translator()

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
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request('POST', endpoint, json.dumps(completion_request), headers)
        response = conn.getresponse()
        result = json.loads(response.read().decode(encoding='utf-8'))
        conn.close()
        return result
#40b7767cc1d846e3bf2bde48ccb690a5
    def execute(self, completion_request):
        res = self._send_request(completion_request)
        if res['status']['code'] == '20000':
            return res['result']['text']
        else:
            return 'Error'

# 클로바 X 요약 함수
def summarize_text_clova(text):
    completion_executor = CompletionExecutor(
        host='clovastudio.apigw.ntruss.com',
        api_key=os.environ.get('CLOVA_API_KEY'),
        api_key_primary_val=os.environ.get('CLOVA_API_KEY_PRIMARY_VAL'),
        request_id=os.environ.get('CLOVA_REQUEST_ID')
    )

    request_data = {
        "texts": [text],
        "segMinSize": 300,
        "includeAiFilters": True,
        "autoSentenceSplitter": True,
        "segCount": -1,
        "segMaxSize": 1000
    }

    response_text = completion_executor.execute(request_data)
    return response_text

# 뉴스 검색 함수
def search_news(query="계엄", display=7):
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

# 텍스트 번역 함수
def translate_text(text, dest='en'):
    try:
        translated = translator.translate(text, dest=dest)
        return translated.text
    except Exception as e:
        st.error(f"Translation failed: {e}")
        return text
def summarize_and_translate_clova(text):
    completion_executor = CompletionExecutor(
        host='clovastudio.apigw.ntruss.com',
        api_key=os.getenv('CLOVA_API_KEY'),
        api_key_primary_val=os.getenv('CLOVA_API_KEY_PRIMARY_VAL'),
        request_id=os.getenv('CLOVA_REQUEST_ID')
    )

    # Summarization request
    request_data = {
        "texts": [text],
        "segMinSize": 300,
        "includeAiFilters": True,
        "autoSentenceSplitter": True,
        "segCount": -1,
        "segMaxSize": 1000
    }

    summarization_response = completion_executor.execute_summarization(request_data)
    if summarization_response['status']['code'] == '20000':
        summarized_text = summarization_response['result']['text']
        
        # Translation request using chat API
        preset_text = [
            {"role": "system", "content": "Translate the following Korean text to English."},
            {"role": "user", "content": summarized_text}
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
        if 'data' in translation_response:
            translated_text = json.loads(translation_response['data'])['choices'][0]['message']['content']
            return summarized_text, translated_text
        else:
            return summarized_text, 'Translation Error'
    else:
        return 'Summarization Error', 'Translation Error'
    
    
# Streamlit 애플리케이션
st.title("What's happening in Korea? News and photos related to martial law")
st.header("This website is intended to share news related to the declaration of martial law in South Korea on December 2, 2024 I want to raise awareness about the critical situation in South Korea. I'm urgently seeking help. If you can assist, please contact me at stormkingrank1@gmail.com.")

if 'search_count' not in st.session_state:
    st.session_state['search_count'] = 0

if st.button("Search"):
    if st.session_state['search_count'] < 5:
        st.session_state['search_count'] += 1
        news_items = search_news()
        for item in news_items:
            st.subheader(item['title'])
            st.write(item['description'])
            # 클로바 X 요약 및 번역 함수 사용
            summary, translated_summary = summarize_and_translate_clova(item['description'])
            st.write("Summary:", summary)
            st.write("Translated Summary:", translated_summary)
            st.write(f"[Original Article]({item['link']})")
    else:
        st.warning("You have reached the maximum number of searches (5).")
        
        
        