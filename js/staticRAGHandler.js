// Static RAG Handler - 정적 데이터 기반 경제 상식 시스템
class StaticRAGHandler {
    constructor() {
        this.isInitialized = true;
        this.financeKnowledge = this.getFinanceKnowledgeData();
    }

    getFinanceKnowledgeData() {
        return [
            {
                "id": "pension_savings",
                "title": "연금저축",
                "content": "연금저축은 노후 준비를 위한 장기 저축 상품입니다. 매년 400만원까지 세제혜택을 받으며 납입할 수 있고, 55세 이후 연금으로 수령하거나 일시금으로 받을 수 있습니다. 개인연금저축(IRP)과 퇴직연금(401k) 등이 있으며, 장기간 꾸준히 납입할수록 더 큰 혜택을 받을 수 있습니다.",
                "category": "연금",
                "keywords": ["연금저축", "개인연금", "퇴직연금", "IRP", "연금보험", "세제혜택", "노후준비"]
            },
            {
                "id": "stock_investment",
                "title": "주식 투자",
                "content": "주식은 기업의 일부를 소유하는 증권으로, 기업의 성장과 함께 주가가 상승할 가능성이 있습니다. 코스피와 코스닥 시장에서 거래되며, 배당을 통해 수익을 얻을 수도 있습니다. 하지만 주가는 변동성이 크므로 투자 전 충분한 분석과 리스크 관리가 필요합니다.",
                "category": "투자",
                "keywords": ["주식", "주식투자", "증권", "코스피", "코스닥", "ETF", "배당", "투자전략"]
            },
            {
                "id": "isa_account",
                "title": "ISA (개인종합자산관리계좌)",
                "content": "ISA는 다양한 금융상품을 하나의 계좌에서 관리할 수 있는 통합 투자계좌입니다. 연간 2천만원까지 투자할 수 있으며, 3년 이상 보유 시 세제혜택을 받을 수 있습니다. 주식, 채권, 펀드, ETF 등 다양한 상품에 투자할 수 있어 포트폴리오 분산투자에 유리합니다.",
                "category": "투자",
                "keywords": ["ISA", "개인종합자산관리계좌", "세제혜택", "투자계좌", "포트폴리오", "통합관리"]
            },
            {
                "id": "etf_investment",
                "title": "ETF (상장지수펀드)",
                "content": "ETF는 주식시장에서 거래되는 펀드로, 특정 지수를 추종합니다. 개별 주식보다 리스크가 분산되고, 수수료가 낮으며, 실시간 거래가 가능합니다. S&P 500, 나스닥, KOSPI 200 등 다양한 지수를 추종하는 ETF가 있어 투자 목적에 맞게 선택할 수 있습니다.",
                "category": "투자",
                "keywords": ["ETF", "상장지수펀드", "인덱스펀드", "패시브투자", "분산투자", "수수료"]
            },
            {
                "id": "bond_investment",
                "title": "채권 투자",
                "content": "채권은 정부나 기업이 발행하는 차용증서로, 만기일에 원금과 이자를 받을 수 있습니다. 주식보다 안정적이지만 수익률은 낮은 편입니다. 국채, 회사채, 채권펀드 등이 있으며, 금리 변동에 민감하므로 투자 시점을 고려해야 합니다.",
                "category": "투자",
                "keywords": ["채권", "국채", "회사채", "채권펀드", "안전자산", "고정수익", "금리"]
            },
            {
                "id": "fund_investment",
                "title": "펀드 투자",
                "content": "펀드는 여러 투자자로부터 자금을 모아 전문가가 운용하는 투자상품입니다. 전문가가 대신 투자 운용하며, 소액으로도 분산 투자 가능합니다. 액티브 펀드와 패시브 펀드로 구분되며, 언제든 환매 가능한 유동성을 제공합니다.",
                "category": "투자",
                "keywords": ["펀드", "투자신탁", "자산운용", "액티브펀드", "패시브펀드", "분산투자", "전문가운용"]
            },
            {
                "id": "deposit_savings",
                "title": "예금과 적금",
                "content": "예금과 적금은 은행에 자금을 맡기고 이자를 받는 가장 기본적인 금융상품입니다. 정기예금은 일정 기간 동안 자금을 맡기고 이자를 받으며, 정기적금은 매월 일정 금액을 납입하고 만기 시 이자를 받습니다. 안전성과 원금 보장이 장점이지만 수익률은 낮은 편입니다.",
                "category": "저축",
                "keywords": ["예금", "적금", "정기예금", "정기적금", "자유적금", "이자", "저축"]
            },
            {
                "id": "insurance_products",
                "title": "보험 상품",
                "content": "보험은 위험을 분산시키는 금융상품으로, 다양한 위험에 대비할 수 있습니다. 생명보험과 손해보험으로 구분되며, 보장과 저축 기능을 동시에 제공합니다. 보험 선택 시에는 보장 필요성, 보험료 부담, 보장 내용, 보험사 신뢰도를 고려해야 합니다.",
                "category": "보험",
                "keywords": ["보험", "생명보험", "손해보험", "연금보험", "종신보험", "보장", "보험료"]
            },
            {
                "id": "real_estate_investment",
                "title": "부동산 투자",
                "content": "부동산 투자는 토지, 건물 등 부동산에 투자하여 수익을 얻는 투자 방법입니다. 실물 자산으로 인플레이션에 강하며, 임대 수익과 매매 수익을 동시에 추구할 수 있습니다. 직접 투자와 REITs, 부동산펀드 등을 통한 간접 투자 방법이 있습니다.",
                "category": "투자",
                "keywords": ["부동산", "아파트", "오피스텔", "REITs", "부동산펀드", "임대", "실물자산"]
            },
            {
                "id": "cryptocurrency",
                "title": "암호화폐 투자",
                "content": "암호화폐는 블록체인 기술을 기반으로 한 디지털 자산입니다. 중앙은행이나 정부의 통제 없이 운영되며, 24시간 거래가 가능합니다. 높은 변동성과 수익 가능성을 가지고 있지만, 규제 리스크와 보안 위험도 고려해야 합니다.",
                "category": "투자",
                "keywords": ["암호화폐", "비트코인", "이더리움", "가상화폐", "블록체인", "디지털자산", "변동성"]
            }
        ];
    }

