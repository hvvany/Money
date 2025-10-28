// RAG Handler - 경제 상식 RAG 시스템 관리
class RAGHandler {
    constructor() {
        this.apiBaseUrl = 'http://localhost:5000/api';
        this.isInitialized = false;
        this.cache = new Map();
        this.cacheTimeout = 10 * 60 * 1000; // 10분 캐시
    }

    async initialize() {
        try {
            // API 서버 상태 확인
            const response = await fetch(`${this.apiBaseUrl}/health`);
            if (response.ok) {
                this.isInitialized = true;
                console.log('RAG system initialized successfully');
                return true;
            } else {
                throw new Error('RAG API server not available');
            }
        } catch (error) {
            console.error('Failed to initialize RAG system:', error);
            this.isInitialized = false;
            return false;
        }
    }

    async askQuestion(question) {
        if (!this.isInitialized) {
            return {
                success: false,
                error: 'RAG system not initialized'
            };
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/ask`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return {
                success: true,
                data: data
            };
        } catch (error) {
            console.error('Error asking question:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }

    async getCategories() {
        const cacheKey = 'categories';
        const cached = this.getCachedData(cacheKey);
        
        if (cached) {
            return cached;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/categories`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.setCachedData(cacheKey, data);
            return data;
        } catch (error) {
            console.error('Error getting categories:', error);
            return {
                categories: [],
                count: 0
            };
        }
    }

    async getKnowledgeByCategory(category) {
        const cacheKey = `knowledge_${category}`;
        const cached = this.getCachedData(cacheKey);
        
        if (cached) {
            return cached;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/knowledge/${encodeURIComponent(category)}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.setCachedData(cacheKey, data);
            return data;
        } catch (error) {
            console.error('Error getting knowledge by category:', error);
            return {
                category: category,
                knowledge: [],
                count: 0
            };
        }
    }

    async searchKnowledge(query, topK = 5) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/search`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    query: query,
                    top_k: topK
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return {
                success: true,
                data: data
            };
        } catch (error) {
            console.error('Error searching knowledge:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }

    async getRandomKnowledge() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/random`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return {
                success: true,
                data: data.knowledge
            };
        } catch (error) {
            console.error('Error getting random knowledge:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }

    getCachedData(key) {
        const cached = this.cache.get(key);
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.data;
        }
        return null;
    }

    setCachedData(key, data) {
        this.cache.set(key, {
            data: data,
            timestamp: Date.now()
        });
    }

    clearCache() {
        this.cache.clear();
    }

    // 질문 제안 목록
    getSuggestedQuestions() {
        return [
            "연금저축이 무엇인가요?",
            "주식 투자할 때 주의사항은?",
            "ISA 계좌의 장점은 무엇인가요?",
            "ETF와 개별 주식의 차이점은?",
            "채권 투자의 리스크는 무엇인가요?",
            "펀드 투자는 어떻게 시작하나요?",
            "예금과 적금의 차이점은?",
            "보험을 선택할 때 고려사항은?",
            "부동산 투자의 장단점은?",
            "암호화폐 투자 시 주의사항은?"
        ];
    }
}

// 전역 RAG 핸들러 인스턴스 생성
window.ragHandler = new RAGHandler();
