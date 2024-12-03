import streamlit as st
import requests
from transformers import pipeline

# 네이버 API 정보
CLIENT_ID = "YOUR_NAVER_CLIENT_ID"
CLIENT_SECRET = "YOUR_NAVER_CLIENT_SECRET"
NAVER_SEARCH_URL = "https://openapi.naver.com/v1/search/news.json"

# Summarization pipeline 설정 (Hugging Face 모델 사용)
summarizer = pipeline("summarization")

def fetch_naver_news(query, display=5):
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET,
    }
    params = {"query": query, "display": display, "sort": "sim"}
    
    response = requests.get(NAVER_SEARCH_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        st.error(f"Error: {response.status_code}")
        return []

def summarize_text(text, max_length=100):
    summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def main():
    st.title("Naver News Summarizer")
    
    query = "계엄령"  # 검색어 설정
    st.subheader(f"'{query}' 관련 뉴스 요약")
    
    news_items = fetch_naver_news(query)
    
    if news_items:
        for news in news_items:
            st.markdown(f"### [{news['title']}]({news['link']})")
            description = news['description']
            summary = summarize_text(description)
            st.write(summary)
            st.write("---")
    else:
        st.write("뉴스를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
 
