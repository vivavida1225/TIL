<template>
  <div class="hypothesis-dashboard">
    <div class="dashboard-header">
      <h4>가설 검정 대시보드 (인터랙티브 UI 확장)</h4>
      <p class="hypothesis-text">
        <strong>💡 검정 가설:</strong> "공유/조회수" 지표가 "댓글/조회수" 지표보다 상대적으로 높은 카테고리는 
        연예, 스포츠 등 젊은 층이 능동적으로 확산시키는 문화 관련 카테고리일 것이다.
      </p>
      
      <div class="interactive-filter-panel">
        <label for="topNInput" class="filter-label">📈 기사 수 기준 상위 N개 카테고리만 필터링:</label>
        <div class="input-wrapper">
          <input 
            id="topNInput"
            type="number" 
            v-model.number="topN" 
            min="1" 
            :max="maxCategories"
            @input="updateDashboard"
            class="top-n-input"
          />
          <span class="filter-hint">(현재 데이터셋 전체 카테고리 수: 총 {{ maxCategories }}개)</span>
        </div>
      </div>
    </div>

    <div class="chart-grid">
      <div class="chart-card">
        <h5 class="chart-title">1. 카테고리별 평균 [공유 수 / 조회수] 비율</h5>
        <canvas ref="canvas1"></canvas>
      </div>

      <div class="chart-card">
        <h5 class="chart-title">2. 카테고리별 평균 [댓글 수 / 조회수] 비율</h5>
        <canvas ref="canvas2"></canvas>
      </div>

      <div class="chart-card">
        <h5 class="chart-title">3. 지표 간 비율 [(공유/조회) ÷ (댓글/조회)]</h5>
        <canvas ref="canvas3"></canvas>
      </div>

      <div class="chart-card highlight-card">
        <h5 class="chart-title">4. 가설 검정 최종 결과 (내림차순 정렬)</h5>
        <canvas ref="canvas4"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Chart } from 'chart.js/auto';
// 규칙에 근거한 @/ 절대 경로 형식 데이터 로드
import newsDataRaw from '@/assets/news_politics.jsonl?raw';

// 4개의 차트 Canvas DOM 매핑 변수
const canvas1 = ref(null);
const canvas2 = ref(null);
const canvas3 = ref(null);
const canvas4 = ref(null);

// 실시간 차트 인스턴스 참조 변수 (메모리 누수 및 인스턴스 중복 방지용 고정 캐싱)
let chart1 = null;
let chart2 = null;
let chart3 = null;
let chart4 = null;

// 파싱 원본 데이터 캐싱 저장소
let cachedAllData = [];

// 반응형 필터 상태 변수
const topN = ref(10);          // 초기 렌더링 시 노출할 상위 카테고리 개수 기본값
const maxCategories = ref(0);  // 데이터 파싱 후 추출된 전체 고유 카테고리 총 개수

// 차트 1, 2, 3 연동용 가공 데이터 상태 변수
const filteredCategories = ref([]);
const sharesPerViewData = ref([]);
const commentsPerViewData = ref([]);
const ratioData = ref([]);

// 차트 4 연동용 내림차순 가공 데이터 상태 변수
const sortedCategories = ref([]);
const sortedRatioData = ref([]);

// 1. [최초 1회 실행] 원본 JSONL 문자열 고속 파싱 및 총 카테고리 수 진단
const initRawData = () => {
  try {
    const lines = newsDataRaw.split('\n').filter(line => line.trim() !== '');
    cachedAllData = lines.map(line => JSON.parse(line));
    
    // 전체 고유 카테고리 목록 추출 후 최대 개수 확보
    const allCats = [...new Set(cachedAllData.map(item => item.category).filter(Boolean))];
    maxCategories.value = allCats.length;
    
    // 예외 방어코드: 초기값이 최대값보다 크면 최대값으로 바인딩
    if (topN.value > maxCategories.value) {
      topN.value = maxCategories.value;
    }
  } catch (error) {
    console.error('F311 데이터 초기 파싱 에러:', error);
  }
};

