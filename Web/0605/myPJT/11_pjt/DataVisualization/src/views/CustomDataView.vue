<template>
  <div class="custom-dashboard">
    <header class="dashboard-intro">
      <h2>자유 데이터 자율 시각화 대시보드</h2>
      <p class="description">
        배포된 10,000건의 뉴스/정치 데이터셋(<code class="file-code">news_politics.jsonl</code>)을 
        구조 분석 및 교차 가공하여 도출한 대중 여론 통계 화면입니다. [cite: 72, 75]
      </p>
    </header>

    <div class="content-grid">
      <section class="chart-card">
        <h3 class="card-title">뉴스 카테고리별 댓글 감성 점수 평균 비교 (F308)</h3>
        <F308 />
      </section>
      <section class="chart-card">
        <h3 class="card-title">뉴스 카테고리별 댓글 감성 점수 분포 비교 (F309)</h3>
        <F309 />
      </section>
    <section class="chart-card">
        <h3 class="card-title">데이터 기반 다차원 가설 검정 복합 대시보드 (F311)</h3>
        <F311 />
      </section>
      
      </div>
  </div>
</template>

<script setup>
import F308 from '@/components/F308.vue';
import F309 from '@/components/F309.vue';
import F311 from '@/components/F311.vue';
</script>

<style scoped>
.custom-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  font-family: sans-serif;
}

.dashboard-intro {
  margin-bottom: 25px;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

h2 {
  color: #2c3e50;
  margin-top: 0;
}

.description {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.5;
}

.file-code {
  background-color: #f1f3f5;
  color: #e03131;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
}

.content-grid {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.chart-card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e9ecef;
}

.card-title {
  font-size: 1.1rem;
  margin-top: 0;
  margin-bottom: 20px;
  color: #343a40;
  border-left: 4px solid #5c7cfa; /* 로열 블루 포인트 컬러 바 */
  padding-left: 10px;
}
</style>