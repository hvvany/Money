#!/usr/bin/env python3
"""
경제 상식 RAG API 서버
Flask를 사용한 REST API 서버
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from rag_finance_knowledge import FinanceRAGSystem

app = Flask(__name__)
CORS(app)  # CORS 허용

# RAG 시스템 초기화
rag_system = None

def initialize_rag_system():
    """RAG 시스템 초기화"""
    global rag_system
    try:
        rag_system = FinanceRAGSystem()
        rag_system.initialize_knowledge_base()
        print("RAG system initialized successfully!")
        return True
    except Exception as e:
        print(f"Error initializing RAG system: {e}")
        return False

@app.route('/api/health', methods=['GET'])
def health_check():
    """서버 상태 확인"""
    return jsonify({
        'status': 'healthy',
        'message': 'RAG API server is running'
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
        knowledge_items = rag_system.query_knowledge(question, top_k=3)
        
        return jsonify({
            'question': question,
            'answer': answer,
            'related_knowledge': knowledge_items,
            'timestamp': rag_system.base_dir  # 임시로 base_dir 사용
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
        knowledge_items = rag_system.query_knowledge(query, top_k=top_k)
        
        return jsonify({
            'query': query,
            'results': knowledge_items,
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
    print("Starting RAG API server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