// 2. [인터랙션 발생 시마다 트리거] 기사 수 기준 상위 N개 슬라이싱 및 핵심 지표 연산
const processFilteredData = () => {
  const articleCounts = {}; // 기사 수(빈도수) 카운터 객체
  const stats = {};         // 지표 합산용 객체

  // 원본 데이터 탐색 루프
  cachedAllData.forEach(item => {
    const cat = item.category;
    if (cat) {
      // 기사 수 카운트 누적
      articleCounts[cat] = (articleCounts[cat] || 0) + 1;
      
      // 수치 지표 합산 누적
      if (!stats[cat]) {
        stats[cat] = { views: 0, shares: 0, comments: 0 };
      }
      stats[cat].views += item.view_count || 0;
      stats[cat].shares += item.shares || 0;
      stats[cat].comments += item.comments_count || 0;
    }
  });

  // 기사 수(Value Counts) 기준으로 전체 카테고리 내림차순 정렬
  const sortedByArticleCount = Object.keys(articleCounts).sort((a, b) => articleCounts[b] - articleCounts[a]);

  // 사용자가 입력한 topN 개수만큼 슬라이싱 추출 (1 미만 및 최대치 초과 방어 조건 포함)
  const targetN = Math.max(1, Math.min(topN.value || 1, maxCategories.value));
  const topNCategories = sortedByArticleCount.slice(0, targetN);
  filteredCategories.value = topNCategories;

  // 가공 리스트 초기화 후 재할당
  sharesPerViewData.value = [];
  commentsPerViewData.value = [];
  ratioData.value = [];

  // 슬라이싱된 상위 N개 카테고리에 대해서만 연산 파이프라인 가동
  topNCategories.forEach(cat => {
    const target = stats[cat];
    const shareRatio = target.views > 0 ? (target.shares / target.views) * 1000 : 0;
    const commentRatio = target.views > 0 ? (target.comments / target.views) * 1000 : 0;
    const finalRatio = commentRatio > 0 ? shareRatio / commentRatio : 0;

    sharesPerViewData.value.push(Number(shareRatio.toFixed(4)));
    commentsPerViewData.value.push(Number(commentRatio.toFixed(4)));
    ratioData.value.push(Number(finalRatio.toFixed(3)));
  });

  // 4번 차트용: 정제된 상위 N개 데이터를 가설 배율 수치 기준으로 한 번 더 정렬
  const combinedList = topNCategories.map((cat, idx) => ({
    name: cat,
    val: ratioData.value[idx]
  }));
  combinedList.sort((a, b) => b.val - a.val);

  sortedCategories.value = combinedList.map(item => item.name);
  sortedRatioData.value = combinedList.map(item => item.val);
};

