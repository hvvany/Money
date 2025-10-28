# 🚀 경제 뉴스 서비스 설정 가이드

## 📋 **설정 전 체크리스트**

### **1. GitHub 저장소 정보 확인**
- [ ] GitHub 사용자명 또는 조직명
- [ ] 저장소 이름
- [ ] 기본 브랜치명 (`main` 또는 `master`)

### **2. 필요한 설정값들**

#### **A. 워크플로우 파일 수정**
`.github/workflows/crawl-news.yml` 파일에서 다음 부분을 확인:

```yaml
# 현재 설정 (수정 불필요)
- cron: '0 * * * *'  # 매시간 실행
```

#### **B. 브랜치명 확인**
```yaml
# 42번째 줄 근처
git push origin HEAD:master  # 또는 main
```

### **3. GitHub 저장소 설정**

#### **A. Actions 활성화**
1. GitHub 저장소 → **Settings** → **Actions** → **General**
2. **"Allow all actions and reusable workflows"** 선택
3. **Save** 클릭

#### **B. 브랜치 보호 규칙 확인**
1. GitHub 저장소 → **Settings** → **Branches**
2. `master` (또는 `main`) 브랜치 선택
3. **"Restrict pushes that create files"** 비활성화
4. **"Require status checks to pass before merging"** 비활성화

#### **C. Secrets 설정 (선택사항)**
1. GitHub 저장소 → **Settings** → **Secrets and variables** → **Actions**
2. **"New repository secret"** 클릭
3. Name: `OPENAI_API_KEY`
4. Value: `sk-proj-...` (OpenAI API 키)
5. **"Add secret"** 클릭

### **4. 워크플로우 테스트**

#### **A. 수동 실행 테스트**
1. GitHub 저장소 → **Actions** 탭
2. **"Daily News Crawler"** 클릭
3. **"Run workflow"** 버튼 클릭
4. **"Run workflow"** 드롭다운에서 `master` 선택
5. **"Run workflow"** 버튼 클릭

#### **B. 실행 결과 확인**
- ✅ **성공**: 초록색 체크마크
- ❌ **실패**: 빨간색 X (로그 확인 필요)
- ⏳ **진행 중**: 노란색 원

### **5. 자동 실행 확인**

#### **A. 스케줄 실행 확인**
- 매시간 정각에 자동 실행됨
- Actions 탭에서 실행 기록 확인
- `data/news.json` 파일 업데이트 확인

#### **B. 실행 시간표 (한국시간)**
| UTC 시간 | 한국시간 | 실행 여부 |
|----------|----------|-----------|
| 00:00 | 09:00 | ✅ |
| 01:00 | 10:00 | ✅ |
| 02:00 | 11:00 | ✅ |
| ... | ... | ✅ |
| 23:00 | 08:00 | ✅ |

### **6. 문제 해결**

#### **A. 워크플로우가 실행되지 않는 경우**
1. **Actions 활성화 확인**
2. **워크플로우 파일 위치 확인** (`.github/workflows/`)
3. **브랜치명 확인** (`master` 또는 `main`)
4. **YAML 문법 오류 확인**

#### **B. 권한 오류가 발생하는 경우**
1. **브랜치 보호 규칙 확인**
2. **저장소 권한 확인**
3. **워크플로우 권한 설정 확인**

#### **C. 크롤링이 실패하는 경우**
1. **로그 확인**하여 구체적인 오류 파악
2. **네트워크 연결 확인**
3. **스크립트 오류 수정**

### **7. 배포 확인**

#### **A. GitHub Pages 활성화**
1. GitHub 저장소 → **Settings** → **Pages**
2. **Source**: "Deploy from a branch" 선택
3. **Branch**: `master` (또는 `main`) 선택
4. **Folder**: "/ (root)" 선택
5. **Save** 클릭

#### **B. 웹 서비스 접속**
- URL: `https://[사용자명].github.io/[저장소명]`
- 배포 완료까지 5-10분 소요

### **8. 모니터링**

#### **A. 정기 확인사항**
- [ ] Actions 탭에서 워크플로우 실행 상태 확인
- [ ] `data/news.json` 파일 업데이트 확인
- [ ] 웹 서비스 정상 작동 확인

#### **B. 알림 설정**
- GitHub 저장소 → **Settings** → **Notifications**
- **"Actions"** 체크하여 이메일 알림 받기

## 🔧 **개발 환경 설정 (선택사항)**

### **로컬 테스트**
```bash
# 1. 저장소 클론
git clone https://github.com/[사용자명]/[저장소명].git
cd [저장소명]

# 2. 가상환경 생성
python -m venv venv

# 3. 가상환경 활성화
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 4. 의존성 설치
pip install -r scripts/requirements.txt

# 5. 웹 서버 실행
python -m http.server 8000

# 6. API 서버 실행 (선택사항)
python start_api.py
```

### **로컬 크롤링 테스트**
```bash
# 크롤링 스크립트 직접 실행
python scripts/enhanced_hankyung_crawler.py
python scripts/local_summarizer.py
```

## 📞 **도움이 필요한 경우**

1. **GitHub Actions 로그** 스크린샷 첨부
2. **에러 메시지** 전체 내용 복사
3. **저장소 설정** 스크린샷 첨부
4. **실행 시간**과 **예상 시간** 비교

---

**🎉 설정이 완료되면 매시간마다 최신 경제 뉴스가 자동으로 업데이트됩니다!**
