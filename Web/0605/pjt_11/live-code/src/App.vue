<script setup>
import { ref } from 'vue'

// 각 탭에서 보여 줄 "페이지" 컴포넌트
import ChartjsView from './views/ChartjsView.vue'
import EchartView from './views/EchartView.vue'
// [추가] Table 컴포넌트 임포트 (@ 경로 사용)
import TableView from '@/components/table/Table.vue'

// 현재 어떤 탭인지 저장 ('chartjs', 'echarts', 'table')
const currentView = ref('chartjs')
</script>

<template>
  <div>
    <nav style="margin-bottom: 1rem;">
      <button
        type="button"
        :class="{ active: currentView === 'chartjs' }"
        @click="currentView = 'chartjs'"
      >
        Chart.js
      </button>
      <button
        type="button"
        :class="{ active: currentView === 'echarts' }"
        @click="currentView = 'echarts'"
        style="margin-left: 0.5rem;"
      >
        ECharts
      </button>
      
      <button
        type="button"
        :class="{ active: currentView === 'table' }"
        @click="currentView = 'table'"
        style="margin-left: 0.5rem;"
      >
        Table
      </button>
    </nav>

    <ChartjsView v-if="currentView === 'chartjs'" />
    <EchartView v-else-if="currentView === 'echarts'" />
    <TableView v-else />
  </div>
</template>

<style scoped>
/*
  scoped = 이 스타일은 App.vue 안에서만 적용 (다른 파일에 섞이지 않음)
*/
button {
  padding: 0.25rem 0.5rem;
  cursor: pointer;
}
button.active {
  font-weight: bold;
}
</style>