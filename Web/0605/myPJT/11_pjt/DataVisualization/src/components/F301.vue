<template>
  <div>
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
// 1. Vite의 ?raw 접미사를 사용하여 JSONL 파일을 텍스트 문자열로 그대로 가져옵니다.
import sportsDataRaw from '@/assets/sports.jsonl?raw';
import { Chart } from 'chart.js/auto'; // 1. 차트 라이브러리 임포트 추가

// Chart.js에 최종적으로 전달할 데이터 상태 정의
const chartLabels = ref([]);
const chartData = ref([]);

// DOM 엘리먼트와 매핑할 ref 선언
const chartCanvas = ref(null);

const processSportsData = () => {
  try {
    // 2. 문자열을 줄바꿈(\n) 기준으로 쪼개고, 양 끝 공백을 제거한 뒤 빈 줄은 필터링합니다.
    const lines = sportsDataRaw.split('\n').filter(line => line.trim() !== '');

    // 3. 각 줄의 JSON 텍스트를 JavaScript 객체로 변환합니다.
    const parsedData = lines.map(line => JSON.parse(line));

    // 4. 종목(sport_type)별 빈도수를 저장할 객체를 생성합니다.
    const counts = {};

    parsedData.forEach(item => {
      const sport = item.sport_type;
      if (sport) {
        // 객체에 이미 종목이 있으면 기존 값 + 1, 없으면 0 + 1 (Python의 get(key, 0)과 동일)
        counts[sport] = (counts[sport] || 0) + 1;
      }
    });

    // 5. 집계된 결과를 Chart.js 포맷에 맞게 key 배열과 value 배열로 분리하여 ref에 할당합니다.
    chartLabels.value = Object.keys(counts); // 예: ['야구', '축구', '농구', ...]
    chartData.value = Object.values(counts);  // 예: [850, 920, 780, ...]

    // 정제된 데이터가 잘 나왔는지 콘솔에서 확인합니다.
    console.log('정제된 종목 리스트(Labels):', chartLabels.value);
    console.log('종목별 경기 수(Data):', chartData.value);

  } catch (error) {
    console.error('데이터를 정제하는 중 에러가 발생했습니다:', error);
  }
};

// 2. 실제 차트를 그리는 함수 정의
const renderChart = () => {
  // canvas 엘리먼트가 정상적으로 로드되었는지 방어 코드 작성
  if (!chartCanvas.value) return;

  // Chart 인스턴스 생성
  new Chart(chartCanvas.value, {
    type: 'bar', // 명세서 요구사항에 따른 막대그래프 [cite: 72, 83]
    data: {
      labels: chartLabels.value, // 위에서 정제한 종목명 배열 연동 (['야구', '축구', ...])
      datasets: [{
        label: '종목별 경기 수', // 차트 상단 범례 명칭 [cite: 76]
        data: chartData.value,   // 위에서 집계한 경기 수 배열 연동 ([850, 920, ...])
        backgroundColor: 'rgba(54, 162, 235, 0.6)', // 명세서 예시와 유사한 시원한 블루톤 [cite: 76]
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true // Y축이 0부터 시작하도록 설정
        }
      }
    }
  });
};

onMounted(() => {
  // 3. 반드시 데이터를 먼저 가공한 '후'에 차트를 그려야 동적으로 데이터가 반영됩니다.
  processSportsData();
  renderChart();
});
</script>

<style scoped>
/* 차트 크기가 무한정 커지는 것을 방지하기 위해 스타일을 제한해 두면 좋습니다 */
div {
  max-width: 800px;
  margin: 0 auto;
}
</style>