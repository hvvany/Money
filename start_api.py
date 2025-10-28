#!/usr/bin/env python3
"""
로컬 크롤링 API 서버 실행 스크립트
개발 환경에서 수동 크롤링을 위한 Flask 서버를 시작합니다.
"""

import subprocess
import sys
import os

def install_requirements():
    """API 서버 실행에 필요한 패키지 설치"""
    try:
        print("API 서버 의존성 설치 중...")
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'api/requirements.txt'
        ])
        print("의존성 설치 완료!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"의존성 설치 실패: {e}")
        return False

def start_api_server():
    """API 서버 시작"""
    try:
        print("로컬 크롤링 API 서버 시작...")
        print("서버 주소: http://localhost:5000")
        print("사용 가능한 엔드포인트:")
        print("  POST http://localhost:5000/api/crawl - 수동 크롤링 실행")
        print("  GET  http://localhost:5000/api/status - 서버 상태 확인")
        print("  GET  http://localhost:5000/api/health - 헬스 체크")
        print("\n서버를 중지하려면 Ctrl+C를 누르세요.")
        
        # API 서버 실행
        subprocess.run([sys.executable, 'api/crawl.py'])
        
    except KeyboardInterrupt:
        print("\n서버가 중지되었습니다.")
    except Exception as e:
        print(f"서버 실행 오류: {e}")

if __name__ == '__main__':
    # 의존성 설치
    if not install_requirements():
        sys.exit(1)
    
    # API 서버 시작
    start_api_server()
