// News Loader - 뉴스 데이터 로딩 및 관리
class NewsLoader {
    constructor() {
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5분 캐시
    }

    async loadNewsData() {
        const cacheKey = 'news-data';
        const cached = this.getCachedData(cacheKey);
        
        if (cached) {
            return cached;
        }

        try {
            const response = await fetch('data/news.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.setCachedData(cacheKey, data);
            return data;
        } catch (error) {
            console.error('Error loading news data:', error);
            throw error;
        }
    }

    async loadTipsData() {
        const cacheKey = 'tips-data';
        const cached = this.getCachedData(cacheKey);
        
        if (cached) {
            return cached;
        }

        try {
            const response = await fetch('data/finance-tips.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.setCachedData(cacheKey, data);
            return data;
        } catch (error) {
            console.error('Error loading tips data:', error);
            throw error;
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

    // 뉴스 데이터 검증
    validateNewsData(data) {
        if (!data || typeof data !== 'object') {
            return false;
        }

        // summary 필드 검증
        if (data.summary && typeof data.summary !== 'string') {
            return false;
        }

        // news 배열 검증
        if (data.news && Array.isArray(data.news)) {
            return data.news.every(news => 
                news.title && 
                news.source && 
                news.publishedAt
            );
        }

        return true;
    }

    // 뉴스 데이터 정규화
    normalizeNewsData(data) {
        if (!data) return null;

        const normalized = {
            summary: data.summary || '',
            news: [],
            lastUpdated: data.lastUpdated || new Date().toISOString()
        };

        if (data.news && Array.isArray(data.news)) {
            normalized.news = data.news.map(news => ({
                title: news.title || '제목 없음',
                content: news.content || '',
                summary: news.summary || '',
                source: news.source || '알 수 없음',
                url: news.url || '',
                publishedAt: news.publishedAt || new Date().toISOString(),
                category: news.category || '경제'
            }));
        }

        return normalized;
    }

    // 에러 처리
    handleError(error, context = '') {
        console.error(`NewsLoader Error ${context}:`, error);
        
        const errorMessages = {
            'network': '네트워크 연결을 확인해주세요.',
            'parse': '데이터를 처리하는 중 오류가 발생했습니다.',
            'validation': '데이터 형식이 올바르지 않습니다.',
            'timeout': '요청 시간이 초과되었습니다.'
        };

        let message = '알 수 없는 오류가 발생했습니다.';
        
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            message = errorMessages.network;
        } else if (error.name === 'SyntaxError') {
            message = errorMessages.parse;
        } else if (error.message.includes('validation')) {
            message = errorMessages.validation;
        }

        return {
            success: false,
            error: message,
            context: context
        };
    }

    // 데이터 새로고침
    async refreshData() {
        this.clearCache();
        try {
            const newsData = await this.loadNewsData();
            const tipsData = await this.loadTipsData();
            
            return {
                success: true,
                news: newsData,
                tips: tipsData
            };
        } catch (error) {
            return this.handleError(error, 'refresh');
        }
    }

    // 오프라인 지원
    isOnline() {
        return navigator.onLine;
    }

    // 데이터 백업 (로컬 스토리지)
    backupToLocal(data) {
        try {
            localStorage.setItem('news-backup', JSON.stringify({
                data: data,
                timestamp: Date.now()
            }));
            return true;
        } catch (error) {
            console.error('Failed to backup data:', error);
            return false;
        }
    }

    // 로컬 백업에서 복원
    restoreFromLocal() {
        try {
            const backup = localStorage.getItem('news-backup');
            if (backup) {
                const parsed = JSON.parse(backup);
                const age = Date.now() - parsed.timestamp;
                
                // 24시간 이내 백업만 사용
                if (age < 24 * 60 * 60 * 1000) {
                    return parsed.data;
                }
            }
            return null;
        } catch (error) {
            console.error('Failed to restore from backup:', error);
            return null;
        }
    }
}

// 전역 NewsLoader 인스턴스 생성
window.newsLoader = new NewsLoader();
