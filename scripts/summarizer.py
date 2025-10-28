#!/usr/bin/env python3
"""
뉴스 요약기
OpenAI API를 사용하여 뉴스를 요약합니다.
"""

import openai
import json
import os
import sys
from datetime import datetime
from typing import List, Dict

class NewsSummarizer:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    def load_news_data(self) -> Dict:
        """뉴스 데이터 로드"""
        news_path = os.path.join(self.base_dir, 'data', 'news.json')
        
        try:
            with open(news_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("News data file not found. Please run crawler.py first.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error parsing news data: {e}")
            sys.exit(1)
    
    def summarize_individual_news(self, news_item: Dict) -> str:
        """개별 뉴스 요약"""
        try:
            title = news_item.get('title', '')
            content = news_item.get('content', '')
            
            if not content:
                return f"제목: {title}\n\n상세 내용을 불러올 수 없습니다."
            
            prompt = f"""
다음 경제 뉴스를 3-4문장으로 요약해주세요. 핵심 내용과 시사점을 포함하여 작성해주세요.

제목: {title}

내용: {content}

요약:
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 경제 뉴스 전문 요약가입니다. 핵심 내용을 간결하고 명확하게 요약해주세요."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error summarizing news item: {e}")
            return f"제목: {title}\n\n요약 생성 중 오류가 발생했습니다."
    
    def create_daily_summary(self, news_list: List[Dict]) -> str:
        """오늘의 경제 이슈 5문장 요약 생성"""
        try:
            # 뉴스 제목들을 하나의 텍스트로 결합
            news_titles = [news.get('title', '') for news in news_list[:10]]
            news_text = "\n".join([f"- {title}" for title in news_titles if title])
            
            prompt = f"""
다음은 오늘의 주요 경제 뉴스 제목들입니다. 이를 바탕으로 오늘의 경제 이슈를 5문장으로 요약해주세요.
각 문장은 핵심 이슈를 다루며, 전체적인 경제 동향을 파악할 수 있도록 작성해주세요.

뉴스 제목들:
{news_text}

오늘의 경제 이슈 요약:
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 경제 전문가입니다. 오늘의 경제 이슈를 5문장으로 간결하고 명확하게 요약해주세요."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error creating daily summary: {e}")
            return "오늘의 경제 이슈 요약을 생성할 수 없습니다. 잠시 후 다시 시도해주세요."
    
    def process_all_news(self):
        """모든 뉴스 처리 및 요약"""
        print("Loading news data...")
        news_data = self.load_news_data()
        
        if not news_data.get('news'):
            print("No news data found.")
            return
        
        print(f"Processing {len(news_data['news'])} news items...")
        
        # 개별 뉴스 요약
        for i, news_item in enumerate(news_data['news']):
            print(f"Summarizing news {i+1}/{len(news_data['news'])}: {news_item.get('title', '')[:50]}...")
            
            summary = self.summarize_individual_news(news_item)
            news_item['summary'] = summary
            
            # API 호출 간격 조절
            import time
            time.sleep(1)
        
        # 오늘의 경제 이슈 요약 생성
        print("Creating daily summary...")
        daily_summary = self.create_daily_summary(news_data['news'])
        
        # 요약된 데이터 저장
        updated_data = {
            'lastUpdated': datetime.now().isoformat(),
            'summary': daily_summary,
            'news': news_data['news'],
            'count': len(news_data['news'])
        }
        
        self.save_summarized_data(updated_data)
        print("News summarization completed successfully!")
    
    def save_summarized_data(self, data: Dict):
        """요약된 데이터 저장"""
        output_path = os.path.join(self.base_dir, 'data', 'news.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Summarized data saved to {output_path}")

def main():
    # OpenAI API 키 확인
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set your OpenAI API key in GitHub Secrets.")
        sys.exit(1)
    
    summarizer = NewsSummarizer()
    
    try:
        summarizer.process_all_news()
    except Exception as e:
        print(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
