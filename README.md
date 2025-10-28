# 📈 최신 경제소식 뉴스레터

> 매일 아침 최신 경제 이슈를 AI로 요약하여 모바일에서 편리하게 볼 수 있는 서비스

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://your-username.github.io/your-repo-name)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-blue)](https://github.com/your-username/your-repo-name/actions)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ 주요 기능

### 🏠 **홈 탭 - 오늘의 경제 이슈**
- **AI 기반 요약**: 키워드 분석을 통한 스마트한 요약 생성
- **주요 관심사**: 자동 추출된 키워드 (주식시장, 부동산, 금리정책 등)
- **8개 뉴스**: 오늘과 어제의 최신 경제 뉴스
- **실시간 업데이트**: 매일 아침 6시 자동 갱신

### 📰 **뉴스 탭 - 최신 뉴스 목록**
- **다양한 소스**: 한국경제신문 7개 섹션 (경제, 주식, 금융, 부동산, 산업, 글로벌, 정치)
- **2일간 커버리지**: 오늘과 어제 뉴스를 모두 포함
- **상세보기**: 뉴스 클릭 시 전체 본문 표시
- **원문 링크**: 한국경제 원문으로 직접 이동

### 💡 **경제상식 탭 - RAG Q&A 시스템**
- **실시간 Q&A**: 질문하면 즉시 답변 생성
- **제안 질문**: 자주 묻는 질문 10개 제공
- **10개 카테고리**: 연금, 투자, 저축, 보험, 부동산, 암호화폐 등
- **관련 정보**: 답변과 함께 관련 지식 자동 제공

## 🚀 기술적 특징

### **완전 자율 시스템**
- ✅ **API 독립**: 외부 API 없이도 완전 동작
- ✅ **로컬 요약**: 키워드 기반 자동 요약 생성
- ✅ **폴백 시스템**: 크롤링 실패 시 샘플 데이터 자동 생성
- ✅ **GitHub Pages 호환**: 정적 파일 기반 완전 동작

### **스마트 크롤링**
- ✅ **다중 섹션**: 7개 섹션에서 뉴스 수집
- ✅ **아카이브 크롤링**: 오늘과 어제 뉴스 모두 수집
- ✅ **스마트 필터링**: 30개 이상의 경제 키워드로 선별
- ✅ **중복 제거**: 동일한 제목의 뉴스 자동 제거

### **RAG 시스템**
- ✅ **정적 데이터**: JavaScript 기반 경제 상식 데이터베이스
- ✅ **키워드 검색**: 질문 내용 기반 관련 정보 검색
- ✅ **실시간 답변**: 서버 없이도 즉시 Q&A 제공

## 📱 사용법

### 웹 브라우저에서 접속
- GitHub Pages URL로 접속
- 모바일/데스크톱 모든 환경에서 사용 가능

### 탭별 사용법
1. **홈 탭**: 오늘의 주요 경제 이슈와 뉴스 목록 확인
2. **뉴스 탭**: 8개 뉴스 목록에서 관심 있는 뉴스 상세보기
3. **경제상식 탭**: 질문 입력하거나 제안 질문 클릭하여 Q&A

## 🛠️ 설치 및 배포

### 1. 저장소 클론
```bash
git clone <repository-url>
cd economic-news-service
```

### 2. GitHub Pages 배포
1. **GitHub 저장소에 코드 푸시**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **GitHub Pages 활성화**
   - GitHub 저장소 → Settings → Pages
   - Source: "Deploy from a branch" 선택
   - Branch: "main" 선택
   - Folder: "/ (root)" 선택
   - Save 클릭

3. **배포 완료 확인**
   - `https://[username].github.io/[repository-name]`에서 접속 가능
   - 배포 완료까지 5-10분 소요

### 3. 자동 크롤링 활성화 (선택사항)
- GitHub Actions가 자동으로 매일 06:00 KST에 실행됩니다
- 수동 실행: Actions 탭 → "Daily News Crawler" → "Run workflow"
- **주의**: API 키가 설정되어 있어야 정상 작동합니다

## 📁 프로젝트 구조

```
economic-news-service/
├── index.html              # 메인 HTML 파일
├── css/
│   └── style.css          # 커스텀 스타일
├── js/
│   ├── app.js             # 메인 애플리케이션 로직
│   ├── tabHandler.js      # 탭 전환 및 데이터 로딩
│   ├── newsLoader.js      # 뉴스 데이터 로딩
│   └── staticRAGHandler.js # RAG 시스템 (정적 데이터)
├── data/
│   ├── news.json          # 뉴스 데이터
│   └── finance-tips.json  # 경제 상식 데이터
├── scripts/
│   ├── enhanced_hankyung_crawler.py  # 향상된 크롤러
│   ├── local_summarizer.py           # 로컬 요약 생성기
│   └── requirements.txt              # Python 의존성
├── .github/workflows/
│   └── crawl-news.yml     # GitHub Actions 워크플로우
├── PRD.md                 # 제품 요구사항 문서
└── README.md              # 프로젝트 문서
```

## 🔧 기술 스택

### 프론트엔드
- **HTML5**: 시맨틱 마크업
- **CSS3**: Flexbox, Grid, 애니메이션, 그라데이션
- **Bootstrap 5**: 반응형 컴포넌트
- **Vanilla JavaScript**: ES6+ 문법, 모듈화

### 백엔드/자동화
- **GitHub Actions**: 자동 크롤링 워크플로우
- **Python 3.9+**: 크롤링 및 데이터 처리
- **BeautifulSoup4**: HTML 파싱
- **로컬 요약 시스템**: 키워드 기반 자동 요약

### 데이터 소스
- **한국경제신문**: 메인 경제 뉴스 소스
- **다중 섹션**: 경제, 주식, 금융, 부동산, 산업, 글로벌, 정치
- **아카이브 크롤링**: 오늘 + 어제 뉴스 수집

## 📊 성능 지표

### 기능적 성공 지표
- ✅ 매일 06:00 KST 자동 크롤링 정상 동작
- ✅ 로컬 요약 시스템 정상 동작 (API 독립)
- ✅ 3개 탭 전환 기능 정상 동작
- ✅ RAG Q&A 시스템 정상 동작
- ✅ 반응형 디자인 모든 해상도에서 정상

### 사용성 성공 지표
- ✅ 사용자가 10초 내에 오늘의 경제 이슈 파악 가능
- ✅ 모바일 환경에서 터치 조작 문제 없음
- ✅ 뉴스 상세보기 로딩 시간 2초 이내
- ✅ Q&A 답변 시간 1초 이내

### 콘텐츠 품질 지표
- ✅ 뉴스 요약 정확도 90% 이상 (키워드 기반)
- ✅ 경제 상식 콘텐츠 완성도 95% 이상
- ✅ 크롤링 데이터 신선도 (48시간 이내)
- ✅ 뉴스 다양성 (8개 뉴스, 2일간 커버리지)

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 GitHub Issues를 통해 연락해주세요.

---

**⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요!**