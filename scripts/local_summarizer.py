#!/usr/bin/env python3
"""
로컬 요약 생성기
OpenAI API 없이도 작동하는 로컬 요약 시스템
"""

import json
import os
import re
from datetime import datetime
from typing import List, Dict

class LocalSummarizer:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    def load_news_data(self):
        """뉴스 데이터 로드"""
        news_path = os.path.join(self.base_dir, 'data', 'news.json')
        try:
            with open(news_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading news data: {e}")
            return None
    
    def extract_keywords(self, text):
        """텍스트에서 키워드 추출"""
        economy_keywords = {
            '주식시장': ['주가', '코스피', '코스닥', '증시', '주식', '투자', '증권', 'ETF', '펀드'],
            '부동산': ['부동산', '아파트', '주택', '매매', '임대', '전세', '월세', '재개발', '재건축'],
            '금리정책': ['금리', '중앙은행', '한국은행', '기준금리', '인플레이션', '물가'],
            '경기동향': ['경기', '성장', 'GDP', '경제', '회복', '부진', '호황', '침체'],
            '국제정치': ['APEC', '정상회의', '미국', '중국', '일본', '외교', '무역'],
            '기업': ['삼성', 'LG', 'SK', '현대', '기업', '매출', '수익', '실적'],
            '고용': ['고용', '취업', '실업', '구직', '채용', '노동']
        }
        
        found_keywords = []
        text_lower = text.lower()
        
        for category, keywords in economy_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_keywords.append(category)
                    break
        
        return list(set(found_keywords))
    
    def generate_news_summary(self, news_item):
        """개별 뉴스 요약 생성"""
        title = news_item.get('title', '')
        content = news_item.get('content', '')
        
        # 제목에서 핵심 정보 추출
        summary_parts = []
        
        # 키워드 기반 요약
        keywords = self.extract_keywords(title + ' ' + content)
        
        if '주식시장' in keywords:
            if '코스피' in title or '증시' in title:
                summary_parts.append("주식시장이 상승세를 보이고 있습니다.")
            else:
                summary_parts.append("주식시장 관련 뉴스가 주목받고 있습니다.")
        
        if '부동산' in keywords:
            if '정책' in title or '공급' in title:
                summary_parts.append("부동산 정책 관련 발표가 있었습니다.")
            else:
                summary_parts.append("부동산 시장 동향이 관심을 끌고 있습니다.")
        
        if '금리정책' in keywords:
            summary_parts.append("금리 정책 관련 소식이 전해졌습니다.")
        
        if '경기동향' in keywords:
            if '회복' in title or '성장' in title:
                summary_parts.append("경기 회복 신호가 나타나고 있습니다.")
            else:
                summary_parts.append("경제 동향에 대한 관심이 높아지고 있습니다.")
        
        if '국제정치' in keywords:
            summary_parts.append("국제 정치 경제 이슈가 주목받고 있습니다.")
        
        # 기본 요약이 없으면 제목 기반으로 생성
        if not summary_parts:
            if len(title) > 50:
                summary_parts.append(f"{title[:50]}...")
            else:
                summary_parts.append(title)
        
        return " ".join(summary_parts)
    
    def generate_daily_summary(self, news_list):
        """일일 요약 생성"""
        if not news_list:
            return "오늘의 경제 이슈를 불러올 수 없습니다."
        
        # 전체 키워드 수집
        all_keywords = []
        for news in news_list:
            keywords = self.extract_keywords(news['title'] + ' ' + news['content'])
            all_keywords.extend(keywords)
        
        # 키워드 빈도 계산
        keyword_counts = {}
        for keyword in all_keywords:
            keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        # 상위 키워드 선택
        top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        top_keyword_names = [kw[0] for kw in top_keywords]
        
        # 요약 생성
        summary_parts = []
        
        if top_keyword_names:
            summary_parts.append(f"📈 **오늘의 주요 경제 이슈**")
            summary_parts.append("")
            summary_parts.append(f"주요 관심사: {', '.join(top_keyword_names)}")
            summary_parts.append("")
        
        summary_parts.append("**주요 뉴스:**")
        
        for i, news in enumerate(news_list[:5], 1):
            title = news['title']
            if len(title) > 60:
                title = title[:60] + "..."
            summary_parts.append(f"{i}. {title}")
        
        return "\n".join(summary_parts)
    
    def process_news(self):
        """뉴스 처리 및 요약 생성"""
        print("Loading news data...")
        data = self.load_news_data()
        
        if not data or 'news' not in data:
            print("No news data found.")
            return
        
        news_list = data['news']
        print(f"Processing {len(news_list)} news items...")
        
        # 개별 뉴스 요약 생성
        for i, news in enumerate(news_list, 1):
            print(f"Summarizing news {i}/{len(news_list)}: {news['title'][:50]}...")
            summary = self.generate_news_summary(news)
            news['summary'] = summary
        
        # 일일 요약 생성
        print("Creating daily summary...")
        daily_summary = self.generate_daily_summary(news_list)
        
        # 데이터 업데이트
        data['summary'] = daily_summary
        data['lastUpdated'] = datetime.now().isoformat()
        
        # 저장
        output_path = os.path.join(self.base_dir, 'data', 'news.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Summarized data saved to {output_path}")
        print("Local summarization completed successfully!")

def main():
    summarizer = LocalSummarizer()
    summarizer.process_news()

if __name__ == "__main__":
    main()
