# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import json
import requests
import os
import re
#client_id = os.environ.get('NAVER_CLIENT_ID')
#client_secret = os.environ.get('NAVER_CLIENT_SECRET')
#client_apik = os.environ.get('CLOVA_API_KEY')
#client_api_primal = os.environ.get('CLOVA_API_KEY_PRIMARY_VAL')
#client_required = os.environ.get('CLOVA_REQUEST_ID')
client_id = st.secrets['NAVER_CLIENT_ID']
client_secret = st.secrets['NAVER_CLIENT_SECRET']
client_api = st.secrets['CLOVA_API_KEY']
client_api_primal = st.secrets['CLOVA_API_KEY_PRIMARY_VAL']
client_required = st.secrets['CLOVA_REQUEST_ID']

class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }  
        responses = requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                           headers=headers, json=completion_request, stream=True)
        final_summary = ""
        for line in responses.iter_lines():
            if line:
                try:
                    line_data = line.decode("utf-8")
                    # Extract JSON data after "data:"
                    if line_data.startswith("data:"):
                        data = json.loads(line_data[5:])
                        # Collect "content" field from "message" role
                        if "message" in data and data["message"]["role"] == "assistant":
                            content = data["message"].get("content", "")
                            final_summary += content
                        # Check for the final result event
                        if data.get("event") == "result":
                            return data["message"]["content"]
                except json.JSONDecodeError:
                    continue
        return final_summary.strip()

def search_news(query="계엄", display=6):
    encoded_query = query
    url = f"https://openapi.naver.com/v1/search/news.json?query={encoded_query}&display={display}"
    headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        items = response.json().get('items', [])
        for item in items:
            # HTML tag delete (<b>, </b>)
            item['title'] = re.sub(r'<\/?b>', '', item['title'])
            item['description'] = re.sub(r'<\/?b>', '', item['description'])
        return items
    else:
        st.error(f"Failed to search news. Status code: {response.status_code}")
        return []
    
st.title("What's happening in Korea? News related to martial law")
st.write("On December 2, 2024, the President of South Korea declared martial law. In response, I created AI-powered service to provide real-time summaries of news related to the crisis from South Korea’s largest portal, NAVER, to inform the global audience accurately. This initiative aims to show that peace and love can triumph over violence, and invites support or inquiries at stormkingrank1@gmail.com.")
# Click button restricted #3
#if st.button("Search"):
#    if st.session_state['search_count'] < 3:
#        st.session_state['search_count'] += 1
#        news_items = search_news()
#        for item in news_items:
#            #st.subheader(item['title'])
#            #st.write(item['description'])
#            newsitems = item['title']+item['description']
#            result = completion_executor.execute(request_data)
#            st.write("Summary:", result)
#            st.write(f"[Original Article]({item['link']})")
#    else:
#        st.warning("You have reached the maximum number of searches (3).")
if __name__ == '__main__':
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key= client_api,
        api_key_primary_val=client_api_primal,
        request_id=client_required
        )
if 'search_count' not in st.session_state:
    st.session_state['search_count'] = 0
if st.button("Search"):
    if st.session_state['search_count'] < 3:
        st.session_state['search_count'] += 1        
        news_items = search_news()

        for item in news_items:
            describe = item['description']
            preset_text = [{"role":"system","content":"- 당신은 텍스트 요약 어시스턴트입니다.\n- 주어진 텍스트의 내용을 분석하여 간결하고 명확한 3줄 요약을 제공합니다.\n- 다음 지침을 엄격히 준수하여 업무를 수행하십시오.\n- 주어진 텍스트의 전체적인 맥락과 주제를 파악합니다.\n- 먼저 기사 제목을 영어로 번역해 제공합니다.\n- 불필요한 세부사항은 제외하고 간결하고 명확한 문장으로 요약을 작성하세요.\n-  모든 응답은 반드시 영어로 제공하세요.\n- 원문의 핵심을 정확히 반영하는 효과적인 요약을 만들어주세요.\n- 위의 지침을 철저히 따라 고품질의 텍스트 요약을 3줄로 제공합니다.\n###형식\n[TITLE]\n[content]\n###끝"},{"role":"user","content":describe}]
            request_data = {
                'messages': preset_text,
                'topP': 0.8,
                'topK': 0,
                'maxTokens': 512,
                'temperature': 0.1,
                'repeatPenalty': 1.2,
                'stopBefore': [],
                'includeAiFilters': True,
                'seed': 0
            }       
            
            resultation = completion_executor.execute(request_data)
            st.write("Summary:", resultation)
            st.write(f"[Original Article]({item['link']})")
    else:
        st.warning("You have reached the maximum number of searches (3).")
# Streamlit 애플리케이션
