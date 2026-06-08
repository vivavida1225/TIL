<!--
  [3-3] ECharts 인터랙티브 버블 차트

  카테고리 체크박스로 seriesData를 걸러낸 뒤 setOption으로 차트 갱신
-->
<template>
  <div class="interactive-echart">
    <h1 style="text-align: center;">도서 데이터 버블 차트 (필터 적용)</h1>

    <div class="filters">
      <span class="filters-label">카테고리</span>
      <!--
        v-for="cat in categories" → 카테고리마다 체크박스 하나씩 생성
        v-model="selectedCategories" → 체크된 값들이 배열에 모임 (다중 선택)
      -->
      <label v-for="cat in categories" :key="cat" class="filter-chip">
        <input type="checkbox" :value="cat" v-model="selectedCategories" />
        <span>{{ cat }}</span>
      </label>
    </div>

    <p v-if="filteredData.length === 0" class="empty">
      조건에 맞는 도서가 없습니다.
    </p>
    <div v-else ref="chartRef" class="chart-container"></div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from "vue";
import * as echarts from "echarts";

const chartRef = ref(null);
let chartInstance = null;

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

/** 체크박스에 표시할 카테고리 목록 */
const categories = ["소설", "자기계발", "IT/기술"];

/** 처음엔 전부 선택된 상태 ([...categories] = 배열 복사) */
const selectedCategories = ref([...categories]);

/**
 * [3-3] 선택된 카테고리에 해당하는 점만 남기기
 * item[3] 이 카테고리 문자열
 */
const filteredData = computed(() => {
  return chartData.seriesData.filter((item) => {
    const category = item[3];
    if (
      selectedCategories.value.length &&
      !selectedCategories.value.includes(category)
    )
      return false;
    return true;
  });
});

/** BasicEchart와 같은 option 구조, data만 인자로 받음 */
function buildOption(data) {
  return {
    title: {
      text: chartData.titleText,
      left: "center"
    },
    tooltip: {
      trigger: "item",
      formatter: function (params) {
        const v = params.value;
        return `가격: ${v[0]}원<br/>판매량: ${v[1]}만부<br/>재고: ${v[2]}권<br/>카테고리: ${v[3]}`;
      }
    },
    xAxis: {
      name: "가격",
      type: "value",
      min: 0
    },
    yAxis: {
      name: "판매량",
      type: "value",
      min: 0
    },
    series: [
      {
        type: "scatter",
        data,
        symbolSize: function (d) {
          return d[2] / 40;
        },
        itemStyle: {
          color: "#5470C6"
        }
      }
    ]
  };
}

function updateChart() {
  if (!chartRef.value) return;

  if (filteredData.value.length === 0) {
    chartInstance?.dispose();
    chartInstance = null;
    return;
  }

  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value);
  }

  // notMerge: true → 이전 option과 합치지 않고 통째로 교체 (필터 시 잔상 방지)
  chartInstance.setOption(buildOption(filteredData.value), { notMerge: true });
}

function handleResize() {
  chartInstance?.resize();
}

watch(filteredData, updateChart, { immediate: true });
onMounted(() => {
  updateChart();
  window.addEventListener("resize", handleResize);
});
onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
  chartInstance?.dispose();
});
</script>

<style scoped>
.interactive-echart {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  padding-top: 1rem;
}

.filters {
  display: flex;
  flex-direction: row;
  align-items: center;
  flex-wrap: nowrap;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding: 0.75rem 1rem;
  background: #f5f5f5;
  border-radius: 8px;
}

.filters-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #333;
  margin-right: 0.25rem;
}

.filter-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.9rem;
  padding: 0.35rem 0.6rem;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  white-space: nowrap;
}

.filter-chip:hover {
  border-color: #5470c6;
  background: #f0f4ff;
}

.filter-chip:has(input:checked) {
  border-color: #5470c6;
  background: #e8eeff;
}

.empty {
  color: #666;
  text-align: center;
  padding: 2rem;
}

.chart-container {
  width: 100%;
  height: 500px;
}
</style>
