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

// Chart.js 산점도에 주입할 데이터 배열 상태 ({ x: attendance, y: viewership_rating_percent })
const scatterData = ref([]);

// F304 요구사항: 관중 수(attendance)와 시청률(viewership_rating_percent) 관계 데이터 정제
const processScatterData = () => {
  try {
    const lines = sportsDataRaw.split('\n').filter(line => line.trim() !== '');
    const parsedData = lines.map(line => JSON.parse(line));

    const points = [];

    parsedData.forEach(item => {
      const attendance = item.attendance;
      const rating = item.viewership_rating_percent;

      // 두 지표 모두 null이나 undefined가 아니고 유효한 수치형 데이터인 경우만 좌표로 매핑
      if (attendance !== null && attendance !== undefined && rating !== null && rating !== undefined) {
        points.push({
          x: attendance, // X축 좌표: 관중 수
          y: rating      // Y축 좌표: 시청률 (%)
        });
      }
    });

    scatterData.value = points;
    console.log('F304 산점도 데이터 정제 완료, 총 매핑 포인트:', scatterData.value.length);
  } catch (error) {
    console.error('F304 데이터 처리 중 에러 발생:', error);
  }
};

// 차트 렌더링 함수
const renderChart = () => {
  if (!chartCanvas.value) return;

  new Chart(chartCanvas.value, {
    type: 'scatter', // 상관관계 분석에 적합한 산점도(Scatter) 유형 선택
    data: {
      datasets: [{
        label: '관중 수 대비 시청률 분포',
        data: scatterData.value, // [{x: 12000, y: 2.5}, ...] 형태의 데이터 주입
        // 명세서 예시 화면과 유사한 민트/청록(Teal) 계열 스타일링
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        pointRadius: 3,          // 수천 개의 점이 겹칠 때 답답해 보이지 않도록 반지름 최적화
        pointHoverRadius: 6      // 마우스를 올렸을 때 점의 크기 확장
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        tooltip: {
          callbacks: {
            // 데이터 포인트 호버 시, 단순 좌표 대신 직관적인 명칭 단위로 출력 커스텀
            label: function(context) {
              const xValue = context.parsed.x.toLocaleString();
              const yValue = context.parsed.y;
              return `관중 수: ${xValue}명 | 시청률: ${yValue}%`;
            }
          }
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: '관중 수 (명)' // X축에 명확한 물리량 인덱스 제공
          },
          beginAtZero: true,
          ticks: {
            callback: function(value) {
              return value.toLocaleString(); // 가로축 수치 천 단위 콤마 포맷팅
            }
          }
        },
        y: {
          title: {
            display: true,
            text: '시청률 (%)' // Y축에 명확한 물리량 인덱스 제공
          },
          beginAtZero: true
        }
      }
    }
  });
};

onMounted(() => {
  // 컴포넌트 장착 시 산점도 포맷팅 후 차트 생성
  processScatterData();
  renderChart();
});
</script>

<style scoped>
div {
  max-width: 800px;
  margin: 20px auto;
}
</style>