<template>
  <div class="dashboard-container">
    <h2 class="dashboard-title">스포츠 종합 데이터 대시보드</h2>
    
    <div class="dashboard-grid">
      
      <div class="chart-card">
        <h3 class="card-title">종목별 경기 수 시각화 (F301)</h3>
        <F301 />
      </div>

      <div class="chart-card">
        <h3 class="card-title">종목별 평균 관중 수 (F302)</h3>
        <F302 />
      </div>

      <div class="chart-card">
        <h3 class="card-title">시간 흐름에 따른 경기 추이 (F303)</h3>
        <F303 />
      </div>

      <div class="chart-card">
        <h3 class="card-title">관중 수 대비 시청률 분포 (F304)</h3>
        <F304 />
      </div>

    </div>
  </div>
</template>

<script setup>
// @/ 절대 경로 규칙을 활용하여 기존 컴포넌트들을 일괄 임포트합니다.
import F301 from '@/components/F301.vue';
import F302 from '@/components/F302.vue';
import F303 from '@/components/F303.vue';
import F304 from '@/components/F304.vue';
</script>

<style scoped>
.dashboard-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f8f9fa; /* 대시보드 몰입감을 위한 옅은 배경색 */
  min-height: 100vh;
}

.dashboard-title {
  text-align: center;
  margin-bottom: 30px;
  color: #343a40;
  font-weight: 700;
}

/* 1. 핵심 대시보드 CSS Grid 설정 */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 2열 균등 배치 */
  gap: 24px; /* 카드 간 간격 */
}

/* 2. 대시보드 품격을 높이는 카드 뷰 스타일링 */
.chart-card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); /* 은은한 그림자 효과 */
  border: 1px solid #e9ecef;
  transition: transform 0.2s ease;
}

.chart-card:hover {
  transform: translateY(-4px); /* 마우스 호버 시 살짝 떠오르는 피드백 */
}

.card-title {
  font-size: 1.1rem;
  margin-bottom: 15px;
  color: #495057;
  border-left: 4px solid #4dabf7; /* 타이틀 옆 포인트 바 */
  padding-left: 8px;
}

/* 3. 모바일 및 태블릿 화면을 위한 반응형 미디어 쿼리 */
@media (max-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: 1fr; /* 화면이 좁아지면 1열 배치로 자동 전환 */
  }
}
</style>