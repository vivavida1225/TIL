<template>
  <div class="chart-wrapper">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Chart } from 'chart.js/auto';
import newsDataRaw from '@/assets/news_politics.jsonl?raw';

const chartCanvas = ref(null);

// 고유 카테고리 목록을 저장할 배열
const categories = ref([]);
// 산점도에 뿌려질 2차원 좌표 데이터 배열 ({ x: 카테고리인덱스 + 노이즈, y: 감성점수 })
const scatterPoints = ref([]);

// F308 고도화: 10,000건의 감성 점수 분포 데이터 정제 (Jittering 알고리즘)
const processDistributionData = () => {
  try {
    const lines = newsDataRaw.split('\n').filter(line => line.trim() !== '');
    const parsedData = lines.map(line => JSON.parse(line));

    // 1. 전체 데이터에서 고유한 카테고리 중복 제거 후 리스트화 (X축 컬럼 레이블이 됨)
    const uniqueCategories = [...new Set(parsedData.map(item => item.category).filter(Boolean))];
    categories.value = uniqueCategories;

    const points = [];

    parsedData.forEach(item => {
      const category = item.category;
      const sentiment = item.sentiment_score;
      const topic = item.article_topic;

      if (category && sentiment !== null && sentiment !== undefined) {
        // 2. 카테고리 문자열을 X축 정수 인덱스(0, 1, 2...)로 변환
        const catIndex = uniqueCategories.indexOf(category);

        if (catIndex !== -1) {
          // 3. [핵심] 지터링(Jittering) 연산: 무작위 가로 오차 생성 (-0.25 ~ +0.25 사이)
          // 이 노이즈 덕분에 점들이 컬럼 가로 영역 내부에서 이쁘게 분산됩니다.
          const jitter = (Math.random() - 0.5) * 0.5;

          points.push({
            x: catIndex + jitter, // X좌표: 고정 컬럼 위치 + 미세 노이즈
            y: sentiment,         // Y좌표: 감성 점수 (-1.0 ~ 1.0)
            // 툴팁 출력 및 커스텀 분석용 메타 데이터 보관
            rawCategory: category,
            articleTopic: topic
          });
        }
      }
    });

    scatterPoints.value = points;
    console.log(`F308 분포도 정제 완료. 총 ${scatterPoints.value.length}개 포인트 매핑`);
  } catch (error) {
    console.error('F308 데이터 분포도 가공 중 에러 발생:', error);
  }
};

// 분포 산점도 렌더링 함수
const renderChart = () => {
  if (!chartCanvas.value) return;

  new Chart(chartCanvas.value, {
    type: 'scatter', // 분포 분석용 산점도 유형 지정
    data: {
      datasets: [{
        label: '기사별 여론 감성 분포 (점 하나 = 기사 1건)',
        data: scatterPoints.value,
        // 4. [핵심] 투명도 최적화: 10,000개가 겹치므로 반투명하게 지정하여 밀집도(Density) 표현
        backgroundColor: 'rgba(92, 124, 250, 0.15)', // 로열 블루 컬러 + 15% 투명도
        borderColor: 'transparent', // 테두리를 없애야 점들이 뭉쳤을 때 경계선 때문에 시야가 가려지지 않음
        pointRadius: 2.5, // 점의 크기를 작게 조절하여 고해상도 분산 궤적 확보
        pointHoverRadius: 6,
        pointHoverBackgroundColor: '#ef4444' // 마우스 올린 점은 강렬한 레드 색상으로 반전 피드백
      }]
    },
    options: {
      responsive: true,
      plugins: {
        tooltip: {
          callbacks: {
            // 산점도 호버 시, 숫자로 된 X좌표 대신 실제 기사 제목과 카테고리가 나오도록 툴팁 탈바꿈
            label: function(context) {
              const rawObj = context.dataset.data[context.dataIndex];
              return [
                `[${rawObj.rawCategory}] 감성 점수: ${rawObj.y}`,
                `주제: ${rawObj.articleTopic.substring(0, 30)}...`
              ];
            }
          }
        }
      },
      scales: {
        x: {
          type: 'linear', // 지터링 수치 계산을 위해 가로축을 선형 숫자로 지정
          min: -0.5,
          max: categories.value.length - 0.5,
          ticks: {
            stepSize: 1,
            // 5. [핵심] 축 레이블 가로채기: 정수 눈금(0, 1, 2...) 위치에 실제 카테고리 문자열 매핑
            callback: function(value) {
              return categories.value[value] || '';
            }
          },
          grid: {
            display: true,
            color: '#e9ecef'
          }
        },
        y: {
          min: -1.0,
          max: 1.0,
          title: {
            display: true,
            text: '감성 점수 스펙트럼 (-1.0 부정 ~ 1.0 긍정)'
          },
          grid: {
            // 0점 중립선을 기준으로 상하 분포를 쉽게 대조할 수 있도록 가이드라인 강조
            color: (context) => context.tick.value === 0 ? '#343a40' : '#f1f3f5',
            lineWidth: (context) => context.tick.value === 0 ? 2 : 1
          }
        }
      }
    }
  });
};

onMounted(() => {
  processDistributionData();
  renderChart();
});
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  max-width: 950px; /* 대량의 점 분산 공간 확보를 위해 가로 너비 확장 */
  margin: 0 auto;
}
</style>