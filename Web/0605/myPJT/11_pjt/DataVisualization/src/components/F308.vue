<template>
  <div class="chart-wrapper">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Chart } from 'chart.js/auto';
// @/ 절대 경로 규칙을 사용하여 뉴스 데이터를 텍스트로 로드합니다.
import newsDataRaw from '@/assets/news_politics.jsonl?raw';

const chartCanvas = ref(null);
const chartLabels = ref([]);
const chartData = ref([]);
const barColors = ref([]); // 긍부정에 따른 동적 색상 배열

// F308: 분야별 평균 감성 점수 계산 파이프라인
const processSentimentData = () => {
  try {
    const lines = newsDataRaw.split('\n').filter(line => line.trim() !== '');
    const parsedData = lines.map(line => JSON.parse(line));

    // 각 카테고리별로 { 감성점수 합산, 기사 건수 }를 저장할 해시맵
    const categoryStats = {};

    parsedData.forEach(item => {
      const category = item.category;
      const sentiment = item.sentiment_score;

      if (category && sentiment !== undefined && sentiment !== null) {
        if (!categoryStats[category]) {
          categoryStats[category] = { totalScore: 0, count: 0 };
        }
        categoryStats[category].totalScore += sentiment;
        categoryStats[category].count += 1;
      }
    });

    // 최종 평균 계산 및 차트 포맷팅
    const labels = [];
    const averages = [];
    const colors = [];

    Object.keys(categoryStats).forEach(category => {
      const stats = categoryStats[category];
      // 소수점 아래 3자리에서 반올림하여 2자리로 규격화 (Python의 round(val, 2)와 유사)
      const avg = stats.count > 0 ? Number((stats.totalScore / stats.count).toFixed(2)) : 0;

      labels.push(category);
      averages.push(avg);

      // 시각적 직관성 강화: 평균 여론이 부정적(0 미만)이면 붉은색계열, 긍정적(0 이상)이면 푸른색계열
      if (avg < 0) {
        colors.push('rgba(239, 68, 68, 0.6)'); // Red
      } else {
        colors.push('rgba(59, 130, 246, 0.6)'); // Blue
      }
    });

    chartLabels.value = labels;
    chartData.value = averages;
    barColors.value = colors;

    console.log('F308 분야별 감성 점수 평균 연산 완료');
  } catch (error) {
    console.error('F308 데이터 처리 중 오류 발생:', error);
  }
};

// Chart.js 인스턴스 빌드 함수
const renderChart = () => {
  if (!chartCanvas.value) return;

  new Chart(chartCanvas.value, {
    type: 'bar', // 범주형 평균 지표 비교에 가장 적합한 Bar 타입 선택 [cite: 72]
    data: {
      labels: chartLabels.value,
      datasets: [{
        label: '평균 감성 점수 여론 성향 (-1.0 ~ 1.0)',
        data: chartData.value,
        backgroundColor: barColors.value, // 동적으로 연산된 조건부 색상 배열 주입
        borderColor: barColors.value.map(color => color.replace('0.6', '1')), // 테두리는 선명하게 강조
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top'
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const score = context.parsed.y;
              const status = score > 0 ? '우호적/긍정' : (score < 0 ? '비판적/부정' : '중립');
              return `평균 감성 점수: ${score} (${status})`;
            }
          }
        }
      },
      scales: {
        y: {
          // 중요: 감성 점수의 원본 한계 범위인 -1과 1을 강제 지정하여 데이터 왜곡을 방지합니다.
          min: -1.0,
          max: 1.0,
          grid: {
            // 0점 기준선(중립선)을 명확하게 인지할 수 있도록 가로 중심선 강조 설정
            color: (context) => context.tick.value === 0 ? '#343a40' : '#e9ecef',
            lineWidth: (context) => context.tick.value === 0 ? 2 : 1
          }
        }
      }
    }
  });
};

onMounted(() => {
  processSentimentData();
  renderChart();
});
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}
</style>