<!--
  [2-1] Chart.js 전용 화면 (View)

  View = "한 탭에 들어가는 페이지 단위" 컴포넌트
  여기서는 (1) 기본 막대 차트 + (2) 필터 있는 막대 차트 를 세로로 배치합니다.
-->
<template>
  <div class="chartjs-view">
    <!-- section: 강의 때 "첫 번째 실습 / 두 번째 실습" 구역 나누기용 -->
    <section>
      <!--
        :chart-data="chartData"
        → 콜론(:)이 붙으면 "문자열"이 아니라 JavaScript 변수/객체를 넘깁니다.
        BasicChartjs의 defineProps({ chartData }) 로 받습니다.
      -->
      <BasicChartjs :chart-data="chartData" />
    </section>
    <section>
      <!-- InteractiveChartjs는 데이터를 컴포넌트 내부에 가지고 있음 (필터 실습용) -->
      <InteractiveChartjs />
    </section>
  </div>
</template>

<script setup>
import BasicChartjs from "../components/BasicChartjs.vue";
import InteractiveChartjs from "../components/InteractiveChartjs.vue";

/**
 * [2-1] Chart.js에 넘길 도서 판매 데이터 (객체 한 덩어리)
 *
 * labels : x축에 쓸 이름 (도서 제목)
 * data   : y축 숫자 (판매량, 단위: 만 부)
 * colors : 각 막대 색 (rgba = 빨강,초록,파랑,투명도)
 */
const chartData = {
  titleText: "도서 판매량 (단위: 만 부)",
  labels: [
    "세이노의 가르침",
    "트렌드 코리아 2024",
    "역행자",
    "도둑맞은 집중력",
    "도시와 그들의 불확실성"
  ],
  data: [200, 150, 120, 90, 80],
  colors: [
    "rgba(255, 99, 132, 0.6)",
    "rgba(54, 162, 235, 0.6)",
    "rgba(255, 206, 86, 0.6)",
    "rgba(75, 192, 192, 0.6)",
    "rgba(153, 102, 255, 0.6)"
  ]
};
</script>

<style scoped>
.chartjs-view {
  max-width: 640px;
  margin: 0 auto;
}

/* 두 section 사이 간격 + 구분선 */
.chartjs-view section + section {
  margin-top: 2rem;
  margin-bottom: 10rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}
</style>
