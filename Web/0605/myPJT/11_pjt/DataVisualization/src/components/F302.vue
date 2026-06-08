<template>
  <div>
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Chart } from 'chart.js/auto';
// @/ 절대 경로 규칙을 적용하여 로컬 JSONL 데이터를 가져옵니다.
import sportsDataRaw from '@/assets/sports.jsonl?raw';

// DOM 접근을 위한 ref 선언
const chartCanvas = ref(null);

// Chart.js에 주입할 라벨과 데이터 상태
const chartLabels = ref([]);
const chartData = ref([]);

// F302 요구사항: 종목별 평균 관중 수(attendance) 계산 로직
const calculateAverageAttendance = () => {
  try {
    const lines = sportsDataRaw.split('\n').filter(line => line.trim() !== '');
    const parsedData = lines.map(line => JSON.parse(line));

    // 각 종목별로 { 누적 관중수, 경기 횟수 }를 저장할 임시 객체
    const sportStats = {};

    parsedData.forEach(item => {
      const sport = item.sport_type;
      const attendance = item.attendance;

      // 종목명이 존재하고, 관중 수 데이터가 유효한(null이 아닌) 경우만 집계
      if (sport && attendance !== undefined && attendance !== null) {
        if (!sportStats[sport]) {
          // 해당 종목이 처음 등장하면 구조 초기화 (Python의 defaultdict 구조와 유사)
          sportStats[sport] = { totalVolume: 0, matchCount: 0 };
        }
        // 누적 관중 수 합산 및 경기 수 카운트 증가
        sportStats[sport].totalVolume += attendance;
        sportStats[sport].matchCount += 1;
      }
    });

    // 누적 데이터를 바탕으로 '평균값'을 계산하여 배열로 정제
    const labels = [];
    const averages = [];

    Object.keys(sportStats).forEach(sport => {
      const stats = sportStats[sport];
      // 경기 수가 0보다 클 때만 평균을 구하고 소수점은 반올림(Math.round) 처리
      const avg = stats.matchCount > 0 ? Math.round(stats.totalVolume / stats.matchCount) : 0;
      
      labels.push(sport);
      averages.push(avg);
    });

    // 반응형 변수에 최종 결과값 바인딩
    chartLabels.value = labels;
    chartData.value = averages;

    console.log('F302 데이터 정제 및 평균 계산 완료');
  } catch (error) {
    console.error('F302 데이터 처리 중 에러 발생:', error);
  }
};

// 차트 렌더링 함수
const renderChart = () => {
  if (!chartCanvas.value) return;

  new Chart(chartCanvas.value, {
    type: 'bar', // 비교에 적합한 막대그래프 유형 선택
    data: {
      labels: chartLabels.value, // 가공된 종목 리스트 배열
      datasets: [{
        label: '종목별 평균 관중 수 (명)',
        data: chartData.value,   // 가공된 평균 관중 수 배열
        // 명세서 예시 화면과 유사한 핑크/로즈 계열 테마 스타일링
        backgroundColor: 'rgba(255, 99, 132, 0.6)', 
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1
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
        y: {
          beginAtZero: true,
          ticks: {
            // 관중 수이므로 숫자에 3자리마다 콤마(,)를 추가하는 포맷팅 적용
            callback: function(value) {
              return value.toLocaleString();
            }
          }
        }
      }
    }
  });
};

onMounted(() => {
  // 컴포넌트 장착 시 순차적으로 데이터 가공 후 차트 생성
  calculateAverageAttendance();
  renderChart();
});
</script>

<style scoped>
div {
  max-width: 800px;
  margin: 20px auto;
}
</style>