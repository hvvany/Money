// Tab Handler - 탭 전환 및 네비게이션 관리
class TabHandler {
    constructor() {
        this.currentTab = 'home-tab';
        this.tabContents = document.querySelectorAll('.tab-content');
        this.navItems = document.querySelectorAll('.nav-item');
        this.init();
    }

    init() {
        this.bindEvents();
        this.setCurrentDate();
    }

    bindEvents() {
        // Bottom navigation click events
        this.navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                const tabId = e.currentTarget.getAttribute('data-tab');
                this.switchTab(tabId);
            });
        });

        // Refresh button event
        const refreshBtn = document.getElementById('refreshBtn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.refreshCurrentTab();
            });
        }
    }

    switchTab(tabId) {
        // Remove active class from all tabs and nav items
        this.tabContents.forEach(tab => {
            tab.classList.remove('active');
        });
        
        this.navItems.forEach(item => {
            item.classList.remove('active');
        });

        // Add active class to selected tab and nav item
        const targetTab = document.getElementById(tabId);
        const targetNavItem = document.querySelector(`[data-tab="${tabId}"]`);
        
        if (targetTab && targetNavItem) {
            targetTab.classList.add('active');
            targetNavItem.classList.add('active');
            this.currentTab = tabId;
            
            // Load data for the active tab
            this.loadTabData(tabId);
        }
    }

    loadTabData(tabId) {
        switch(tabId) {
            case 'home-tab':
                this.loadHomeData();
                break;
            case 'news-tab':
                this.loadNewsData();
                break;
            case 'tips-tab':
                this.loadTipsData();
                break;
        }
    }

    async loadHomeData() {
        const summaryContent = document.getElementById('summaryContent');
        if (!summaryContent) return;

        try {
            // Show loading state
            summaryContent.innerHTML = `
                <div class="loading-spinner">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p>오늘의 경제 이슈를 불러오는 중...</p>
                </div>
            `;

            // Load news data
            const response = await fetch('data/news.json');
            if (!response.ok) {
                throw new Error('뉴스 데이터를 불러올 수 없습니다.');
            }
            
            const data = await response.json();
            
            // 요약이 있으면 표시, 없으면 뉴스 제목들로 요약 생성
            let summary = data.summary;
            if (!summary || summary.trim() === '' || summary.includes('오류가 발생했습니다')) {
                if (data.news && data.news.length > 0) {
                    summary = this.generateSummaryFromNews(data.news);
                } else {
                    summary = "오늘의 경제 이슈를 불러오는 중입니다.";
                }
            }
            
            // 마크다운 형식을 HTML로 변환
            const formattedSummary = this.formatSummaryText(summary);
            summaryContent.innerHTML = `
                <div class="summary-text">
                    ${formattedSummary}
                </div>
            `;
        } catch (error) {
            console.error('Error loading home data:', error);
            summaryContent.innerHTML = `
                <div class="alert alert-warning">
                    <i class="bi bi-exclamation-triangle"></i>
                    데이터를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.
                </div>
            `;
        }
    }

    generateSummaryFromNews(newsList) {
        if (!newsList || newsList.length === 0) {
            return "오늘의 경제 이슈를 불러오는 중입니다.";
        }

        const titles = newsList.slice(0, 5).map(news => news.title);
        
        // 주요 키워드 추출
        const keywords = [];
        titles.forEach(title => {
            if (title.includes('부동산') || title.includes('아파트')) keywords.push('부동산');
            if (title.includes('주가') || title.includes('증시') || title.includes('코스피')) keywords.push('주식시장');
            if (title.includes('금리') || title.includes('중앙은행')) keywords.push('금리정책');
            if (title.includes('경기') || title.includes('성장')) keywords.push('경기동향');
            if (title.includes('APEC') || title.includes('정상회의')) keywords.push('국제정치');
        });

        const uniqueKeywords = [...new Set(keywords)];
        
        let summary = "📈 **오늘의 주요 경제 이슈**\n\n";
        
        if (uniqueKeywords.length > 0) {
            summary += `주요 관심사: ${uniqueKeywords.join(', ')}\n\n`;
        }
        
        summary += "**주요 뉴스:**\n";
        titles.forEach((title, index) => {
            const shortTitle = title.length > 60 ? title.substring(0, 60) + "..." : title;
            summary += `${index + 1}. ${shortTitle}\n`;
        });
        
        return summary;
    }

    formatSummaryText(text) {
        // 마크다운 형식을 HTML로 변환
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // **텍스트** -> <strong>텍스트</strong>
            .replace(/\n\n/g, '</p><p class="summary-sentence">') // 이중 줄바꿈을 문단 구분으로
            .replace(/\n/g, '<br>') // 단일 줄바꿈을 <br>로
            .replace(/^/, '<p class="summary-sentence">') // 시작에 <p> 태그 추가
            .replace(/$/, '</p>'); // 끝에 </p> 태그 추가
    }

    async loadNewsData() {
        const newsList = document.getElementById('newsList');
        if (!newsList) return;

        try {
            // Show loading state
            newsList.innerHTML = `
                <div class="loading-spinner">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p>뉴스를 불러오는 중...</p>
                </div>
            `;

            // Load news data
            const response = await fetch('data/news.json');
            if (!response.ok) {
                throw new Error('뉴스 데이터를 불러올 수 없습니다.');
            }
            
            const data = await response.json();
            
            if (data.news && data.news.length > 0) {
                newsList.innerHTML = data.news.map((news, index) => `
                    <div class="news-card" data-news-index="${index}">
                        <div class="news-title">${news.title}</div>
                        <div class="news-meta">
                            <span class="news-source">${news.source}</span>
                            <span class="news-time">${this.formatTime(news.publishedAt)}</span>
                        </div>
                    </div>
                `).join('');

                // Add click events to news cards
                this.bindNewsCardEvents(data.news);
            } else {
                newsList.innerHTML = `
                    <div class="alert alert-info">
                        <i class="bi bi-info-circle"></i>
                        오늘의 뉴스가 아직 준비되지 않았습니다.
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error loading news data:', error);
            newsList.innerHTML = `
                <div class="alert alert-warning">
                    <i class="bi bi-exclamation-triangle"></i>
                    뉴스를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.
                </div>
            `;
        }
    }

    async loadTipsData() {
        const knowledgeCategories = document.getElementById('knowledgeCategories');
        if (!knowledgeCategories) return;

        try {
            // Show loading state
            knowledgeCategories.innerHTML = `
                <div class="rag-loading">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p>경제 상식을 불러오는 중...</p>
                </div>
            `;

            // RAG system is already initialized (static data)

            // Load categories and knowledge
            const categoriesData = window.ragHandler.getCategories();
            
            if (categoriesData.categories && categoriesData.categories.length > 0) {
                let html = '';
                
                for (const category of categoriesData.categories) {
                    const knowledgeData = window.ragHandler.getKnowledgeByCategory(category);
                    
                    if (knowledgeData.knowledge && knowledgeData.knowledge.length > 0) {
                        html += `
                            <div class="category-section">
                                <div class="category-title">
                                    <i class="bi bi-${this.getCategoryIcon(category)}"></i>
                                    ${category}
                                </div>
                                <div class="knowledge-items">
                                    ${knowledgeData.knowledge.map(item => `
                                        <div class="knowledge-item" data-knowledge-id="${item.id}">
                                            <div class="knowledge-item-title">${item.title}</div>
                                            <div class="knowledge-item-content">${item.content}</div>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                        `;
                    }
                }
                
                knowledgeCategories.innerHTML = html;
                
                // Add click events to knowledge items
                this.bindKnowledgeItemEvents();
                
                // Setup Q&A functionality
                this.setupQAFunctionality();
                
            } else {
                knowledgeCategories.innerHTML = `
                    <div class="alert alert-info">
                        <i class="bi bi-info-circle"></i>
                        경제 상식 콘텐츠가 아직 준비되지 않았습니다.
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error loading tips data:', error);
            knowledgeCategories.innerHTML = `
                <div class="rag-error">
                    <i class="bi bi-exclamation-triangle"></i>
                    경제 상식을 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.
                </div>
            `;
        }
    }

    bindNewsCardEvents(newsData) {
        const newsCards = document.querySelectorAll('.news-card');
        newsCards.forEach((card, index) => {
            card.addEventListener('click', () => {
                this.showNewsModal(newsData[index]);
            });
        });
    }

    bindKnowledgeItemEvents() {
        const knowledgeItems = document.querySelectorAll('.knowledge-item');
        knowledgeItems.forEach(item => {
            item.addEventListener('click', () => {
                item.classList.toggle('expanded');
            });
        });
    }

    setupQAFunctionality() {
        // 질문 제안 태그 생성
        this.setupSuggestedQuestions();
        
        // 질문 입력 이벤트
        const questionInput = document.getElementById('questionInput');
        const askButton = document.getElementById('askButton');
        const clearAnswerButton = document.getElementById('clearAnswer');
        
        if (questionInput && askButton) {
            // 엔터키로 질문하기
            questionInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.askQuestion();
                }
            });
            
            // 버튼 클릭으로 질문하기
            askButton.addEventListener('click', () => {
                this.askQuestion();
            });
        }
        
        if (clearAnswerButton) {
            clearAnswerButton.addEventListener('click', () => {
                this.clearAnswer();
            });
        }
    }

    setupSuggestedQuestions() {
        const suggestedQuestions = document.getElementById('suggestedQuestions');
        if (!suggestedQuestions) return;
        
        const questions = window.ragHandler.getSuggestedQuestions();
        suggestedQuestions.innerHTML = questions.map(question => 
            `<button class="question-tag" data-question="${question}">${question}</button>`
        ).join('');
        
        // 질문 태그 클릭 이벤트
        const questionTags = document.querySelectorAll('.question-tag');
        questionTags.forEach(tag => {
            tag.addEventListener('click', () => {
                const question = tag.getAttribute('data-question');
                document.getElementById('questionInput').value = question;
                this.askQuestion();
            });
        });
    }

    async askQuestion() {
        const questionInput = document.getElementById('questionInput');
        const answerSection = document.getElementById('answerSection');
        const answerContent = document.getElementById('answerContent');
        
        if (!questionInput || !answerSection || !answerContent) return;
        
        const question = questionInput.value.trim();
        if (!question) return;
        
        // 로딩 상태 표시
        answerContent.innerHTML = `
            <div class="rag-loading">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p>답변을 생성하는 중...</p>
            </div>
        `;
        answerSection.style.display = 'block';
        
        try {
            // RAG 시스템에 질문
            const result = await window.ragHandler.askQuestion(question);
            
            if (result.success) {
                answerContent.innerHTML = `
                    <div class="answer-text">
                        ${result.data.answer}
                    </div>
                    ${result.data.related_knowledge && result.data.related_knowledge.length > 0 ? `
                        <div class="related-knowledge mt-3">
                            <h6>관련 정보:</h6>
                            <ul class="list-unstyled">
                                ${result.data.related_knowledge.map(item => `
                                    <li class="mb-2">
                                        <small class="text-muted">
                                            <strong>${item.metadata.title}</strong>: ${item.content.substring(0, 100)}...
                                        </small>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>
                    ` : ''}
                `;
            } else {
                answerContent.innerHTML = `
                    <div class="rag-error">
                        <i class="bi bi-exclamation-triangle"></i>
                        ${result.error || '답변을 생성할 수 없습니다.'}
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error asking question:', error);
            answerContent.innerHTML = `
                <div class="rag-error">
                    <i class="bi bi-exclamation-triangle"></i>
                    질문 처리 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.
                </div>
            `;
        }
    }

    clearAnswer() {
        const answerSection = document.getElementById('answerSection');
        const questionInput = document.getElementById('questionInput');
        
        if (answerSection) {
            answerSection.style.display = 'none';
        }
        
        if (questionInput) {
            questionInput.value = '';
        }
    }

    getCategoryIcon(category) {
        const iconMap = {
            '연금': 'piggy-bank',
            '투자': 'graph-up',
            '저축': 'bank',
            '보험': 'shield-check'
        };
        return iconMap[category] || 'lightbulb';
    }

    showNewsModal(news) {
        const modal = new bootstrap.Modal(document.getElementById('newsModal'));
        const modalContent = document.getElementById('newsModalContent');
        const originalLink = document.getElementById('originalLink');

        modalContent.innerHTML = `
            <div class="news-detail-title">${news.title}</div>
            <div class="news-detail-summary">${news.summary || news.content}</div>
            <div class="news-detail-meta">
                <span class="news-source">${news.source}</span>
                <span class="news-time">${this.formatTime(news.publishedAt)}</span>
            </div>
        `;

        if (news.url) {
            originalLink.href = news.url;
            originalLink.style.display = 'inline-block';
        } else {
            originalLink.style.display = 'none';
        }

        modal.show();
    }

    getTipIcon(category) {
        const iconMap = {
            '연금저축': 'piggy-bank',
            '주식': 'graph-up',
            'ISA': 'wallet2',
            'ETF': 'bar-chart',
            '채권': 'receipt',
            '펀드': 'pie-chart',
            '예적금': 'bank'
        };
        return iconMap[category] || 'lightbulb';
    }

    formatTime(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
        
        if (diffInHours < 1) {
            return '방금 전';
        } else if (diffInHours < 24) {
            return `${diffInHours}시간 전`;
        } else {
            return date.toLocaleDateString('ko-KR', {
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        }
    }

    setCurrentDate() {
        const dateElement = document.getElementById('currentDate');
        if (dateElement) {
            const now = new Date();
            const options = {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                weekday: 'long'
            };
            dateElement.textContent = now.toLocaleDateString('ko-KR', options);
        }
    }

    refreshCurrentTab() {
        // Add rotation animation to refresh button
        const refreshBtn = document.getElementById('refreshBtn');
        if (refreshBtn) {
            refreshBtn.style.transform = 'rotate(180deg)';
            setTimeout(() => {
                refreshBtn.style.transform = 'rotate(0deg)';
            }, 300);
        }

        // Reload current tab data
        this.loadTabData(this.currentTab);
    }
}

// Initialize tab handler when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.tabHandler = new TabHandler();
});
