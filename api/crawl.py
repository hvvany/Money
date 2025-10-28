#!/usr/bin/env python3
"""
로컬 크롤링 API 서버
개발 환경에서 수동 크롤링을 위한 간단한 Flask 서버
"""

import os
import sys
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

# 상위 디렉토리의 scripts 모듈을 import하기 위한 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

try:
    from enhanced_hankyung_crawler import main as crawl_news
    from local_summarizer import main as summarize_news
except ImportError as e:
    print(f"Import error: {e}")
    crawl_news = None
    summarize_news = None

app = Flask(__name__)
CORS(app)

@app.route('/api/crawl', methods=['POST'])
def trigger_crawl():
    """수동 크롤링 실행"""
    try:
        if not crawl_news or not summarize_news:
            return jsonify({
                'success': False,
                'error': '크롤링 모듈을 찾을 수 없습니다.'
            }), 500

        # 뉴스 크롤링 실행
        print("뉴스 크롤링 시작...")
        crawl_result = crawl_news()
        
        if not crawl_result:
            return jsonify({
                'success': False,
                'error': '크롤링에 실패했습니다.'
            }), 500

        # 뉴스 요약 실행
        print("뉴스 요약 시작...")
        summary_result = summarize_news()
        
        if not summary_result:
            return jsonify({
                'success': False,
                'error': '요약 생성에 실패했습니다.'
            }), 500

        return jsonify({
            'success': True,
            'message': '크롤링과 요약이 완료되었습니다.',
            'timestamp': json.dumps({
                'crawl_time': crawl_result.get('timestamp'),
                'summary_time': summary_result.get('timestamp')
            })
        })

    except Exception as e:
        print(f"크롤링 오류: {e}")
        return jsonify({
            'success': False,
            'error': f'크롤링 중 오류가 발생했습니다: {str(e)}'
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """서버 상태 확인"""
    return jsonify({
        'status': 'running',
        'crawl_available': crawl_news is not None,
        'summarize_available': summarize_news is not None
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """헬스 체크"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("로컬 크롤링 API 서버 시작...")
    print("사용 가능한 엔드포인트:")
    print("  POST /api/crawl - 수동 크롤링 실행")
    print("  GET  /api/status - 서버 상태 확인")
    print("  GET  /api/health - 헬스 체크")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
