<!--
  [3-1] ECharts 전용 화면 (View)

  Chart.js 뷰와 같은 구조:
    - BasicEchart     : 필터 없는 버블 차트
    - InteractiveEchart : 카테고리 체크박스 필터
-->
<template>
  <div class="echart-view">
    <section>
      <BasicEchart />
    </section>
    <section>
      <InteractiveEchart />
    </section>
  </div>
</template>

<script setup>
// 데이터는 각 컴포넌트 안에 있어서, 이 파일은 "배치"만 담당
import BasicEchart from "../components/BasicEchart.vue";
import InteractiveEchart from "../components/InteractiveEchart.vue";
</script>

<style scoped>
.echart-view {
  padding: 0 1rem;
}

.echart-view section + section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}
</style>
