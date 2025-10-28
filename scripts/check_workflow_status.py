#!/usr/bin/env python3
"""
GitHub Actions 워크플로우 실행 상태 확인 스크립트
"""

import requests
import json
import os
from datetime import datetime, timezone
import pytz

def check_workflow_status(repo_owner, repo_name, token=None):
    """워크플로우 실행 상태 확인"""
    
    # GitHub API 엔드포인트
    base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    headers.update({
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Economic-News-Service"
    })
    
    try:
        # 워크플로우 목록 조회
        workflows_url = f"{base_url}/actions/workflows"
        response = requests.get(workflows_url, headers=headers)
        
        if response.status_code != 200:
            print(f"❌ 워크플로우 목록 조회 실패: {response.status_code}")
            print(f"응답: {response.text}")
            return False
        
        workflows = response.json()
        print(f"📋 등록된 워크플로우 수: {workflows['total_count']}")
        
        # 각 워크플로우의 실행 기록 조회
        for workflow in workflows['workflows']:
            workflow_name = workflow['name']
            workflow_id = workflow['id']
            
            print(f"\n🔍 워크플로우: {workflow_name}")
            print(f"   ID: {workflow_id}")
            print(f"   상태: {'✅ 활성' if workflow['state'] == 'active' else '❌ 비활성'}")
            
            # 최근 실행 기록 조회
            runs_url = f"{base_url}/actions/workflows/{workflow_id}/runs"
            runs_response = requests.get(runs_url, headers=headers)
            
            if runs_response.status_code == 200:
                runs = runs_response.json()
                print(f"   최근 실행 기록: {runs['total_count']}개")
                
                if runs['workflow_runs']:
                    latest_run = runs['workflow_runs'][0]
                    run_status = latest_run['status']
                    run_conclusion = latest_run['conclusion']
                    created_at = latest_run['created_at']
                    
                    # 시간 변환 (UTC → KST)
                    utc_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    kst_time = utc_time.astimezone(pytz.timezone('Asia/Seoul'))
                    
                    print(f"   최근 실행 시간: {kst_time.strftime('%Y-%m-%d %H:%M:%S KST')}")
                    print(f"   실행 상태: {run_status}")
                    print(f"   실행 결과: {run_conclusion or '진행 중'}")
                    
                    # 실행 결과에 따른 상태 표시
                    if run_conclusion == 'success':
                        print("   ✅ 성공")
                    elif run_conclusion == 'failure':
                        print("   ❌ 실패")
                    elif run_conclusion == 'cancelled':
                        print("   ⏹️ 취소됨")
                    else:
                        print("   ⏳ 진행 중")
                else:
                    print("   📝 실행 기록 없음")
            else:
                print(f"   ❌ 실행 기록 조회 실패: {runs_response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

def check_repository_settings(repo_owner, repo_name, token=None):
    """저장소 설정 확인"""
    
    base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    headers.update({
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Economic-News-Service"
    })
    
    try:
        # 저장소 정보 조회
        response = requests.get(base_url, headers=headers)
        
        if response.status_code != 200:
            print(f"❌ 저장소 정보 조회 실패: {response.status_code}")
            return False
        
        repo_info = response.json()
        
        print(f"\n📊 저장소 정보:")
        print(f"   이름: {repo_info['full_name']}")
        print(f"   공개 여부: {'Public' if repo_info['private'] == False else 'Private'}")
        print(f"   기본 브랜치: {repo_info['default_branch']}")
        print(f"   Actions 활성화: {'✅' if repo_info.get('has_actions', False) else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 저장소 정보 조회 오류: {e}")
        return False

def main():
    """메인 함수"""
    print("🔍 GitHub Actions 워크플로우 상태 확인")
    print("=" * 50)
    
    # 저장소 정보 입력
    repo_owner = input("GitHub 사용자명 또는 조직명을 입력하세요: ").strip()
    repo_name = input("저장소 이름을 입력하세요: ").strip()
    
    # 토큰 입력 (선택사항)
    token = input("GitHub Personal Access Token (선택사항): ").strip()
    if not token:
        token = None
        print("⚠️  토큰 없이 조회합니다. 일부 정보가 제한될 수 있습니다.")
    
    print(f"\n📋 저장소: {repo_owner}/{repo_name}")
    print("=" * 50)
    
    # 저장소 설정 확인
    if not check_repository_settings(repo_owner, repo_name, token):
        return
    
    # 워크플로우 상태 확인
    if not check_workflow_status(repo_owner, repo_name, token):
        return
    
    print("\n✅ 확인 완료!")
    print("\n💡 문제가 있다면 GITHUB_ACTIONS_SETUP.md 파일을 참고하세요.")

if __name__ == "__main__":
    main()
