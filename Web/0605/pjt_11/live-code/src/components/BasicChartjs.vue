<!--
  [2-2] Chart.js 기본 막대 차트 컴포넌트

  흐름 요약:
    1) 부모(ChartjsView)가 chartData를 props로 전달
    2) <canvas> 요소에 Chart.js가 막대 그래프를 그림
    3) chartData가 바뀌면 watch가 renderChart를 다시 호출
-->
<template>
  <div class="basic-chart">
    <!-- {{ }} = script의 데이터를 화면에 출력 (제목) -->
    <h2>{{ chartData.titleText }}</h2>

    <!--
      ref="canvasRef" → script의 canvasRef 변수와 이 canvas를 연결
      Chart.js는 반드시 <canvas> 위에 그려집니다.
    -->
    <canvas ref="canvasRef"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { Chart, registerables } from "chart.js";

// Chart.js v4: 사용할 차트 종류(막대, 선 등)를 한 번에 등록
Chart.register(...registerables);

/**
 * [2-2] props = 부모 컴포넌트가 넘겨준 읽기 전용 데이터
 * required: true → 이 컴포넌트는 chartData 없이 쓰면 안 됨
 */
const props = defineProps({
  chartData: {
    type: Object,
    required: true
  }
});

// canvas DOM을 가리키는 참조 (처음엔 null, onMounted 이후에 값이 채워짐)
const canvasRef = ref(null);

// Chart.js 인스턴스를 담아 둘 변수 (다시 그릴 때 destroy 하기 위해 밖에 둠)
let chartInstance = null;

/**
 * [2-2] 실제로 막대 차트를 그리는 함수
 */
function renderChart() {
  // canvas가 아직 없거나, 데이터가 없으면 그리지 않음 (안전 장치)
  if (!canvasRef.value || !props.chartData) return;

  const { labels, data, colors, titleText } = props.chartData;
  if (!labels?.length) return;

  // 이미 차트가 있으면 메모리 누수 방지를 위해 제거 후 새로 생성
  if (chartInstance) chartInstance.destroy();

  chartInstance = new Chart(canvasRef.value, {
    type: "bar", // 막대 차트
    data: {
      labels, // x축 라벨 (도서명)
      datasets: [
        {
          label: "판매량", // 범례에 보이는 이름
          data, // y축 값 배열
          backgroundColor: colors || [],
          // 테두리 색: 배경색에서 투명도 0.6 → 1 로 바꿔 진하게
          borderColor: (colors || []).map(c => c.replace("0.6", "1")),
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true, // 창 크기에 맞게 조절
      plugins: {
        legend: { position: "top" },
        tooltip: { enabled: true } // 마우스 올리면 값 표시
      },
      scales: {
        y: { beginAtZero: true } // y축 0부터 시작 (막대 비교가 쉬움)
      }
    }
  });
}

// 컴포넌트가 화면에 붙은 직후 한 번 그리기
onMounted(renderChart);

// chartData 객체 내용이 바뀌면 다시 그리기 (deep: 객체 안쪽까지 감시)
watch(() => props.chartData, renderChart, { deep: true });
</script>

<style scoped>
.basic-chart {
  width: 600px;
  margin: 0 auto;
}
</style>