    searchKnowledge(query, topK = 3) {
        const queryLower = query.toLowerCase();
        const scoredItems = [];

        for (const item of this.financeKnowledge) {
            let score = 0;

            // 제목에서 키워드 매칭
            if (item.title.toLowerCase().includes(queryLower)) {
                score += 3;
            }

            // 키워드에서 매칭
            if (item.keywords.some(keyword => keyword.toLowerCase().includes(queryLower))) {
                score += 2;
            }

            // 내용에서 키워드 매칭
            if (item.content.toLowerCase().includes(queryLower)) {
                score += 1;
            }

            if (score > 0) {
                scoredItems.push({
                    item: item,
                    score: score
                });
            }
        }

        // 점수순으로 정렬하고 상위 k개 반환
        scoredItems.sort((a, b) => b.score - a.score);
        return scoredItems.slice(0, topK).map(item => item.item);
    }

    generateAnswer(question) {
        const knowledgeItems = this.searchKnowledge(question, 3);
        
        if (knowledgeItems.length === 0) {
            return "죄송합니다. 관련 정보를 찾을 수 없습니다. 다른 질문을 해주세요.";
        }

        // 가장 관련성 높은 정보를 기반으로 답변 생성
        const mainItem = knowledgeItems[0];
        let answer = `**${mainItem.title}**에 대해 설명드리겠습니다.\n\n`;
        answer += mainItem.content;

        if (knowledgeItems.length > 1) {
            answer += `\n\n**관련 정보:**\n`;
            knowledgeItems.slice(1).forEach(item => {
                answer += `• ${item.title}: ${item.content.substring(0, 100)}...\n`;
            });
        }

        return answer;
    }

    async askQuestion(question) {
        return {
            success: true,
            data: {
                question: question,
                answer: this.generateAnswer(question),
                related_knowledge: this.searchKnowledge(question, 3).map(item => ({
                    metadata: { title: item.title },
                    content: item.content
                })),
                timestamp: new Date().toISOString()
            }
        };
    }

    getCategories() {
        const categories = [...new Set(this.financeKnowledge.map(item => item.category))];
        return {
            categories: categories,
            count: categories.length
        };
    }

    getKnowledgeByCategory(category) {
        const knowledge = this.financeKnowledge.filter(item => item.category === category);
        return {
            category: category,
            knowledge: knowledge,
            count: knowledge.length
        };
    }

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

// 전역 Static RAG 핸들러 인스턴스 생성
window.ragHandler = new StaticRAGHandler();
