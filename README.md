# 경제 뉴스 서비스

매일 아침 최신 경제 이슈를 AI로 요약하여 모바일에서 편리하게 볼 수 있는 웹 서비스입니다.

## 🚀 주요 기능

### 📱 3개 탭 구조
- **홈 탭**: 오늘의 경제 이슈 5문장 요약
- **뉴스 탭**: 최신 경제 뉴스 10개 목록 및 상세보기
- **경제상식 탭**: 금융상품별 설명 (연금저축, 주식, ISA 등)

### 🤖 AI 자동화
- **GitHub Actions**: 매일 06:00 KST 자동 크롤링
- **OpenAI API**: 뉴스 요약 및 경제상식 콘텐츠 생성
- **다중 소스**: 네이버, 한국경제, 매일경제, 연합뉴스 통합

### 📱 모바일 최적화
- **반응형 디자인**: 320px ~ 1920px 지원
- **터치 친화적**: 하단 고정 탭바
- **오프라인 지원**: 로컬 캐싱 및 백업

## 🛠 기술 스택

### 프론트엔드
- **HTML5** + **CSS3** + **Vanilla JavaScript**
- **Bootstrap 5**: 반응형 컴포넌트
- **Bootstrap Icons**: 아이콘

### 백엔드/자동화
- **GitHub Actions**: 자동 크롤링 워크플로우
- **Python 3.9+**: 크롤링 및 데이터 처리
- **BeautifulSoup4**: HTML 파싱
- **OpenAI API**: 뉴스 요약 및 콘텐츠 생성

### 데이터 소스
- 네이버 뉴스 (경제 섹션)
- 한국경제신문
- 매일경제신문
- 연합뉴스 (경제 섹션)

## 📁 프로젝트 구조

```
/
├── index.html              # 메인 페이지
├── css/
│   └── style.css          # 커스텀 스타일
├── js/
│   ├── app.js             # 메인 앱 로직
│   ├── newsLoader.js      # 뉴스 데이터 로딩
│   └── tabHandler.js      # 탭 전환 로직
├── data/
│   ├── news.json          # 크롤링된 뉴스 (자동 생성)
│   └── finance-tips.json  # 경제상식 콘텐츠
├── .github/
│   └── workflows/
│       └── crawl-news.yml # 자동 크롤링 워크플로우
└── scripts/
    ├── crawler.py         # 뉴스 크롤링 스크립트
    ├── summarizer.py      # OpenAI 요약 스크립트
    ├── generate_finance_tips.py # 경제상식 생성 스크립트
    └── requirements.txt   # Python 의존성
```

## 🚀 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd economic-news-service
```

### 2. GitHub Pages 배포
1. GitHub 저장소에 코드 푸시
2. Settings > Pages에서 GitHub Pages 활성화
3. Source를 "Deploy from a branch" 선택
4. Branch를 "main" 선택

### 3. OpenAI API 키 설정
1. GitHub 저장소 Settings > Secrets and variables > Actions
2. "New repository secret" 클릭
3. Name: `OPENAI_API_KEY`
4. Value: OpenAI API 키 입력

### 4. 자동 크롤링 활성화
- GitHub Actions가 자동으로 매일 06:00 KST에 실행됩니다
- 수동 실행: Actions 탭 > "Daily News Crawler" > "Run workflow"

## 📱 사용법

### 웹 브라우저에서 접속
- GitHub Pages URL로 접속
- 모바일 브라우저에서 최적화된 경험

### 키보드 단축키
- `1`: 홈 탭
- `2`: 뉴스 탭  
- `3`: 경제상식 탭
- `Ctrl/Cmd + R`: 새로고침

## 🔧 개발 및 커스터마이징

### 크롤링 소스 추가
`scripts/crawler.py`에서 새로운 뉴스 소스 추가:

```python
def crawl_new_source(self):
    # 새로운 뉴스 소스 크롤링 로직
    pass
```

### 요약 프롬프트 수정
`scripts/summarizer.py`에서 OpenAI 프롬프트 커스터마이징:

```python
prompt = f"""
사용자 정의 프롬프트
{news_content}
"""
```

### UI 커스터마이징
`css/style.css`에서 색상, 폰트, 레이아웃 수정:

```css
:root {
  --primary-color: #667eea;
  --secondary-color: #764ba2;
}
```

## 📊 성능 최적화

### 캐싱 전략
- **메모리 캐시**: 5분 TTL
- **로컬 스토리지**: 24시간 백업
- **CDN**: Bootstrap, 아이콘 등 외부 리소스

### 로딩 최적화
- **지연 로딩**: 탭별 데이터 로딩
- **압축**: JSON 데이터 최적화
- **이미지**: WebP 형식 사용

## 🐛 문제 해결

### 자주 발생하는 문제

#### 1. 뉴스 데이터가 로드되지 않음
- GitHub Actions 실행 상태 확인
- OpenAI API 키 설정 확인
- 네트워크 연결 상태 확인

#### 2. 크롤링 실패
- 뉴스 사이트 구조 변경 가능성
- User-Agent 또는 요청 헤더 업데이트 필요
- 요청 간격 조절 (rate limiting)

#### 3. 요약 생성 실패
- OpenAI API 키 유효성 확인
- API 사용량 한도 확인
- 프롬프트 길이 제한 확인

### 로그 확인
- GitHub Actions 로그: Actions 탭에서 확인
- 브라우저 콘솔: F12 > Console 탭
- 네트워크 탭: F12 > Network 탭

## 📈 향후 계획

### 단기 계획
- [ ] 다크 모드 지원
- [ ] 푸시 알림 기능
- [ ] 북마크 기능
- [ ] 검색 기능

### 장기 계획
- [ ] PWA (Progressive Web App) 지원
- [ ] 사용자 맞춤 설정
- [ ] 뉴스 카테고리 필터링
- [ ] 소셜 공유 기능

## 📄 라이선스

이 프로젝트는 개인 사용 목적으로 제작되었습니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요.

---

**Made with ❤️ for better economic news consumption**
