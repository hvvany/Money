#!/usr/bin/env python3
"""
샘플 데이터 생성기
테스트를 위한 샘플 뉴스 및 경제상식 데이터를 생성합니다.
"""

import json
import os
from datetime import datetime, timedelta
import random

class SampleDataGenerator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    def create_sample_news(self):
        """샘플 뉴스 데이터 생성"""
        sample_news = [
            {
                "title": "코스피 3일 연속 상승, 2,500선 돌파",
                "content": "코스피가 3일 연속 상승세를 이어가며 2,500선을 돌파했습니다. 외국인 투자자들의 순매수세가 지속되면서 상승 모멘텀이 강화되고 있습니다.",
                "summary": "코스피가 3일 연속 상승하며 2,500선을 돌파했습니다. 외국인 투자자들의 순매수세가 지속되어 상승 모멘텀이 강화되고 있습니다.",
                "source": "네이버뉴스",
                "url": "https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=101&oid=001&aid=0001234567",
                "publishedAt": (datetime.now() - timedelta(hours=2)).isoformat(),
                "category": "경제"
            },
            {
                "title": "한국은행 기준금리 3.5% 동결 결정",
                "content": "한국은행이 금융통화위원회를 통해 기준금리를 3.5%로 동결하기로 결정했습니다. 인플레이션 안정화와 경제 성장의 균형을 고려한 결정으로 평가됩니다.",
                "summary": "한국은행이 기준금리를 3.5%로 동결하기로 결정했습니다. 인플레이션 안정화와 경제 성장의 균형을 고려한 결정입니다.",
                "source": "한국경제",
                "url": "https://www.hankyung.com/economy/article/2024010100001",
                "publishedAt": (datetime.now() - timedelta(hours=4)).isoformat(),
                "category": "경제"
            },
            {
                "title": "원달러 환율 1,320원대 하락",
                "content": "원달러 환율이 1,320원대까지 하락했습니다. 미 연준의 금리 인하 기대감과 달러 약세가 원화 강세를 이끌고 있습니다.",
                "summary": "원달러 환율이 1,320원대까지 하락했습니다. 미 연준의 금리 인하 기대감과 달러 약세가 원화 강세를 이끌고 있습니다.",
                "source": "매일경제",
                "url": "https://www.mk.co.kr/news/economy/2024/01/01/1234567",
                "publishedAt": (datetime.now() - timedelta(hours=6)).isoformat(),
                "category": "경제"
            },
            {
                "title": "삼성전자 주가 5% 상승, 반도체 회복 기대감",
                "content": "삼성전자 주가가 5% 상승했습니다. 반도체 업황 회복 기대감과 AI 관련 수요 증가가 주가 상승을 이끌고 있습니다.",
                "summary": "삼성전자 주가가 5% 상승했습니다. 반도체 업황 회복 기대감과 AI 관련 수요 증가가 주가 상승을 이끌고 있습니다.",
                "source": "연합뉴스",
                "url": "https://www.yna.co.kr/view/AKR20240101000100001",
                "publishedAt": (datetime.now() - timedelta(hours=8)).isoformat(),
                "category": "경제"
            },
            {
                "title": "부동산 시장 거래량 증가세 지속",
                "content": "부동산 시장에서 거래량이 증가세를 보이고 있습니다. 정부의 규제 완화 정책과 금리 안정화가 시장 활성화에 기여하고 있습니다.",
                "summary": "부동산 시장에서 거래량이 증가세를 보이고 있습니다. 정부의 규제 완화 정책과 금리 안정화가 시장 활성화에 기여하고 있습니다.",
                "source": "네이버뉴스",
                "url": "https://news.naver.com/main/read.naver?mode=LSD&mid=shm&sid1=101&oid=421&aid=0001234567",
                "publishedAt": (datetime.now() - timedelta(hours=10)).isoformat(),
                "category": "경제"
            }
        ]
        
        # 오늘의 경제 이슈 요약 생성
        summary = """오늘의 주요 경제 이슈는 다음과 같습니다. 코스피가 3일 연속 상승세를 이어가며 2,500선을 돌파했습니다. 한국은행이 기준금리를 3.5%로 동결하기로 결정하여 인플레이션 안정화와 경제 성장의 균형을 도모하고 있습니다. 원달러 환율이 1,320원대까지 하락하며 미 연준의 금리 인하 기대감이 원화 강세를 이끌고 있습니다. 삼성전자 주가가 5% 상승하며 반도체 업황 회복 기대감이 높아지고 있습니다. 부동산 시장에서도 거래량 증가세가 지속되어 시장 활성화가 이루어지고 있습니다."""
        
        news_data = {
            "lastUpdated": datetime.now().isoformat(),
            "summary": summary,
            "news": sample_news,
            "count": len(sample_news)
        }
        
        return news_data
    
    def create_sample_finance_tips(self):
        """샘플 경제상식 데이터 생성"""
        sample_tips = [
            {
                "id": 1,
                "category": "연금저축",
                "title": "연금저축이란?",
                "content": "연금저축은 노후 준비를 위한 장기 저축 상품입니다. 매년 400만원까지 세제혜택을 받으며 납입할 수 있고, 55세 이후 연금으로 수령하거나 일시금으로 받을 수 있습니다. 개인연금저축(IRP)과 퇴직연금(401k) 등이 있으며, 장기간 꾸준히 납입할수록 더 큰 혜택을 받을 수 있습니다.",
                "keywords": ["연금저축", "개인연금", "퇴직연금", "IRP", "연금보험"],
                "createdAt": datetime.now().isoformat()
            },
            {
                "id": 2,
                "category": "주식",
                "title": "주식 투자 기초",
                "content": "주식은 기업의 일부를 소유하는 증권으로, 기업의 성장과 함께 주가가 상승할 가능성이 있습니다. 코스피와 코스닥 시장에서 거래되며, 배당을 통해 수익을 얻을 수도 있습니다. 하지만 주가는 변동성이 크므로 투자 전 충분한 분석과 리스크 관리가 필요합니다.",
                "keywords": ["주식", "주식투자", "증권", "코스피", "코스닥", "ETF"],
                "createdAt": datetime.now().isoformat()
            },
            {
                "id": 3,
                "category": "ISA",
                "title": "ISA (개인종합자산관리계좌)",
                "content": "ISA는 다양한 금융상품을 하나의 계좌에서 관리할 수 있는 통합 투자계좌입니다. 연간 2천만원까지 투자할 수 있으며, 3년 이상 보유 시 세제혜택을 받을 수 있습니다. 주식, 채권, 펀드, ETF 등 다양한 상품에 투자할 수 있어 포트폴리오 분산투자에 유리합니다.",
                "keywords": ["ISA", "개인종합자산관리계좌", "세제혜택", "투자계좌"],
                "createdAt": datetime.now().isoformat()
            },
            {
                "id": 4,
                "category": "ETF",
                "title": "ETF (상장지수펀드)",
                "content": "ETF는 주식시장에서 거래되는 펀드로, 특정 지수를 추종합니다. 개별 주식보다 리스크가 분산되고, 수수료가 낮으며, 실시간 거래가 가능합니다. S&P 500, 나스닥, KOSPI 200 등 다양한 지수를 추종하는 ETF가 있어 투자 목적에 맞게 선택할 수 있습니다.",
                "keywords": ["ETF", "상장지수펀드", "인덱스펀드", "패시브투자"],
                "createdAt": datetime.now().isoformat()
            },
            {
                "id": 5,
                "category": "채권",
                "title": "채권 투자",
                "content": "채권은 정부나 기업이 발행하는 차용증서로, 만기일에 원금과 이자를 받을 수 있습니다. 주식보다 안정적이지만 수익률은 낮은 편입니다. 국채, 회사채, 채권펀드 등이 있으며, 금리 변동에 민감하므로 투자 시점을 고려해야 합니다.",
                "keywords": ["채권", "국채", "회사채", "채권펀드", "안전자산"],
                "createdAt": datetime.now().isoformat()
            }
        ]
        
        tips_data = {
            "lastUpdated": datetime.now().isoformat(),
            "tips": sample_tips,
            "count": len(sample_tips)
        }
        
        return tips_data
    
    def save_data(self):
        """샘플 데이터 저장"""
        # 뉴스 데이터 저장
        news_data = self.create_sample_news()
        news_path = os.path.join(self.base_dir, 'data', 'news.json')
        os.makedirs(os.path.dirname(news_path), exist_ok=True)
        
        with open(news_path, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        
        print(f"Sample news data saved to {news_path}")
        
        # 경제상식 데이터 저장
        tips_data = self.create_sample_finance_tips()
        tips_path = os.path.join(self.base_dir, 'data', 'finance-tips.json')
        
        with open(tips_path, 'w', encoding='utf-8') as f:
            json.dump(tips_data, f, ensure_ascii=False, indent=2)
        
        print(f"Sample finance tips data saved to {tips_path}")

def main():
    generator = SampleDataGenerator()
    generator.save_data()
    print("Sample data generation completed successfully!")

if __name__ == "__main__":
    main()
