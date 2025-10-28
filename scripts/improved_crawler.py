#!/usr/bin/env python3
"""
개선된 경제 뉴스 크롤러
실제 최신 뉴스를 크롤링할 수 있도록 개선된 버전
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

class ImprovedNewsCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        # SSL 검증 우회 (개발/테스트 환경에서만)
        self.session.verify = False
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.news_data = []
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    def crawl_naver_news(self):
        """네이버 뉴스 경제 섹션 크롤링 (개선된 버전)"""
        try:
            # 네이버 뉴스 경제 섹션 URL
            url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            news_items = []
            
            # 다양한 선택자로 뉴스 링크 찾기
            selectors = [
                'a[href*="/read.naver?mode=LSD"]',
                'a[href*="/article/"]',
                '.cluster_group a',
                '.list_body a',
                '.news_area a'
            ]
            
            for selector in selectors:
                links = soup.select(selector)
                for link in links[:10]:  # 각 선택자에서 최대 10개
                    href = link.get('href')
                    if href and ('/read.naver' in href or '/article/' in href):
                        title = link.get_text(strip=True)
                        if title and len(title) > 10 and '경제' in title:
                            full_url = urljoin(url, href)
                            news_items.append({
                                'title': title,
                                'url': full_url,
                                'source': '네이버뉴스'
                            })
            
            # 중복 제거
            seen_urls = set()
            unique_items = []
            for item in news_items:
                if item['url'] not in seen_urls:
                    seen_urls.add(item['url'])
                    unique_items.append(item)
            
            # 상세 내용 크롤링
            for item in unique_items[:5]:  # 최대 5개만
                try:
                    detail_response = self.session.get(item['url'], timeout=10)
                    detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                    
                    # 본문 추출 (다양한 선택자 시도)
                    content_selectors = [
                        '#newsct_article',
                        '.news_end_body',
                        '.article_body',
                        '.news_body',
                        '.article_view'
                    ]
                    
                    content = ""
                    for selector in content_selectors:
                        content_elem = detail_soup.select_one(selector)
                        if content_elem:
                            content = content_elem.get_text(strip=True)
                            break
                    
                    if content:
                        item['content'] = content[:800]  # 800자로 제한
                    else:
                        item['content'] = item['title']  # 제목을 내용으로 사용
                    
                    # 발행시간 추출
                    time_selectors = [
                        '.t11',
                        '.author em',
                        '.info_group .t11',
                        '.press_logo .t11'
                    ]
                    
                    published_at = datetime.now().isoformat()
                    for selector in time_selectors:
                        time_elem = detail_soup.select_one(selector)
                        if time_elem:
                            time_text = time_elem.get_text(strip=True)
                            published_at = self.parse_naver_time(time_text)
                            break
                    
                    item['publishedAt'] = published_at
                    item['category'] = '경제'
                    
                    time.sleep(1)  # 요청 간격 조절
                    
                except Exception as e:
                    print(f"Error crawling detail for {item['url']}: {e}")
                    item['content'] = item['title']
                    item['publishedAt'] = datetime.now().isoformat()
                    item['category'] = '경제'
            
            return unique_items[:5]
            
        except Exception as e:
            print(f"Error crawling Naver news: {e}")
            return []
    
    def crawl_hankyung_news(self):
        """한국경제신문 크롤링 (개선된 버전)"""
        try:
            url = "https://www.hankyung.com/economy"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            news_items = []
            
            # 다양한 선택자로 뉴스 링크 찾기
            selectors = [
                'a[href*="/article/"]',
                '.news_list a',
                '.list_news a',
                '.article_list a'
            ]
            
            for selector in selectors:
                links = soup.select(selector)
                for link in links[:10]:
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
            
            # 중복 제거
            seen_urls = set()
            unique_items = []
            for item in news_items:
                if item['url'] not in seen_urls:
                    seen_urls.add(item['url'])
                    unique_items.append(item)
            
            # 상세 내용 크롤링
            for item in unique_items[:3]:  # 최대 3개만
                try:
                    detail_response = self.session.get(item['url'], timeout=10)
                    detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                    
                    # 본문 추출
                    content_elem = detail_soup.select_one('.article-body, .news-body, .article_view')
                    if content_elem:
                        content = content_elem.get_text(strip=True)
                        item['content'] = content[:800]
                    else:
                        item['content'] = item['title']
                    
                    # 발행시간 추출
                    time_elem = detail_soup.select_one('time, .date, .publish-time')
                    if time_elem:
                        time_text = time_elem.get_text(strip=True)
                        item['publishedAt'] = self.parse_time(time_text)
                    else:
                        item['publishedAt'] = datetime.now().isoformat()
                    
                    item['category'] = '경제'
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error crawling detail for {item['url']}: {e}")
                    item['content'] = item['title']
                    item['publishedAt'] = datetime.now().isoformat()
                    item['category'] = '경제'
            
            return unique_items[:3]
            
        except Exception as e:
            print(f"Error crawling Hankyung news: {e}")
            return []
    
    def crawl_mk_news(self):
        """매일경제신문 크롤링 (개선된 버전)"""
        try:
            url = "https://www.mk.co.kr/news/economy/"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            news_items = []
            
            # 다양한 선택자로 뉴스 링크 찾기
            selectors = [
                'a[href*="/news/economy/"]',
                '.news_list a',
                '.list_news a',
                '.article_list a'
            ]
            
            for selector in selectors:
                links = soup.select(selector)
                for link in links[:10]:
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
            
            # 중복 제거
            seen_urls = set()
            unique_items = []
            for item in news_items:
                if item['url'] not in seen_urls:
                    seen_urls.add(item['url'])
                    unique_items.append(item)
            
            # 상세 내용 크롤링
            for item in unique_items[:3]:  # 최대 3개만
                try:
                    detail_response = self.session.get(item['url'], timeout=10)
                    detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                    
                    # 본문 추출
                    content_elem = detail_soup.select_one('.news_cnt_detail_wrap, .article_body, .news_body')
                    if content_elem:
                        content = content_elem.get_text(strip=True)
                        item['content'] = content[:800]
                    else:
                        item['content'] = item['title']
                    
                    # 발행시간 추출
                    time_elem = detail_soup.select_one('.time, .date, .publish-time')
                    if time_elem:
                        time_text = time_elem.get_text(strip=True)
                        item['publishedAt'] = self.parse_time(time_text)
                    else:
                        item['publishedAt'] = datetime.now().isoformat()
                    
                    item['category'] = '경제'
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error crawling detail for {item['url']}: {e}")
                    item['content'] = item['title']
                    item['publishedAt'] = datetime.now().isoformat()
                    item['category'] = '경제'
            
            return unique_items[:3]
            
        except Exception as e:
            print(f"Error crawling MK news: {e}")
            return []
    
    def crawl_yna_news(self):
        """연합뉴스 경제 섹션 크롤링 (개선된 버전)"""
        try:
            url = "https://www.yna.co.kr/economy"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            news_items = []
            
            # 다양한 선택자로 뉴스 링크 찾기
            selectors = [
                'a[href*="/economy/"]',
                '.news_list a',
                '.list_news a',
                '.article_list a'
            ]
            
            for selector in selectors:
                links = soup.select(selector)
                for link in links[:10]:
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
            
            # 중복 제거
            seen_urls = set()
            unique_items = []
            for item in news_items:
                if item['url'] not in seen_urls:
                    seen_urls.add(item['url'])
                    unique_items.append(item)
            
            # 상세 내용 크롤링
            for item in unique_items[:3]:  # 최대 3개만
                try:
                    detail_response = self.session.get(item['url'], timeout=10)
                    detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
                    
                    # 본문 추출
                    content_elem = detail_soup.select_one('.story-news, .article_body, .news_body')
                    if content_elem:
                        content = content_elem.get_text(strip=True)
                        item['content'] = content[:800]
                    else:
                        item['content'] = item['title']
                    
                    # 발행시간 추출
                    time_elem = detail_soup.select_one('.publish-time, .date, time')
                    if time_elem:
                        time_text = time_elem.get_text(strip=True)
                        item['publishedAt'] = self.parse_time(time_text)
                    else:
                        item['publishedAt'] = datetime.now().isoformat()
                    
                    item['category'] = '경제'
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error crawling detail for {item['url']}: {e}")
                    item['content'] = item['title']
                    item['publishedAt'] = datetime.now().isoformat()
                    item['category'] = '경제'
            
            return unique_items[:3]
            
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
            elif '일 전' in time_str:
                days = int(re.search(r'(\d+)일', time_str).group(1))
                return (now - timedelta(days=days)).isoformat()
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
        print("Starting improved news crawling...")
        
        all_news = []
        
        # 각 소스에서 뉴스 수집
        print("Crawling Naver news...")
        naver_news = self.crawl_naver_news()
        all_news.extend(naver_news)
        print(f"Found {len(naver_news)} Naver news items")
        
        print("Crawling Hankyung news...")
        hankyung_news = self.crawl_hankyung_news()
        all_news.extend(hankyung_news)
        print(f"Found {len(hankyung_news)} Hankyung news items")
        
        print("Crawling MK news...")
        mk_news = self.crawl_mk_news()
        all_news.extend(mk_news)
        print(f"Found {len(mk_news)} MK news items")
        
        print("Crawling YNA news...")
        yna_news = self.crawl_yna_news()
        all_news.extend(yna_news)
        print(f"Found {len(yna_news)} YNA news items")
        
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
    crawler = ImprovedNewsCrawler()
    
    try:
        # 뉴스 크롤링
        news_data = crawler.crawl_all_news()
        
        # JSON 파일로 저장
        crawler.save_to_json()
        
        print("Improved news crawling completed successfully!")
        
    except Exception as e:
        print(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