// 3. 차트 생성 및 실시간 갱신(Update) 제어 함수
const renderOrUpdateCharts = () => {
  // 4개의 차트 인스턴스가 모두 이미 빌드되어 있다면 새로 생성하지 않고 데이터 구조만 동적 갱신
  if (chart1 && chart2 && chart3 && chart4) {
    chart1.data.labels = filteredCategories.value;
    chart1.data.datasets[0].data = sharesPerViewData.value;
    chart1.update();

    chart2.data.labels = filteredCategories.value;
    chart2.data.datasets[0].data = commentsPerViewData.value;
    chart2.update();

    chart3.data.labels = filteredCategories.value;
    chart3.data.datasets[0].data = ratioData.value;
    chart3.update();

    chart4.data.labels = sortedCategories.value;
    chart4.data.datasets[0].data = sortedRatioData.value;
    chart4.update();
    
    console.log(`인터랙티브 필터 동적 반영 완료 (상위 ${topN.value}개 카테고리)`);
  } else {
    // 컴포넌트 마운트 시점 최초 빌드 로직
    chart1 = new Chart(canvas1.value, {
      type: 'bar',
      data: {
        labels: filteredCategories.value,
        datasets: [{ label: '공유수 / 조회수 (×10³)', data: sharesPerViewData.value, backgroundColor: 'rgba(54, 162, 235, 0.6)' }]
      },
      options: { responsive: true }
    });

    chart2 = new Chart(canvas2.value, {
      type: 'bar',
      data: {
        labels: filteredCategories.value,
        datasets: [{ label: '댓글수 / 조회수 (×10³)', data: commentsPerViewData.value, backgroundColor: 'rgba(153, 102, 255, 0.6)' }]
      },
      options: { responsive: true }
    });

    chart3 = new Chart(canvas3.value, {
      type: 'bar',
      data: {
        labels: filteredCategories.value,
        datasets: [{ label: '상대적 비율 (공유 ÷ 댓글)', data: ratioData.value, backgroundColor: 'rgba(75, 192, 192, 0.6)' }]
      },
      options: { responsive: true }
    });

    chart4 = new Chart(canvas4.value, {
      type: 'bar',
      data: {
        labels: sortedCategories.value,
        datasets: [{
          label: '가설 지표 우위 순위',
          data: sortedRatioData.value,
          backgroundColor: 'rgba(255, 159, 64, 0.7)',
          borderColor: 'rgba(255, 159, 64, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          tooltip: {
            enabled: true,
            callbacks: {
              title: (context) => `순위 등급 분야: ${context[0].label}`,
              label: (context) => `공유/댓글 배율 수치: ${context.parsed.y}배`
            }
          }
        },
        scales: {
          x: {
            ticks: { display: false },
            grid: { display: false }
          }
        }
      }
    });
    console.log('가설 검정 4종 기본 차트 팩토리 빌드 완료');
  }
};

// 입력 폼 변화 시 트리거되는 중앙 통제 제어 핸들러
const updateDashboard = () => {
  processFilteredData();
  renderOrUpdateCharts();
};

onMounted(() => {
  initRawData();
  processFilteredData();
  renderOrUpdateCharts();
});
</script>

<style scoped>
.hypothesis-dashboard {
  padding: 10px;
}

.dashboard-header {
  background-color: #f1f3f5;
  padding: 18px;
  border-radius: 8px;
  margin-bottom: 20px;
  border-left: 5px solid #ff922b;
}

.dashboard-header h4 {
  margin: 0 0 8px 0;
  color: #343a40;
}

.hypothesis-text {
  margin: 0 0 15px 0;
  font-size: 0.95rem;
  color: #495057;
  line-height: 1.4;
}

/* 인터랙티브 필터 영역 스타일링 */
.interactive-filter-panel {
  background-color: #ffffff;
  padding: 12px 15px;
  border-radius: 6px;
  border: 1px solid #dee2e6;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-label {
  font-size: 0.88rem;
  font-weight: 700;
  color: #495057;
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.top-n-input {
  width: 80px;
  padding: 6px 10px;
  font-size: 0.95rem;
  font-weight: bold;
  border: 2px solid #ff922b;
  border-radius: 4px;
  text-align: center;
  color: #212529;
}

.top-n-input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(255, 146, 43, 0.25);
}

.filter-hint {
  font-size: 0.82rem;
  color: #868e96;
}

/* 2x2 대시보드 배치 Grid */
.chart-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.chart-card {
  background: #ffffff;
  border: 1px solid #dee2e6;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.02);
}

.highlight-card {
  border: 1px solid #ff922b;
  background-color: #fff9db;
}

.chart-title {
  margin-top: 0;
  margin-bottom: 12px;
  font-size: 0.95rem;
  color: #212529;
  font-weight: 600;
}

@media (max-width: 1024px) {
  .chart-grid {
    grid-template-columns: 1fr;
  }
}
</style>