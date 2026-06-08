<!--
  [2-3] Chart.js 인터랙티브 막대 차트

  사용자가 슬라이더·셀렉트를 바꾸면 → filteredChartData가 자동 계산 → 차트 갱신
-->
<template>
  <div class="interactive-chart">
    <h2>{{ chartData.titleText }} (필터 적용)</h2>

    <!-- [2-3] 필터 UI 영역 -->
    <div class="filters">
      <label>
        최소 판매량 (만 부)
        <!--
          v-model.number="minSales"
          → 슬라이더 값이 minSales와 양방향 연결 + 숫자 타입으로 변환
        -->
        <input
          v-model.number="minSales"
          type="range"
          min="0"
          max="200"
          step="10"
        />
        <span>{{ minSales }}</span>
      </label>
      <label>
        상위 N권
        <select v-model.number="topN">
          <option :value="1">상위 1권</option>
          <option :value="3">상위 3권</option>
          <option :value="5">상위 5권 (전체)</option>
        </select>
      </label>
    </div>

    <!-- 필터 결과가 0건이면 안내 문구 -->
    <p v-if="filteredChartData.labels.length === 0" class="empty">
      조건에 맞는 도서가 없습니다.
    </p>
    <div v-else class="chart-wrap">
      <canvas ref="canvasRef"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const canvasRef = ref(null);
let chartInstance = null;

/** [2-3] 사용자가 조절하는 필터 값 (반응형) */
const minSales = ref(0);   // 최소 판매량 (만 부)
const topN = ref(5);       // 상위 몇 권까지 보일지

/** 원본 데이터 (BasicChartjs와 동일한 구조) */
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

/**
 * [2-3] computed = minSales, topN이 바뀔 때마다 자동으로 다시 계산되는 값
 *
 * 처리 순서:
 *   1) label + value + color 를 한 쌍(pair)으로 묶기
 *   2) value >= minSales 인 것만 남기기 (filter)
 *   3) 앞에서부터 topN개만 자르기 (slice) — 이미 판매량 순으로 정렬되어 있다고 가정
 */
const filteredChartData = computed(() => {
  const pairs = chartData.labels.map((label, i) => ({
    label,
    value: chartData.data[i],
    color: chartData.colors[i]
  }));

  const filtered = pairs
    .filter((p) => p.value >= minSales.value)
    .slice(0, topN.value);

  return {
    titleText: chartData.titleText,
    labels: filtered.map((p) => p.label),
    data: filtered.map((p) => p.value),
    colors: filtered.map((p) => p.color)
  };
});

/**
 * [2-3] 차트 생성 또는 데이터만 갱신
 * - 처음: new Chart(...)
 * - 이후: chartInstance.update() 로 막대만 바꿈 (더 빠름)
 */
function updateChart() {
  if (!canvasRef.value) return;
  const { labels, data, colors } = filteredChartData.value;

  if (labels.length === 0) {
    if (chartInstance) {
      chartInstance.destroy();
      chartInstance = null;
    }
    return;
  }

  if (!chartInstance) {
    chartInstance = new Chart(canvasRef.value, {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "판매량",
            data,
            backgroundColor: colors,
            borderColor: colors.map((c) => c.replace("0.6", "1")),
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "top" },
          tooltip: { enabled: true }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  } else {
    chartInstance.data.labels = labels;
    chartInstance.data.datasets[0].data = data;
    chartInstance.data.datasets[0].backgroundColor = colors;
    chartInstance.data.datasets[0].borderColor = colors.map((c) =>
      c.replace("0.6", "1")
    );
    chartInstance.update();
  }
}

// filteredChartData가 바뀔 때마다 차트 반영 (immediate: 첫 로딩 시에도 실행)
watch(filteredChartData, updateChart, { immediate: true });
onMounted(updateChart);
</script>

<style scoped>
.interactive-chart {
  width: 600px;
  margin: 0 auto;
  padding-top: 1.5rem;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 8px;
}

.filters label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.filters input[type="range"] {
  width: 100px;
}

.filters select {
  padding: 0.25rem 0.5rem;
}

.empty {
  color: #666;
  text-align: center;
  padding: 2rem;
}

.chart-wrap {
  margin-top: 0.5rem;
}
</style>
