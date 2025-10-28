#!/usr/bin/env python3
"""
간단한 RAG 시스템
ChromaDB 없이 키워드 기반 검색과 OpenAI를 활용한 경제 상식 시스템
"""

import openai
import json
import os
import sys
import re
from datetime import datetime
from typing import List, Dict
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS 허용

class SimpleRAGSystem:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # 경제 상식 데이터 초기화
        self.finance_knowledge = self.get_finance_knowledge_data()
        
    def get_finance_knowledge_data(self):
        """경제 상식 데이터 정의"""
        return [
            {
                "id": "pension_savings",
                "title": "연금저축",
                "content": """
                연금저축은 노후 준비를 위한 장기 저축 상품입니다.
                
                주요 특징:
                - 매년 400만원까지 세제혜택을 받으며 납입 가능
                - 55세 이후 연금으로 수령하거나 일시금으로 받을 수 있음
                - 개인연금저축(IRP)과 퇴직연금(401k) 등이 있음
                - 장기간 꾸준히 납입할수록 더 큰 혜택을 받을 수 있음
                - 연금소득세 혜택을 받을 수 있음
                
                장점: 세제혜택, 장기적 자산 형성, 연금소득세 혜택
                단점: 장기간 자금 동결, 조기 인출 시 불이익
                """,
                "category": "연금",
                "keywords": ["연금저축", "개인연금", "퇴직연금", "IRP", "연금보험", "세제혜택", "노후준비"]
            },
            {
                "id": "stock_investment",
                "title": "주식 투자",
                "content": """
                주식은 기업의 일부를 소유하는 증권으로, 기업의 성장과 함께 주가가 상승할 가능성이 있습니다.
                
                주요 특징:
                - 코스피와 코스닥 시장에서 거래됨
                - 배당을 통해 수익을 얻을 수 있음
                - 주가는 변동성이 크므로 리스크 관리가 중요
                - 장기 투자와 단기 투자 전략이 다름
                - 기업 분석과 시장 분석이 필요
                
                투자 전략:
                - 가치 투자: 내재가치 대비 저평가된 주식 선택
                - 성장 투자: 높은 성장 가능성이 있는 기업 투자
                - 분산 투자: 여러 종목에 분산 투자하여 리스크 분산
                
                장점: 높은 수익 가능성, 유동성, 소유권
                단점: 높은 변동성, 손실 위험, 시장 리스크
                """,
                "category": "투자",
                "keywords": ["주식", "주식투자", "증권", "코스피", "코스닥", "ETF", "배당", "투자전략"]
            },
            {
                "id": "isa_account",
                "title": "ISA (개인종합자산관리계좌)",
                "content": """
                ISA는 다양한 금융상품을 하나의 계좌에서 관리할 수 있는 통합 투자계좌입니다.
                
                주요 특징:
                - 연간 2천만원까지 투자 가능
                - 3년 이상 보유 시 세제혜택을 받을 수 있음
                - 주식, 채권, 펀드, ETF 등 다양한 상품에 투자 가능
                - 포트폴리오 분산투자에 유리
                - 1년에 1회만 개설 가능
                
                세제혜택:
                - 3년 이상 보유 시 배당소득세, 양도소득세 면제
                - 연간 200만원까지 이자소득세 면제
                - 1년에 1회만 출금 가능
                
                장점: 세제혜택, 다양한 상품 투자, 통합 관리
                단점: 연간 투자 한도, 출금 제한, 복잡한 규정
                """,
                "category": "투자",
                "keywords": ["ISA", "개인종합자산관리계좌", "세제혜택", "투자계좌", "포트폴리오", "통합관리"]
            },
            {
                "id": "etf_investment",
                "title": "ETF (상장지수펀드)",
                "content": """
                ETF는 주식시장에서 거래되는 펀드로, 특정 지수를 추종합니다.
                
                주요 특징:
                - 개별 주식보다 리스크가 분산됨
                - 수수료가 낮고 실시간 거래가 가능
                - S&P 500, 나스닥, KOSPI 200 등 다양한 지수 추종
                - 투자 목적에 맞게 선택 가능
                - 인덱스 펀드의 상장 버전
                
                종류:
                - 주식형 ETF: 주식 지수를 추종
                - 채권형 ETF: 채권 지수를 추종
                - 섹터 ETF: 특정 산업 섹터에 집중
                - 테마 ETF: 특정 테마나 트렌드에 집중
                
                투자 전략:
                - 패시브 투자: 시장 수익률 추종
                - 분산 투자: 여러 ETF에 분산 투자
                - 정기 투자: DCA(달러 코스트 평균법) 활용
                
                장점: 낮은 수수료, 높은 유동성, 분산투자 효과
                단점: 시장 수익률에 제한, 개별 종목 대비 낮은 수익
                """,
                "category": "투자",
                "keywords": ["ETF", "상장지수펀드", "인덱스펀드", "패시브투자", "분산투자", "수수료"]
            },
            {
                "id": "bond_investment",
                "title": "채권 투자",
                "content": """
                채권은 정부나 기업이 발행하는 차용증서로, 만기일에 원금과 이자를 받을 수 있습니다.
                
                주요 특징:
                - 주식보다 안정적이지만 수익률은 낮은 편
                - 국채, 회사채, 채권펀드 등이 있음
                - 금리 변동에 민감하므로 투자 시점이 중요
                - 신용도에 따라 수익률이 달라짐
                - 만기까지 보유하면 원금 보장
                
                종류:
                - 국채: 정부가 발행하는 채권 (가장 안전)
                - 회사채: 기업이 발행하는 채권 (신용도에 따라 수익률 차이)
                - 지방채: 지방자치단체가 발행하는 채권
                - 채권펀드: 여러 채권에 분산 투자하는 펀드
                
                투자 고려사항:
                - 신용도: 발행자의 신용도 확인
                - 만기: 만기가 길수록 금리 변동 리스크 증가
                - 금리 환경: 금리 상승 시 채권 가격 하락
                - 인플레이션: 실질 수익률 고려
                
                장점: 안정성, 예측 가능한 수익, 원금 보장
                단점: 낮은 수익률, 금리 변동 리스크, 인플레이션 리스크
                """,
                "category": "투자",
                "keywords": ["채권", "국채", "회사채", "채권펀드", "안전자산", "고정수익", "금리"]
            },
            {
                "id": "fund_investment",
                "title": "펀드 투자",
                "content": """
                펀드는 여러 투자자로부터 자금을 모아 전문가가 운용하는 투자상품입니다.
                
                주요 특징:
                - 전문가가 대신 투자 운용
                - 소액으로도 분산 투자 가능
                - 액티브 펀드와 패시브 펀드로 구분
                - 수수료와 보수 지불 필요
                - 언제든 환매 가능 (유동성)
                
                종류:
                - 액티브 펀드: 전문가가 적극적으로 운용하여 시장 수익률 초과 목표
                - 패시브 펀드: 특정 지수를 추종하여 시장 수익률 추종
                - 주식형 펀드: 주식에 집중 투자
                - 채권형 펀드: 채권에 집중 투자
                - 혼합형 펀드: 주식과 채권을 적절히 배분
                
                투자 전략:
                - 장기 투자: 복리 효과를 통한 자산 증식
                - 정기 투자: 시장 변동성을 평균화
                - 분산 투자: 여러 펀드에 분산 투자
                
                장점: 전문가 운용, 분산투자 효과, 소액 투자 가능
                단점: 수수료 부담, 운용사 리스크, 시장 리스크
                """,
                "category": "투자",
                "keywords": ["펀드", "투자신탁", "자산운용", "액티브펀드", "패시브펀드", "분산투자", "전문가운용"]
            },
            {
                "id": "deposit_savings",
                "title": "예금과 적금",
                "content": """
                예금과 적금은 은행에 자금을 맡기고 이자를 받는 가장 기본적인 금융상품입니다.
                
                예금 (정기예금):
                - 일정 기간 동안 자금을 맡기고 이자를 받음
                - 만기 전 해지 시 이자 손실
                - 금리가 고정되어 있어 예측 가능
                - 원금 보장
                
                적금 (정기적금):
                - 매월 일정 금액을 납입하고 만기 시 이자를 받음
                - 강제 저축 효과
                - 복리 효과로 이자 수익 증대
                - 중도 해지 시 이자 손실
                
                종류:
                - 정기예금: 일시불 예치 후 만기 시 이자 수령
                - 정기적금: 매월 납입 후 만기 시 이자 수령
                - 자유적금: 납입 금액과 시기를 자유롭게 조절
                - 주택청약종합저축: 주택 구매를 위한 특별 적금
                
                선택 기준:
                - 자금 여유도: 정기예금 vs 적금
                - 금리 환경: 금리 상승/하락 전망
                - 목적: 단기/장기 목적에 따라 선택
                
                장점: 안전성, 원금 보장, 예측 가능한 수익
                단점: 낮은 수익률, 인플레이션 리스크, 기회비용
                """,
                "category": "저축",
                "keywords": ["예금", "적금", "정기예금", "정기적금", "자유적금", "이자", "저축"]
            },
            {
                "id": "insurance_products",
                "title": "보험 상품",
                "content": """
                보험은 위험을 분산시키는 금융상품으로, 다양한 위험에 대비할 수 있습니다.
                
                주요 특징:
                - 위험 발생 시 보상금 지급
                - 보험료 납입을 통해 위험 분산
                - 생명보험과 손해보험으로 구분
                - 보장과 저축 기능을 동시에 제공
                
                종류:
                - 생명보험: 사망, 질병, 상해 등에 대한 보장
                - 손해보험: 자동차, 화재, 여행 등에 대한 보장
                - 연금보험: 노후 생활비를 위한 연금 지급
                - 종신보험: 평생 보장하는 생명보험
                
                보험 선택 기준:
                - 보장 필요성: 어떤 위험에 대비할 것인가
                - 보험료 부담: 월 보험료가 가계에 부담되지 않는가
                - 보장 내용: 보장 범위와 금액이 적절한가
                - 보험사 신뢰도: 보험사의 재정 건전성
                
                장점: 위험 분산, 안정성, 세제혜택
                단점: 보험료 부담, 복잡한 약관, 해지 시 손실
                """,
                "category": "보험",
                "keywords": ["보험", "생명보험", "손해보험", "연금보험", "종신보험", "보장", "보험료"]
            },
            {
                "id": "real_estate_investment",
                "title": "부동산 투자",
                "content": """
                부동산 투자는 토지, 건물 등 부동산에 투자하여 수익을 얻는 투자 방법입니다.
                
                주요 특징:
                - 실물 자산으로 인플레이션에 강함
                - 임대 수익과 매매 수익을 동시에 추구
                - 높은 진입 장벽 (많은 자금 필요)
                - 지역별, 용도별 특성이 다름
                
                투자 방법:
                - 직접 투자: 직접 부동산을 구매하여 관리
                - 간접 투자: REITs, 부동산펀드 등을 통한 투자
                - 개발 투자: 부동산을 개발하여 수익 창출
                - 임대 투자: 임대 수익을 통한 안정적 수익
                
                고려사항:
                - 위치: 접근성, 상권, 교통편의성
                - 용도: 주거용, 상업용, 사무용
                - 시장 동향: 지역별 시장 상황
                - 자금 조달: 대출 조건과 이자 부담
                - 세금: 양도소득세, 종합부동산세 등
                
                장점: 실물 자산, 인플레이션 헤지, 임대 수익
                단점: 높은 진입 장벽, 유동성 부족, 관리 부담
                """,
                "category": "투자",
                "keywords": ["부동산", "아파트", "오피스텔", "REITs", "부동산펀드", "임대", "실물자산"]
            },
            {
                "id": "cryptocurrency",
                "title": "암호화폐 투자",
                "content": """
                암호화폐는 블록체인 기술을 기반으로 한 디지털 자산입니다.
                
                주요 특징:
                - 중앙은행이나 정부의 통제 없이 운영
                - 블록체인 기술로 보안성과 투명성 확보
                - 24시간 거래 가능
                - 높은 변동성과 수익 가능성
                - 전 세계 어디서나 거래 가능
                
                주요 암호화폐:
                - 비트코인: 최초이자 가장 유명한 암호화폐
                - 이더리움: 스마트 컨트랙트 플랫폼
                - 알트코인: 비트코인 외의 다른 암호화폐들
                
                투자 고려사항:
                - 변동성: 매우 높은 가격 변동성
                - 규제: 각국의 규제 정책 변화
                - 기술: 블록체인 기술의 발전
                - 보안: 해킹, 분실 위험
                - 유동성: 거래소별 유동성 차이
                
                투자 전략:
                - 분산 투자: 여러 암호화폐에 분산
                - 장기 투자: 단기 변동성 무시하고 장기 보유
                - 정기 투자: DCA 방식으로 정기 투자
                - 리스크 관리: 투자 금액의 일정 비율만 투자
                
                장점: 높은 수익 가능성, 24시간 거래, 글로벌 접근성
                단점: 높은 변동성, 규제 리스크, 보안 위험
                """,
                "category": "투자",
                "keywords": ["암호화폐", "비트코인", "이더리움", "가상화폐", "블록체인", "디지털자산", "변동성"]
            }
        ]
    
    def search_knowledge(self, query: str, top_k: int = 3) -> List[Dict]:
        """키워드 기반 지식 검색"""
        query_lower = query.lower()
        scored_items = []
        
        for item in self.finance_knowledge:
            score = 0
            
            # 제목에서 키워드 매칭
            if any(keyword.lower() in item['title'].lower() for keyword in query.split()):
                score += 3
            
            # 키워드에서 매칭
            if any(keyword.lower() in query_lower for keyword in item['keywords']):
                score += 2
            
            # 내용에서 키워드 매칭
            content_lower = item['content'].lower()
            for keyword in query.split():
                if keyword.lower() in content_lower:
                    score += 1
            
            if score > 0:
                scored_items.append({
                    'item': item,
                    'score': score
                })
        
        # 점수순으로 정렬하고 상위 k개 반환
        scored_items.sort(key=lambda x: x['score'], reverse=True)
        return [item['item'] for item in scored_items[:top_k]]
    
    def generate_answer(self, question: str) -> str:
        """RAG를 활용한 답변 생성"""
        try:
            # 관련 지식 검색
            knowledge_items = self.search_knowledge(question, top_k=3)
            
            if not knowledge_items:
                return "죄송합니다. 관련 정보를 찾을 수 없습니다. 다른 질문을 해주세요."
            
            # 검색된 지식을 컨텍스트로 구성
            context = "\n\n".join([
                f"제목: {item['title']}\n내용: {item['content']}"
                for item in knowledge_items
            ])
            
            # OpenAI API로 답변 생성
            prompt = f"""
            다음은 경제 상식에 대한 질문과 관련 정보입니다.
            
            질문: {question}
            
            관련 정보:
            {context}
            
            위 정보를 바탕으로 질문에 대한 정확하고 도움이 되는 답변을 작성해주세요.
            답변은 300-500자 정도로 간결하게 작성하고, 구체적인 정보와 실용적인 조언을 포함해주세요.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 경제 상식 전문가입니다. 사용자의 질문에 정확하고 도움이 되는 답변을 제공해주세요."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating answer: {e}")
            return "죄송합니다. 답변을 생성하는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
    
    def get_all_categories(self) -> List[str]:
        """모든 카테고리 목록 반환"""
        categories = set()
        for item in self.finance_knowledge:
            categories.add(item['category'])
        return list(categories)
    
    def get_knowledge_by_category(self, category: str) -> List[Dict]:
        """카테고리별 지식 반환"""
        return [item for item in self.finance_knowledge if item['category'] == category]

# 전역 RAG 시스템 인스턴스
rag_system = None

def initialize_rag_system():
    """RAG 시스템 초기화"""
    global rag_system
    try:
        rag_system = SimpleRAGSystem()
        print("Simple RAG system initialized successfully!")
        return True
    except Exception as e:
        print(f"Error initializing RAG system: {e}")
        return False

@app.route('/api/health', methods=['GET'])
def health_check():
    """서버 상태 확인"""
    return jsonify({
        'status': 'healthy',
        'message': 'Simple RAG API server is running'
    })

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """모든 카테고리 목록 반환"""
    try:
        if not rag_system:
            return jsonify({'error': 'RAG system not initialized'}), 500
        
        categories = rag_system.get_all_categories()
        return jsonify({
            'categories': categories,
            'count': len(categories)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/knowledge/<category>', methods=['GET'])
def get_knowledge_by_category(category):
    """카테고리별 지식 반환"""
    try:
        if not rag_system:
            return jsonify({'error': 'RAG system not initialized'}), 500
        
        knowledge = rag_system.get_knowledge_by_category(category)
        return jsonify({
            'category': category,
            'knowledge': knowledge,
            'count': len(knowledge)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """질문에 대한 답변 생성"""
    try:
        if not rag_system:
            return jsonify({'error': 'RAG system not initialized'}), 500
        
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({'error': 'Question is required'}), 400
        
        question = data['question']
        if not question.strip():
            return jsonify({'error': 'Question cannot be empty'}), 400
        
        # 답변 생성
        answer = rag_system.generate_answer(question)
        
        # 관련 지식도 함께 반환
        knowledge_items = rag_system.search_knowledge(question, top_k=3)
        
        return jsonify({
            'question': question,
            'answer': answer,
            'related_knowledge': [{'metadata': {'title': item['title']}, 'content': item['content']} for item in knowledge_items],
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_knowledge():
    """지식베이스 검색"""
    try:
        if not rag_system:
            return jsonify({'error': 'RAG system not initialized'}), 500
        
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        query = data['query']
        top_k = data.get('top_k', 5)
        
        if not query.strip():
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        # 지식 검색
        knowledge_items = rag_system.search_knowledge(query, top_k=top_k)
        
        return jsonify({
            'query': query,
            'results': [{'metadata': {'title': item['title']}, 'content': item['content']} for item in knowledge_items],
            'count': len(knowledge_items)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/random', methods=['GET'])
def get_random_knowledge():
    """랜덤 지식 반환"""
    try:
        if not rag_system:
            return jsonify({'error': 'RAG system not initialized'}), 500
        
        import random
        random_item = random.choice(rag_system.finance_knowledge)
        
        return jsonify({
            'knowledge': random_item
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # OpenAI API 키 확인
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        sys.exit(1)
    
    # RAG 시스템 초기화
    if not initialize_rag_system():
        print("Failed to initialize RAG system. Exiting...")
        sys.exit(1)
    
    # 서버 실행
    print("Starting Simple RAG API server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
