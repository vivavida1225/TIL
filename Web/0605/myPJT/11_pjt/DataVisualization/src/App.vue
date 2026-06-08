<template>
  <div class="app-container">
    <header class="main-header">
      <h1>Data Visualization Project</h1>
      
      <nav class="nav-tabs">
        <router-link to="/sport" class="nav-btn">
          스포츠 데이터 대시보드 (F301~F306)
        </router-link>
        
        <router-link to="/custom" class="nav-btn">
          자유 데이터 분석 대시보드 (F307~F312)
        </router-link>
      </nav>
    </header>
    
    <hr class="divider" />

    <main class="view-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
// 상태 변수를 직접 제어할 필요가 없어 스크립트 영역이 완벽하게 비워집니다.
</script>

<style scoped>
.app-container {
  background-color: #f8f9fa;
  min-height: 100vh;
  padding-bottom: 40px;
}

.main-header {
  padding: 20px 20px 10px 20px;
  background-color: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 1.8rem;
}

.nav-tabs {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.nav-btn {
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  background-color: #e9ecef;
  color: #495057;
  border-radius: 8px;
  cursor: pointer;
  text-decoration: none; /* router-link가 기본 <a> 태그화되는 것 방지 */
  transition: all 0.2s ease;
}

.nav-btn:hover {
  background-color: #dee2e6;
}

/* 3. 핵심 포인트: active 클래스 대신 Vue Router가 자동으로 부여하는 클래스를 타겟팅합니다 */
.nav-btn.router-link-active {
  background-color: #2c3e50;
  color: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.divider {
  border: 0;
  height: 1px;
  background: #e9ecef;
  margin: 0 0 20px 0;
}

.view-content {
  padding: 0 20px;
}
</style>