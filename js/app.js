// Main App - 애플리케이션 초기화 및 전역 관리
class App {
    constructor() {
        this.isInitialized = false;
        this.retryCount = 0;
        this.maxRetries = 3;
        this.init();
    }

    async init() {
        try {
            console.log('App initializing...');
            
            // 기본 설정
            this.setupApp();
            
            // 이벤트 리스너 등록
            this.bindGlobalEvents();
            
            // 초기 데이터 로딩
            await this.loadInitialData();
            
            // 오프라인 지원 설정
            this.setupOfflineSupport();
            
            this.isInitialized = true;
            console.log('App initialized successfully');
            
        } catch (error) {
            console.error('App initialization failed:', error);
            this.handleInitializationError(error);
        }
    }

    setupApp() {
        // 앱 버전 및 빌드 정보
        this.appInfo = {
            version: '1.0.0',
            buildDate: new Date().toISOString(),
            environment: this.getEnvironment()
        };

        // 성능 모니터링
        this.performance = {
            startTime: performance.now(),
            loadTimes: {}
        };

        // 사용자 설정
        this.userSettings = this.loadUserSettings();
    }

    bindGlobalEvents() {
        // 온라인/오프라인 상태 변경
        window.addEventListener('online', () => {
            this.handleOnlineStatusChange(true);
        });

        window.addEventListener('offline', () => {
            this.handleOnlineStatusChange(false);
        });

        // 페이지 가시성 변경 (탭 전환)
        document.addEventListener('visibilitychange', () => {
            this.handleVisibilityChange();
        });

        // 새로고침 버튼
        const refreshBtn = document.getElementById('refreshBtn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.handleRefresh();
            });
        }

        // 키보드 단축키
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardShortcuts(e);
        });
    }

    async loadInitialData() {
        const startTime = performance.now();
        
        try {
            // 뉴스 데이터 로딩
            const newsData = await window.newsLoader.loadNewsData();
            this.performance.loadTimes.news = performance.now() - startTime;

            // 데이터 검증
            if (!window.newsLoader.validateNewsData(newsData)) {
                throw new Error('Invalid news data format');
            }

            // 정규화된 데이터로 변환
            const normalizedData = window.newsLoader.normalizeNewsData(newsData);
            
            // 로컬 백업
            window.newsLoader.backupToLocal(normalizedData);

            console.log('Initial data loaded successfully');
            return normalizedData;

        } catch (error) {
            console.error('Failed to load initial data:', error);
            
            // 오프라인 모드에서 백업 데이터 사용
            if (!window.newsLoader.isOnline()) {
                const backupData = window.newsLoader.restoreFromLocal();
                if (backupData) {
                    console.log('Using backup data');
                    return backupData;
                }
            }
            
            throw error;
        }
    }

    setupOfflineSupport() {
        // Service Worker 등록 (향후 구현)
        if ('serviceWorker' in navigator) {
            // navigator.serviceWorker.register('/sw.js');
        }

        // 오프라인 상태 표시
        this.updateOfflineIndicator();
    }

    handleOnlineStatusChange(isOnline) {
        console.log(`Network status changed: ${isOnline ? 'online' : 'offline'}`);
        
        this.updateOfflineIndicator();
        
        if (isOnline && !this.isInitialized) {
            // 온라인 상태가 되면 재시도
            this.retryInitialization();
        }
    }

    handleVisibilityChange() {
        if (!document.hidden) {
            // 탭이 다시 활성화되면 데이터 새로고침
            this.refreshDataIfNeeded();
        }
    }

    handleRefresh() {
        console.log('Manual refresh triggered');
        
        // 새로고침 애니메이션
        const refreshBtn = document.getElementById('refreshBtn');
        if (refreshBtn) {
            refreshBtn.style.transform = 'rotate(180deg)';
            setTimeout(() => {
                refreshBtn.style.transform = 'rotate(0deg)';
            }, 300);
        }

        // 데이터 새로고침
        this.refreshData();
    }

    handleKeyboardShortcuts(e) {
        // Ctrl/Cmd + R: 새로고침
        if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
            e.preventDefault();
            this.handleRefresh();
        }
        
        // 숫자 키로 탭 전환
        if (e.key >= '1' && e.key <= '3') {
            const tabMap = {
                '1': 'home-tab',
                '2': 'news-tab',
                '3': 'tips-tab'
            };
            
            const tabId = tabMap[e.key];
            if (tabId && window.tabHandler) {
                window.tabHandler.switchTab(tabId);
            }
        }
    }

    async refreshData() {
        try {
            const result = await window.newsLoader.refreshData();
            
            if (result.success) {
                // 탭 핸들러에 새 데이터 알림
                if (window.tabHandler) {
                    window.tabHandler.loadTabData(window.tabHandler.currentTab);
                }
                
                this.showNotification('데이터가 새로고침되었습니다.', 'success');
            } else {
                throw new Error(result.error);
            }
        } catch (error) {
            console.error('Refresh failed:', error);
            this.showNotification('새로고침에 실패했습니다.', 'error');
        }
    }

    async refreshDataIfNeeded() {
        // 마지막 업데이트 시간 확인
        const lastUpdate = localStorage.getItem('lastDataUpdate');
        const now = Date.now();
        const updateInterval = 30 * 60 * 1000; // 30분

        if (!lastUpdate || (now - parseInt(lastUpdate)) > updateInterval) {
            await this.refreshData();
            localStorage.setItem('lastDataUpdate', now.toString());
        }
    }

    handleInitializationError(error) {
        this.retryCount++;
        
        if (this.retryCount < this.maxRetries) {
            console.log(`Retrying initialization (${this.retryCount}/${this.maxRetries})`);
            setTimeout(() => {
                this.init();
            }, 2000 * this.retryCount);
        } else {
            this.showErrorState(error);
        }
    }

    async retryInitialization() {
        if (this.retryCount < this.maxRetries) {
            this.retryCount++;
            await this.init();
        }
    }

    showErrorState(error) {
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.innerHTML = `
                <div class="container-fluid">
                    <div class="row">
                        <div class="col-12">
                            <div class="alert alert-danger text-center">
                                <i class="bi bi-exclamation-triangle-fill"></i>
                                <h4>앱을 불러올 수 없습니다</h4>
                                <p>네트워크 연결을 확인하고 다시 시도해주세요.</p>
                                <button class="btn btn-outline-danger" onclick="location.reload()">
                                    <i class="bi bi-arrow-clockwise"></i>
                                    다시 시도
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
    }

    showNotification(message, type = 'info') {
        // 간단한 토스트 알림 구현
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        toast.innerHTML = `
            <i class="bi bi-${this.getNotificationIcon(type)}"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(toast);
        
        // 애니메이션
        setTimeout(() => toast.classList.add('show'), 100);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => document.body.removeChild(toast), 300);
        }, 3000);
    }

    getNotificationIcon(type) {
        const icons = {
            'success': 'check-circle',
            'error': 'exclamation-triangle',
            'info': 'info-circle',
            'warning': 'exclamation-circle'
        };
        return icons[type] || 'info-circle';
    }

    updateOfflineIndicator() {
        const indicator = document.getElementById('offlineIndicator');
        if (!indicator) {
            // 오프라인 인디케이터 생성
            const offlineDiv = document.createElement('div');
            offlineDiv.id = 'offlineIndicator';
            offlineDiv.className = 'offline-indicator';
            offlineDiv.innerHTML = `
                <i class="bi bi-wifi-off"></i>
                <span>오프라인 모드</span>
            `;
            document.body.appendChild(offlineDiv);
        }

        const isOffline = !window.newsLoader.isOnline();
        const indicator = document.getElementById('offlineIndicator');
        
        if (indicator) {
            indicator.style.display = isOffline ? 'block' : 'none';
        }
    }

    loadUserSettings() {
        try {
            const settings = localStorage.getItem('userSettings');
            return settings ? JSON.parse(settings) : {
                theme: 'light',
                autoRefresh: true,
                notifications: true
            };
        } catch (error) {
            console.error('Failed to load user settings:', error);
            return {};
        }
    }

    saveUserSettings(settings) {
        try {
            localStorage.setItem('userSettings', JSON.stringify(settings));
            this.userSettings = { ...this.userSettings, ...settings };
        } catch (error) {
            console.error('Failed to save user settings:', error);
        }
    }

    getEnvironment() {
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'development';
        } else if (window.location.hostname.includes('github.io')) {
            return 'production';
        } else {
            return 'staging';
        }
    }

    // 성능 메트릭 수집
    getPerformanceMetrics() {
        const endTime = performance.now();
        return {
            ...this.performance,
            totalLoadTime: endTime - this.performance.startTime,
            memoryUsage: performance.memory ? {
                used: performance.memory.usedJSHeapSize,
                total: performance.memory.totalJSHeapSize,
                limit: performance.memory.jsHeapSizeLimit
            } : null
        };
    }
}

// 앱 초기화
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});

// 페이지 언로드 시 정리
window.addEventListener('beforeunload', () => {
    if (window.app) {
        console.log('Performance metrics:', window.app.getPerformanceMetrics());
    }
});
