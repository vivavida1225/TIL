<script setup>
import { ref, computed } from "vue";

// 💡 부모에게 상속받는 props를 모두 제거하고 내부에 직접 데이터를 선언합니다.

// 1. 이미지 UI와 똑같은 헤더 구조 정의
const headers = ref([
  { key: "id", title: "ID" },
  { key: "title", title: "책 제목" },
  { key: "rating", title: "평점" },
  { key: "sales_volume", title: "판매량" },
  { key: "number_of_reviews", title: "리뷰 수" },
]);

// 2. book_publishing.jsonl 파일 및 이미지 기반의 상위 5개 데이터 구성
const tableData = ref([
  { id: 1, title: "세이노의 가르침", rating: 4.7, sales_volume: 2000000, number_of_reviews: 100000 },
  { id: 2, title: "어린 왕자", rating: 4.9, sales_volume: 2000000, number_of_reviews: 120000 },
  { id: 3, title: "사피엔스", rating: 4.6, sales_volume: 1800000, number_of_reviews: 95000 },
  { id: 4, title: "불편한 편의점", rating: 4.5, sales_volume: 1500000, number_of_reviews: 80000 },
  { id: 5, title: "나는 나로 살기로 했다", rating: 4.3, sales_volume: 1300000, number_of_reviews: 75000 },
]);

const sortColumn = ref(null); // 현재 정렬 컬럼의 key
const sortDirection = ref("asc"); // 'asc' 또는 'desc'

const sortedData = computed(() => {
  // 💡 props.initialData 대신 내부 데이터(tableData)를 참조하도록 변경
  if (!tableData.value || tableData.value.length === 0 || !sortColumn.value) {
    return tableData.value;
  }

  const dataCopy = [...tableData.value];
  const column = sortColumn.value;
  const direction = sortDirection.value;

  dataCopy.sort((a, b) => {
    const aValue = a[column];
    const bValue = b[column];

    // 문자열 비교 (대소문자 구분 없이, 한국어 고려)
    if (typeof aValue === "string" && typeof bValue === "string") {
      const comparison = aValue.localeCompare(bValue, "ko", {
        sensitivity: "base",
      });
      return direction === "asc" ? comparison : -comparison;
    }

    // 숫자 비교
    if (aValue < bValue) {
      return direction === "asc" ? -1 : 1;
    }
    if (aValue > bValue) {
      return direction === "asc" ? 1 : -1;
    }
    return 0;
  });

  return dataCopy;
});

/**
 * 헤더 클릭 시 정렬 상태를 업데이트합니다.
 */
function handleHeaderClick(columnKey) {
  if (sortColumn.value === columnKey) {
    sortDirection.value = sortDirection.value === "asc" ? "desc" : "asc";
  } else {
    sortColumn.value = columnKey;
    sortDirection.value = "asc";
  }
}

/**
 * 현재 정렬 상태에 따른 Material Icon 텍스트를 반환합니다.
 */
function getSortIcon(key) {
  if (sortColumn.value !== key) {
    return "unfold_more"; 
  }
  return sortDirection.value === "asc" ? "arrow_upward" : "arrow_downward";
}
</script>

<template>
  <div class="sortable-table__container">
    <h3 class="table-title">상위 5개 판매량 통계</h3>

    <table class="sortable-table__table">
      <thead>
        <tr>
          <th
            v-for="header in headers"
            :key="header.key"
            :data-key="header.key"
            class="sortable-table__header"
            :class="{ sorted: sortColumn === header.key }"
            @click="handleHeaderClick(header.key)"
          >
            <span class="header-text">{{ header.title }}</span>
            <span class="material-symbols-outlined sort-icon">{{ getSortIcon(header.key) }}</span>
          </th>
        </tr>
      </thead>
      <tbody class="sortable-table__body">
        <tr v-for="(book, index) in sortedData" :key="index">
          <td v-for="header in headers" :key="header.key">
            {{ book[header.key] }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
/* 💡 이미지처럼 제목 스타일을 중앙 정렬로 추가 */
.table-title {
  text-align: center;
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 1.25rem;
  color: #1a202c;
}

.sortable-table__container {
  width: 100%;
  height: 100%;
}

/* Table Style */
.sortable-table__table {
  width: 100%;
  height: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

/* Table Header Style */
.sortable-table__header {
  background-color: #e9eff5;
  color: #4a5568;
  padding: 12px 16px;
  text-align: left;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s ease;
  user-select: none;
  position: relative; 
}

.sortable-table__header:hover {
  background-color: #dce3eb;
}

.sortable-table__header .header-text {
  margin-right: 5px;
}

.sort-icon {
  font-size: 18px;
  vertical-align: middle;
  transition: color 0.2s ease, opacity 0.2s ease;
  color: #718096; 
  opacity: 0.7;
}

.sortable-table__header.sorted {
  background-color: #90EE90; 
  color: #ffffff;
  font-weight: 700;
}

.sortable-table__header.sorted .sort-icon {
  color: #ffffff; 
  opacity: 1;
}

.sortable-table__body tr {
  transition: background-color 0.15s ease;
}

.sortable-table__body tr:nth-child(even) {
  background-color: #f7fafc;
}

.sortable-table__body tr:hover {
  background-color: #edf2f7;
}

.sortable-table__body td {
  padding: 12px 16px;
  border-bottom: 1px solid #e2e8f0;
  color: #4a5568;
}

/* 둥근 모서리 적용 */
.sortable-table__table thead tr:first-child .sortable-table__header:first-child {
  border-top-left-radius: 8px;
}
.sortable-table__table thead tr:first-child .sortable-table__header:last-child {
  border-top-right-radius: 8px;
}
.sortable-table__body tr:last-child td:first-child {
  border-bottom-left-radius: 8px;
}
.sortable-table__body tr:last-child td:last-child {
  border-bottom-right-radius: 8px;
}
.sortable-table__body tr:last-child td {
  border-bottom: none;
}
</style>