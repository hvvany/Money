# GitHub Actions 자동 실행 설정 가이드

## 🚨 **자동 실행이 안 되는 경우 체크리스트**

### **1. 저장소 설정 확인**

#### **A. GitHub Actions 활성화**
1. GitHub 저장소 → **Settings** → **Actions** → **General**
2. **"Allow all actions and reusable workflows"** 선택
3. **"Allow actions and reusable workflows"** 섹션에서:
   - ✅ **"Allow all actions and reusable workflows"** 체크
   - ✅ **"Allow actions created by GitHub"** 체크
   - ✅ **"Allow actions by Marketplace verified creators"** 체크

#### **B. 브랜치 보호 규칙 확인**
1. GitHub 저장소 → **Settings** → **Branches**
2. `main` 브랜치에 보호 규칙이 있다면:
   - **"Restrict pushes that create files"** 비활성화
   - **"Require status checks to pass before merging"** 비활성화 (Actions용)

### **2. 워크플로우 파일 위치 확인**

```
.github/
└── workflows/
    ├── crawl-news.yml          # 메인 크롤링 워크플로우
    └── test-schedule.yml       # 테스트용 워크플로우
```

### **3. 권한 설정 확인**

#### **A. 저장소 권한**
- 저장소가 **Public**이거나 **Private**이어도 Actions 사용 가능
- **Organization** 저장소의 경우 Actions 권한 확인 필요

#### **B. Secrets 설정**
1. GitHub 저장소 → **Settings** → **Secrets and variables** → **Actions**
2. 다음 Secrets가 설정되어 있는지 확인:
   - `OPENAI_API_KEY`: OpenAI API 키 (선택사항, 로컬 요약 사용)

### **4. 스케줄 실행 확인**

#### **A. Cron 표현식 검증**
```yaml
# 현재 설정: 매시간 정각 실행 (UTC 시간 기준)
- cron: '0 * * * *'

# 테스트용: 매시간 정각 실행
- cron: '0 * * * *'
```

#### **B. 시간대 확인**
- GitHub Actions는 **UTC 시간** 기준
- 매시간 정각에 실행 (00:00, 01:00, 02:00, ... 23:00 UTC)
- 한국시간으로는 09:00, 10:00, 11:00, ... 08:00 (다음날)

### **5. 실행 로그 확인**

#### **A. Actions 탭에서 확인**
1. GitHub 저장소 → **Actions** 탭
2. **"Daily News Crawler"** 워크플로우 클릭
3. 실행 기록 확인:
   - ✅ **성공**: 초록색 체크마크
   - ❌ **실패**: 빨간색 X
   - ⏸️ **대기**: 노란색 원

#### **B. 로그 분석**
- **"Checkout repository"** 단계에서 실패하는 경우: 권한 문제
- **"Run news crawler"** 단계에서 실패하는 경우: 스크립트 오류
- **"Commit and push changes"** 단계에서 실패하는 경우: Git 권한 문제

### **6. 문제 해결 방법**

#### **A. 워크플로우가 전혀 실행되지 않는 경우**
1. **Actions 활성화 확인**
2. **워크플로우 파일 위치 확인**
3. **브랜치 확인** (main 브랜치에 있어야 함)
4. **YAML 문법 오류 확인**

#### **B. 워크플로우는 실행되지만 실패하는 경우**
1. **로그 확인**하여 실패 원인 파악
2. **권한 설정** 확인
3. **Secrets 설정** 확인
4. **스크립트 오류** 수정

#### **C. 스케줄이 예상 시간에 실행되지 않는 경우**
1. **Cron 표현식** 재확인
2. **시간대 계산** 재확인
3. **GitHub Actions 지연** 고려 (최대 15분 지연 가능)

### **7. 테스트 방법**

#### **A. 수동 실행 테스트**
1. GitHub 저장소 → **Actions** → **Daily News Crawler**
2. **"Run workflow"** 버튼 클릭
3. **"Run workflow"** 드롭다운에서 **"main"** 선택
4. **"Run workflow"** 버튼 클릭

#### **B. 스케줄 테스트**
1. `test-schedule.yml` 워크플로우 사용
2. 매 5분마다 실행되도록 설정
3. 실행 로그 확인

### **8. 일반적인 문제와 해결책**

| 문제 | 원인 | 해결책 |
|------|------|--------|
| 워크플로우가 실행되지 않음 | Actions 비활성화 | Settings → Actions → General에서 활성화 |
| 권한 오류 | Git 권한 부족 | permissions 섹션 추가 |
| 커밋 실패 | 브랜치 보호 규칙 | 보호 규칙 비활성화 또는 예외 추가 |
| 스크립트 오류 | Python 환경 문제 | requirements.txt 확인 |
| 시간대 오류 | Cron 표현식 오류 | UTC 시간으로 재계산 |

### **9. 모니터링**

#### **A. 실행 상태 확인**
- GitHub 저장소 → **Actions** 탭에서 실시간 모니터링
- 이메일 알림 설정 (Settings → Notifications)

#### **B. 데이터 업데이트 확인**
- `data/news.json` 파일의 최신 업데이트 시간 확인
- 커밋 히스토리에서 자동 커밋 확인

## 📞 **추가 도움이 필요한 경우**

1. **GitHub Actions 로그** 스크린샷 첨부
2. **저장소 설정** 스크린샷 첨부
3. **에러 메시지** 전체 내용 복사
4. **워크플로우 실행 시간**과 **예상 시간** 비교
