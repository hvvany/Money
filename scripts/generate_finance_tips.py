#!/usr/bin/env python3
"""
경제 상식 콘텐츠 생성기
OpenAI API를 사용하여 금융상품 설명을 생성합니다.
"""

import openai
import json
import os
import sys
from datetime import datetime
from typing import List, Dict

class FinanceTipsGenerator:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # 금융상품 카테고리 정의
        self.finance_categories = [
            {
                'category': '연금저축',
                'title': '연금저축이란?',
                'keywords': ['연금저축', '개인연금', '퇴직연금', 'IRP', '연금보험']
            },
            {
                'category': '주식',
                'title': '주식 투자 기초',
                'keywords': ['주식', '주식투자', '증권', '코스피', '코스닥', 'ETF']
            },
            {
                'category': 'ISA',
                'title': 'ISA (개인종합자산관리계좌)',
                'keywords': ['ISA', '개인종합자산관리계좌', '세제혜택', '투자계좌']
            },
            {
                'category': 'ETF',
                'title': 'ETF (상장지수펀드)',
                'keywords': ['ETF', '상장지수펀드', '인덱스펀드', '패시브투자']
            },
            {
                'category': '채권',
                'title': '채권 투자',
                'keywords': ['채권', '국채', '회사채', '채권펀드', '안전자산']
            },
            {
                'category': '펀드',
                'title': '펀드 투자',
                'keywords': ['펀드', '투자신탁', '자산운용', '액티브펀드', '패시브펀드']
            },
            {
                'category': '예적금',
                'title': '예금과 적금',
                'keywords': ['예금', '적금', '정기예금', '정기적금', '자유적금']
            },
            {
                'category': '보험',
                'title': '보험 상품',
                'keywords': ['보험', '생명보험', '손해보험', '연금보험', '종신보험']
            },
            {
                'category': '부동산',
                'title': '부동산 투자',
                'keywords': ['부동산', '아파트', '오피스텔', 'REITs', '부동산펀드']
            },
            {
                'category': '암호화폐',
                'title': '암호화폐 투자',
                'keywords': ['암호화폐', '비트코인', '이더리움', '가상화폐', '블록체인']
            }
        ]
    
    def generate_tip_content(self, category_info: Dict) -> str:
        """개별 금융상품 설명 생성"""
        try:
            prompt = f"""
다음 금융상품에 대해 300-400자로 설명해주세요. 
일반인이 이해하기 쉽게 작성하고, 핵심 특징과 장단점을 포함해주세요.

카테고리: {category_info['category']}
제목: {category_info['title']}
관련 키워드: {', '.join(category_info['keywords'])}

설명:
"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 금융 전문가입니다. 일반인이 이해하기 쉽게 금융상품을 설명해주세요."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating content for {category_info['category']}: {e}")
            return f"{category_info['title']}에 대한 설명을 생성할 수 없습니다."
    
    def generate_all_tips(self):
        """모든 금융상품 설명 생성"""
        print("Generating finance tips content...")
        
        tips = []
        
        for i, category_info in enumerate(self.finance_categories):
            print(f"Generating content {i+1}/{len(self.finance_categories)}: {category_info['category']}")
            
            content = self.generate_tip_content(category_info)
            
            tip = {
                'id': i + 1,
                'category': category_info['category'],
                'title': category_info['title'],
                'content': content,
                'keywords': category_info['keywords'],
                'createdAt': datetime.now().isoformat()
            }
            
            tips.append(tip)
            
            # API 호출 간격 조절
            import time
            time.sleep(1)
        
        return tips
    
    def save_tips_data(self, tips: List[Dict]):
        """경제 상식 데이터 저장"""
        data = {
            'lastUpdated': datetime.now().isoformat(),
            'tips': tips,
            'count': len(tips)
        }
        
        output_path = os.path.join(self.base_dir, 'data', 'finance-tips.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Finance tips data saved to {output_path}")

def main():
    # OpenAI API 키 확인
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set your OpenAI API key in GitHub Secrets.")
        sys.exit(1)
    
    generator = FinanceTipsGenerator()
    
    try:
        # 경제 상식 콘텐츠 생성
        tips = generator.generate_all_tips()
        
        # JSON 파일로 저장
        generator.save_tips_data(tips)
        
        print("Finance tips generation completed successfully!")
        
    except Exception as e:
        print(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
