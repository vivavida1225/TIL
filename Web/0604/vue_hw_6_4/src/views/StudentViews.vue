<template>
    <div>
        <h3>학생들 상세 정보 목록입니다.</h3>
        <p v-for="student in students" :key="student.name">
            <!-- 방법 1. 선언식으로 작성
            <RouterLink :to="{name: 'studentDetail', params: {name: student.name}}">
                {{ student.name }} 학생 정보 보기
            </RouterLink> -->
            <!-- 방법 2. 프로그래밍식 작성 -->
             <span class="link-style" @click="goToDetail(student.name)">
                {{ student.name }} 학생 정보 보기
             </span>
        </p>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

    const students = [
        {name: '김하나'},
        {name: '김두리'},
        {name: '김서이'},
    ]

// 프로그래밍식을 위해: router 인스턴스 & 이동 위한 함수 정의
const router = useRouter()
const goToDetail = function(studentName) {
    router.push({
        name: 'studentDetail',
        params: {name: studentName}
        // or
        //router.push(`/students/${studentName}`)
    })
}
</script>

<style scoped>
.link-style {
  /* color: blue;
  text-decoration: underline; */
  cursor: pointer; /* 마우스를 올렸을 때 손가락 모양으로 변하게 */
}
</style>