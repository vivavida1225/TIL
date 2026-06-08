// src/composables/useChartDownload.js
export function useChartDownload() {
  /**
   * @param {Object} chartInstance - Chart.js 인스턴스 객체
   * @param {String} fileName - 저장될 파일명 기본값
   */
  const downloadChart = (chartInstance, fileName = 'chart-export') => {
    if (!chartInstance) {
      console.warn('다운로드할 차트 인스턴스가 존재하지 않습니다.');
      return;
    }

    // 1. Chart.js 내장 메서드로 차트 그래픽을 Base64 데이터 주소(URL)로 추출 
    const imageLink = chartInstance.toBase64Image();

    // 2. 가상 <a> 태그를 생성하여 다운로드 트리거 수행 
    const link = document.createElement('a');
    link.download = `${fileName}.png`; // 저장될 확장자명 지정 
    link.href = imageLink;
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link); // 다운로드 후 가상 태그 제거
  };

  return { downloadChart };
}