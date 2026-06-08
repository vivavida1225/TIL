<template>
  <div class="filter-dashboard">
    <div class="filter-container">
      <label class="filter-label">연도·월 범위 (종목별 경기 수에만 적용):</label>
      <div class="input-group">
        <input type="month" v-model="startDate" @change="updateDashboard" class="date-input" />
        <span class="separator">~</span>
        <input type="month" v-model="endDate" @change="updateDashboard" class="date-input" />
        <button @click="resetFilter" class="reset-btn">전체</button>
        <span class="match-count">({{ totalMatches }}경기)</span>
      </div>
    </div>

    <div class="chart-container">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Chart } from 'chart.js/auto';
import sportsDataRaw from '@/assets/sports.jsonl?raw';

// DOM 엘리먼트 맵핑 ref
const chartCanvas = ref(null);

// F306 인터랙티브 UI 상태관리를 위한 반응형 변수 (v-model)
const startDate = ref('2024-01'); // 기본 시작 월 세팅
const endDate = ref('2024-12');   // 기본 종료 월 세팅
const totalMatches = ref(0);      // 필터링된 총 경기 수 표기용

// Chart.js 인스턴스를 저장할 컴포넌트 스코프 변수 (중복 생성 방지용)
let chartInstance = null;

// 파싱이 완료된 원본 데이터 전체를 보관할 배열 (메모리 최적화)
let cachedAllData = [];

// 차트 데이터 갱신을 위한 독립형 리액티브 상태
const chartLabels = ref([]);
const chartData = ref([]);

// 1. [초기 마운트 시 1회 실행] 원본 JSONL 로드 및 파싱 함수
const initRawData = () => {
  try {
    const lines = sportsDataRaw.split('\n').filter(line => line.trim() !== '');
    cachedAllData = lines.map(line => JSON.parse(line));
  } catch (error) {
    console.error('원천 데이터 초기 파싱 중 치명적 에러 발생:', error);
  }
};

// 2. [필터 변경 시마다 호출] 선택된 날짜 범위 기준 데이터 필터링 및 집계 함수
const filterAndProcessData = () => {
  const counts = {};
  let matchCounter = 0;

  cachedAllData.forEach(item => {
    const sport = item.sport_type;
    const matchDate = item.date; // 예: "2024-11-01"

    if (sport && matchDate) {
      // 문자열 자르기(substring)를 통해 "YYYY-MM" 포맷 추출 (예: "2024-11")
      const matchYearMonth = matchDate.substring(0, 7);

      // 시작일과 종료일 범위 조건 검증 (문자열 대소비교 가능)
      const isAfterStart = !startDate.value || matchYearMonth >= startDate.value;
      const isBeforeEnd = !endDate.value || matchYearMonth <= endDate.value;

      if (isAfterStart && isBeforeEnd) {
        counts[sport] = (counts[sport] || 0) + 1;
        matchCounter++;
      }
    }
  });

  // 집계 결과 바인딩
  chartLabels.value = Object.keys(counts);
  chartData.value = Object.values(counts);
  totalMatches.value = matchCounter; // UI 상단에 노출할 필터링 카운트 반영
};

// 3. [렌더링 및 업데이트 관리] 차트 인스턴스 생명주기 제어 함수
const renderOrUpdateChart = () => {
  if (!chartCanvas.value) return;

  // 이미 차트가 존재한다면 새 객체를 만들지 않고 내부 데이터셋만 갈아끼운 후 업데이트 수행
  if (chartInstance) {
    chartInstance.data.labels = chartLabels.value;
    chartInstance.data.datasets[0].data = chartData.value;
    chartInstance.update(); // Chart.js 내장 부드러운 애니메이션 리렌더링 효과 작동
    console.log('기존 차트 실시간 필터 데이터 업데이트 완료');
  } else {
    // 차트가 최초 생성되는 시점의 빌드 로직
    chartInstance = new Chart(chartCanvas.value, {
      type: 'bar',
      data: {
        labels: chartLabels.value,
        datasets: [{
          label: '종목별 경기 수',
          data: chartData.value,
          backgroundColor: 'rgba(54, 162, 235, 0.6)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
    console.log('최초 바 차트 인스턴스 빌드 완료');
  }
};

// 사용자가 UI 날짜 값을 바꿨을 때 통합 실행될 제어 파이프라인
const updateDashboard = () => {
  filterAndProcessData();
  renderOrUpdateChart();
};

// '전체' 보기 버튼 클릭 시 필터 조건 초기화 처리 함수
const resetFilter = () => {
  startDate.value = '';
  endDate.value = '';
  updateDashboard();
};

onMounted(() => {
  initRawData();           // 1. 원본 데이터 1회 캐싱
  filterAndProcessData();  // 2. 초기 세팅 범위 데이터 집계
  renderOrUpdateChart();   // 3. 차트 시각화 활성화
});
</script>

<style scoped>
.filter-dashboard {
  max-width: 800px;
  margin: 0 auto;
  font-family: sans-serif;
}

/* 명세서 레이아웃 스타일 맵핑 */
.filter-container {
  background-color: #f1f3f5;
  padding: 12px 20px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.filter-label {
  font-size: 0.9rem;
  font-weight: bold;
  color: #495057;
  display: block;
  margin-bottom: 6px;
}

.input-group {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.date-input {
  border: 1px solid #ced4da;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9rem;
}

.separator {
  color: #868e96;
}

.reset-btn {
  background-color: #343a40;
  color: #ffffff;
  border: none;
  padding: 5px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
}

.reset-btn:hover {
  background-color: #212529;
}

.match-count {
  font-size: 0.9rem;
  color: #495057;
  margin-left: 5px;
}

.chart-container {
  position: relative;
  width: 100%;
}
</style>