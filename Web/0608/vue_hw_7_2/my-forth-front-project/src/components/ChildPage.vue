<template>
    <div class="child-card">
        <h4>자식 페이지</h4>
        <p>{{ childName }}</p>
    </div>
</template>

<script setup>
defineProps({
    childName: String
})
</script>

<style scoped>
.child-card {
  background-color: #ffffff;  /* 하얀색 배경 */
  border: 1px solid #e0e0e0;  /* 외곽선 */
  padding: 20px;              /* 안쪽 여백 */
  margin-top: 15px;           /* 자식 상자 사이의 간격 띄우기 */
}

</style>