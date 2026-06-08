<template>
  <div>
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Chart } from 'chart.js/auto';
// @/ 절대 경로 규칙을 사용하여 로컬 JSONL 데이터를 가져옵니다.
import sportsDataRaw from '@/assets/sports.jsonl?raw';

// DOM 접근을 위한 ref 선언
const chartCanvas = ref(null);

// Chart.js에 주입할 날짜(Labels)와 경기 수(Data) 상태
const chartLabels = ref([]);
const chartData = ref([]);

// F303 요구사항: 날짜별 경기 추이 집계 및 정렬 로직
const processTimeSeriesData = () => {
  try {
    const lines = sportsDataRaw.split('\n').filter(line => line.trim() !== '');
    const parsedData = lines.map(line => JSON.parse(line));

    // 1. 날짜별 경기 수를 누적할 빈 객체(해시맵) 생성
    const dateCounts = {};

    parsedData.forEach(item => {
      const date = item.date; // 데이터 내 "YYYY-MM-DD" 문자열 형태
      if (date) {
        dateCounts[date] = (dateCounts[date] || 0) + 1;
      }
    });

    // 2. 시계열 차트의 특성상 날짜를 오름차순(과거 -> 최신)으로 반드시 정렬해야 합니다.
    // 문자열 날짜를 Date 객체로 변환하여 크기를 비교 정렬합니다.
    const sortedDates = Object.keys(dateCounts).sort((a, b) => new Date(a) - new Date(b));

    // 3. 정렬된 날짜 순서에 맞춰서 Labels 배열과 Data 배열을 맵핑합니다.
    chartLabels.value = sortedDates;
    chartData.value = sortedDates.map(date => dateCounts[date]);

    console.log('F303 시계열 데이터 정제 및 정렬 완료');
  } catch (error) {
    console.error('F303 데이터 처리 중 에러 발생:', error);
  }
};

// 차트 렌더링 함수
const renderChart = () => {
  if (!chartCanvas.value) return;

  new Chart(chartCanvas.value, {
    type: 'line', // 추이 변화를 시각화하기 위해 선 그래프(Line Chart) 유형 선택
    data: {
      labels: chartLabels.value, // 정렬된 일자 배열 (X축)
      datasets: [{
        label: '일별 경기 수 추이',
        data: chartData.value,   // 해당 일자의 경기 수 배열 (Y축)
        // 명세서 예시와 매칭되는 황색/앰버(Amber) 계열 스타일링
        borderColor: 'rgba(255, 193, 7, 1)',     
        backgroundColor: 'rgba(255, 193, 7, 0.1)', 
        borderWidth: 2,
        fill: true,          // 선 아래 영역을 은은하게 채워 볼륨감 표현
        tension: 0.15,       // 선을 살짝 부드럽게 꺾이도록 설정 (0이면 완전 직선)
        pointRadius: 1,      // 데이터 포인트(점)의 크기를 줄여 조밀한 시계열 가독성 확보
        pointHoverRadius: 5  // 마우스를 올렸을 때만 점이 커지도록 설정
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        }
      },
      scales: {
        x: {
          grid: {
            display: false // X축 세로 그리드 선을 숨겨 차트를 시각적으로 단순화
          },
          ticks: {
            maxTicksLimit: 15 // 날짜 수가 너무 많아 글자가 겹치는 현상을 방지 (최대 15개만 눈금 표출)
          }
        },
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1 // 경기 수는 정수 단위이므로 눈금 간격을 1로 제어
          }
        }
      }
    }
  });
};

onMounted(() => {
  // 컴포넌트 마운트 시 시계열 가공 후 차트 생성
  processTimeSeriesData();
  renderChart();
});
</script>

<style scoped>
div {
  max-width: 800px;
  margin: 20px auto;
}
</style>