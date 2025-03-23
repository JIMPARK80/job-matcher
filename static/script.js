const citySelect = document.getElementById("city-select");
const customCity = document.getElementById("custom-city");
const jobLinks = document.getElementById("job-links");
const roles = JSON.parse(document.getElementById("roles-json").textContent);

// ✅ 링크 카드 전체 업데이트 함수
function updateJobLinks(city) {
    jobLinks.innerHTML = '';
    roles.forEach(role => {
      // 🔹 카드 wrapper
      const card = document.createElement('div');
      card.className = 'link-card';
  
      // 🔹 직무명
      const title = document.createElement('div');
      title.className = 'link-role';
      title.textContent = role;
  
      // 🔹 검색 버튼
      const link = document.createElement('a');
      link.href = `https://www.google.com/search?q=${encodeURIComponent(role)} Job in ${encodeURIComponent(city)}`;
      link.target = "_blank";
      link.className = 'link-button';
      link.innerHTML = '🔍 Search Job';
  
      // 조립
      card.appendChild(title);
      card.appendChild(link);
      jobLinks.appendChild(card);
    });
  }


  // ✅ 도시 선택 이벤트
citySelect.addEventListener("change", () => {
    const selected = citySelect.value;
    if (selected === "Custom") {
      customCity.style.display = "inline-block";
    } else {
      customCity.style.display = "none";
      updateJobLinks(selected);
    }
  });
  
  // ✅ 사용자 정의 도시 입력 이벤트
  customCity.addEventListener("input", () => {
    if (customCity.value.trim() !== "") {
      updateJobLinks(customCity.value.trim());
    }
  });
  
  // ✅ 초기 실행
  window.addEventListener("DOMContentLoaded", () => {
    updateJobLinks(citySelect.value);  // 초기 선택값으로 렌더링
  });