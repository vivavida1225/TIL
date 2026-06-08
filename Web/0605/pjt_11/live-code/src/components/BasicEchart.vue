<!--
  [3-2] ECharts 기본 버블(산점) 차트

  Chart.js와 다른 점:
    - <canvas> 대신 <div> 하나에 echarts.init(div) 로 그림
    - 한 점 = [가격, 판매량, 재고, 카테고리] 네 칸 배열
-->
<template>
  <div class="basic-echart">
    <h1 style="text-align: center;">도서 데이터 버블 차트 실습</h1>
    <!-- ECharts가 이 div 크기에 맞춰 내부 canvas를 만듦 -->
    <div ref="chartRef" class="chart-container"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import * as echarts from "echarts";

// 차트를 그릴 DOM (div)
const chartRef = ref(null);
let chartInstance = null;

/**
 * [3-2] 실습용 데이터
 * seriesData 한 줄 = [ x값(가격), y값(판매량), 버블크기용(재고), 카테고리문자열 ]
 */
const chartData = {
  titleText: "도서 판매 분석 (가격 vs 판매량 vs 재고)",
  seriesData: [
    [12000, 20, 500, "소설"],
    [15000, 45, 1200, "자기계발"],
    [18000, 10, 300, "소설"],
    [25000, 50, 2000, "IT/기술"],
    [22000, 30, 800, "자기계발"]
  ]
};

function renderChart() {
  if (!chartRef.value) return;

  // [3-2] ECharts 인스턴스 생성 (이 div에 차트 엔진 연결)
  chartInstance = echarts.init(chartRef.value);

  /**
   * option = 차트의 "설계도" (제목, 축, 데이터, 툴팁 등 한 번에 설정)
   */
  const option = {
    title: {
      text: chartData.titleText,
      left: "center"
    },
    tooltip: {
      trigger: "item", // 점 하나에 마우스 올릴 때
      formatter: function (params) {
        // params.value = [가격, 판매량, 재고, 카테고리]
        return `
          가격: ${params.value[0]}원<br/>
          판매량: ${params.value[1]}만부<br/>
          재고: ${params.value[2]}권<br/>
          카테고리: ${params.value[3]}
        `;
      }
    },
    xAxis: {
      name: "가격",
      type: "value", // 숫자 축 (카테고리 이름이 아님)
      min: 0
    },
    yAxis: {
      name: "판매량",
      type: "value",
      min: 0
    },
    series: [
      {
        type: "scatter", // 산점도 → 버블 크기는 symbolSize로 조절
        data: chartData.seriesData,
        symbolSize: function (data) {
          // data[2] = 재고 → 재고가 많을수록 큰 원
          return data[2] / 40;
        },
        itemStyle: {
          color: "#5470C6"
        }
      }
    ]
  };

  chartInstance.setOption(option);
}

/** 창 크기가 바뀌면 차트도 리사이즈 (찌그러짐 방지) */
function handleResize() {
  chartInstance?.resize();
}

onMounted(() => {
  renderChart();
  window.addEventListener("resize", handleResize);
});

/** 컴포넌트가 사라질 때: 이벤트 제거 + 차트 메모리 해제 */
onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
  chartInstance?.dispose();
});
</script>

<style scoped>
.basic-echart {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
}

.chart-container {
  width: 100%;
  height: 500px; /* 높이가 있어야 ECharts가 그릴 영역을 계산할 수 있음 */
}
</style>
