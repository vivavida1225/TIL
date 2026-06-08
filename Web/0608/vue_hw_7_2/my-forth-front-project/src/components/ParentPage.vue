<template>
    <div class="parent-container">
        <h3>부모 컴포넌트</h3>
        <p>{{ family.father }}</p>
        <p>{{ family.mother }}</p>
        <ChildPage 
        v-for="child in family.children"
        :key="child.name"
        :child-name="child.name"
        />
    </div>
</template>

<script setup>
import ChildPage from '@/components/ChildPage.vue';

defineProps({
    family: Object
})

</script>

<style scoped>
.parent-container {
  text-align: center;         /* 내부의 모든 글자와 상자를 한 방에 가운데 정렬 (상속) */
  background-color: #f9f9f9;  /* 연한 회색 배경 */
  border: 1px solid #e0e0e0;  /* 외곽선 */
  padding: 30px;              /* 안쪽 여백 */
  max-width: 600px;           /* 화면에 보기 좋은 적당한 너비 제한 */
  margin: 20px auto;          /* 화면 중앙 정렬 */
}

</style>