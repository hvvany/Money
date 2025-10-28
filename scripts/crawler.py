#!/usr/bin/env python3
"""
경제 뉴스 크롤러
네이버, 한국경제, 매일경제, 연합뉴스에서 경제 뉴스를 수집합니다.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
import os
import sys

class NewsCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        # SSL 검증 우회 (개발/테스트 환경에서만)
        self.session.verify = False
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.news_data = []
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    def crawl_naver_news(self):
        """네이버 뉴스 경제 섹션 크롤링"""
        try:
            url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            news_items = []
            
            # 메인 뉴스 섹션
            main_news = soup.find_all('div', class_='cluster_group')
            
            for group in main_news[:3]:  # 상위 3개 그룹만
                links = group.find_all('a', href=True)
                for link in links[:3]:  # 각 그룹에서 3개씩
                    if link.get('href') and 'news.naver.com' in link.get('href'):
                        title = link.get_text(strip=True)
                        if title and len(title) > 10:
                            news_items.append({
                                'title': title,
                                'url': link.get('href'),
                                'source': '네이버뉴스'
                            })
            
            # 상세 내용 크롤링
            for item in news_items[:10]:
                try:
                    detail_response = self.session.get(item['url'], timeout=10)
                    detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                    
                    # 본문 추출
                    content_div = detail_soup.find('div', {'id': 'newsct_article'})
                    if content_div:
                        content = content_div.get_text(strip=True)
                        item['content'] = content[:500]  # 500자로 제한
                    
                    # 발행시간 추출
                    time_elem = detail_soup.find('span', class_='t11')
                    if time_elem:
                        item['publishedAt'] = self.parse_naver_time(time_elem.get_text())
                    else:
                        item['publishedAt'] = datetime.now().isoformat()
                    
                    time.sleep(1)  # 요청 간격 조절
                    
                except Exception as e:
                    print(f"Error crawling detail for {item['url']}: {e}")
                    item['content'] = ""
                    item['publishedAt'] = datetime.now().isoformat()
            
            return news_items[:10]
            
        except Exception as e:
            print(f"Error crawling Naver news: {e}")
            return []
    
    def crawl_hankyung_news(self):
        """한국경제신문 크롤링"""
        try:
            url = "https://www.hankyung.com/economy"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            news_items = []
            
            # 뉴스 링크 추출
            news_links = soup.find_all('a', href=True)
            
            for link in news_links[:20]:
                href = link.get('href')
                if href and '/article/' in href:
                    title = link.get_text(strip=True)
                    if title and len(title) > 10:
                        full_url = urljoin(url, href)
                        news_items.append({
                            'title': title,
                            'url': full_url,
                            'source': '한국경제'
                        })
            
            # 상세 내용 크롤링
            for item in news_items[:10]:
                try:
                    detail_response = self.session.get(item['url'], timeout=10)
                    detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                    
                    # 본문 추출
                    content_div = detail_soup.find('div', class_='article-body')
                    if content_div:
                        content = content_div.get_text(strip=True)
                        item['content'] = content[:500]
                    
                    # 발행시간 추출
                    time_elem = detail_soup.find('time')
                    if time_elem:
                        item['publishedAt'] = self.parse_time(time_elem.get('datetime'))
                    else:
                        item['publishedAt'] = datetime.now().isoformat()
                    
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error crawling detail for {item['url']}: {e}")
                    item['content'] = ""
                    item['publishedAt'] = datetime.now().isoformat()
            
            return news_items[:10]
            
        except Exception as e:
            print(f"Error crawling Hankyung news: {e}")
            return []
    
    def crawl_mk_news(self):
        """매일경제신문 크롤링"""
        try:
            url = "https://www.mk.co.kr/news/economy/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            news_items = []
            
            # 뉴스 링크 추출
            news_links = soup.find_all('a', href=True)
            
            for link in news_links[:20]:
                href = link.get('href')
                if href and '/news/economy/' in href and 'view' in href:
                    title = link.get_text(strip=True)
                    if title and len(title) > 10:
                        full_url = urljoin(url, href)
                        news_items.append({
                            'title': title,
                            'url': full_url,
                            'source': '매일경제'
                        })
            
            # 상세 내용 크롤링
            for item in news_items[:10]:
                try:
                    detail_response = self.session.get(item['url'], timeout=10)
                    detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                    
                    # 본문 추출
                    content_div = detail_soup.find('div', class_='news_cnt_detail_wrap')
                    if content_div:
                        content = content_div.get_text(strip=True)
                        item['content'] = content[:500]
                    
                    # 발행시간 추출
                    time_elem = detail_soup.find('span', class_='time')
                    if time_elem:
                        item['publishedAt'] = self.parse_time(time_elem.get_text())
                    else:
                        item['publishedAt'] = datetime.now().isoformat()
                    
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error crawling detail for {item['url']}: {e}")
                    item['content'] = ""
                    item['publishedAt'] = datetime.now().isoformat()
            
            return news_items[:10]
            
        except Exception as e:
            print(f"Error crawling MK news: {e}")
            return []
    
    def crawl_yna_news(self):
        """연합뉴스 경제 섹션 크롤링"""
        try:
            url = "https://www.yna.co.kr/economy"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            news_items = []
            
            # 뉴스 링크 추출
            news_links = soup.find_all('a', href=True)
            
            for link in news_links[:20]:
                href = link.get('href')
                if href and '/economy/' in href and 'view' in href:
                    title = link.get_text(strip=True)
                    if title and len(title) > 10:
                        full_url = urljoin(url, href)
                        news_items.append({
                            'title': title,
                            'url': full_url,
                            'source': '연합뉴스'
                        })
            
            # 상세 내용 크롤링
            for item in news_items[:10]:
                try:
                    detail_response = self.session.get(item['url'], timeout=10)
                    detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                    
                    # 본문 추출
                    content_div = detail_soup.find('div', class_='story-news')
                    if content_div:
                        content = content_div.get_text(strip=True)
                        item['content'] = content[:500]
                    
                    # 발행시간 추출
                    time_elem = detail_soup.find('span', class_='publish-time')
                    if time_elem:
                        item['publishedAt'] = self.parse_time(time_elem.get_text())
                    else:
                        item['publishedAt'] = datetime.now().isoformat()
                    
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error crawling detail for {item['url']}: {e}")
                    item['content'] = ""
                    item['publishedAt'] = datetime.now().isoformat()
            
            return news_items[:10]
            
        except Exception as e:
            print(f"Error crawling YNA news: {e}")
            return []
    
    def parse_naver_time(self, time_str):
        """네이버 시간 형식 파싱"""
        try:
            now = datetime.now()
            if '분 전' in time_str:
                minutes = int(re.search(r'(\d+)분', time_str).group(1))
                return (now - timedelta(minutes=minutes)).isoformat()
            elif '시간 전' in time_str:
                hours = int(re.search(r'(\d+)시간', time_str).group(1))
                return (now - timedelta(hours=hours)).isoformat()
            else:
                return now.isoformat()
        except:
            return datetime.now().isoformat()
    
    def parse_time(self, time_str):
        """일반적인 시간 형식 파싱"""
        try:
            # ISO 형식인 경우
            if 'T' in time_str:
                return datetime.fromisoformat(time_str.replace('Z', '+00:00')).isoformat()
            # 한국 시간 형식인 경우
            elif re.match(r'\d{4}-\d{2}-\d{2}', time_str):
                return datetime.strptime(time_str, '%Y-%m-%d').isoformat()
            else:
                return datetime.now().isoformat()
        except:
            return datetime.now().isoformat()
    
    def remove_duplicates(self, news_list):
        """중복 뉴스 제거"""
        seen_titles = set()
        unique_news = []
        
        for news in news_list:
            title = news['title'].strip()
            if title not in seen_titles and len(title) > 10:
                seen_titles.add(title)
                unique_news.append(news)
        
        return unique_news
    
    def crawl_all_news(self):
        """모든 뉴스 소스에서 뉴스 수집"""
        print("Starting news crawling...")
        
        all_news = []
        
        # 각 소스에서 뉴스 수집
        print("Crawling Naver news...")
        all_news.extend(self.crawl_naver_news())
        
        print("Crawling Hankyung news...")
        all_news.extend(self.crawl_hankyung_news())
        
        print("Crawling MK news...")
        all_news.extend(self.crawl_mk_news())
        
        print("Crawling YNA news...")
        all_news.extend(self.crawl_yna_news())
        
        # 중복 제거
        print("Removing duplicates...")
        unique_news = self.remove_duplicates(all_news)
        
        # 최신 10개 선택
        unique_news.sort(key=lambda x: x.get('publishedAt', ''), reverse=True)
        self.news_data = unique_news[:10]
        
        print(f"Collected {len(self.news_data)} unique news items")
        return self.news_data
    
    def save_to_json(self):
        """뉴스 데이터를 JSON 파일로 저장"""
        data = {
            'lastUpdated': datetime.now().isoformat(),
            'news': self.news_data,
            'count': len(self.news_data)
        }
        
        output_path = os.path.join(self.base_dir, 'data', 'news.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"News data saved to {output_path}")

def main():
    crawler = NewsCrawler()
    
    try:
        # 뉴스 크롤링
        news_data = crawler.crawl_all_news()
        
        # JSON 파일로 저장
        crawler.save_to_json()
        
        print("News crawling completed successfully!")
        
    except Exception as e:
        print(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
