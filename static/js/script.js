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
  
     // 🔘 내부 미리보기 실행 버튼
     const previewButton = document.createElement('button');
     previewButton.className = 'link-button';
     previewButton.textContent = '🔍 Preview Jobs';
     previewButton.addEventListener('click', () => {
     fetchJobPreview(role, city);  // 🔥 미리보기 카드 출력
    });

     // 🌐 외부 Google 검색 링크 (선택 사항)
     const googleLink = document.createElement('a');
     googleLink.href = `https://www.google.com/search?q=${encodeURIComponent(role)} Job in ${encodeURIComponent(city)}`;
     googleLink.target = "_blank";
     googleLink.className = 'link-text-link';
     googleLink.textContent = '🌐 Google Search';
  
     // 조립
     card.appendChild(title);
     card.appendChild(previewButton);
     card.appendChild(googleLink); // 선택
     jobLinks.appendChild(card);
    });
  }


function fetchJobPreview(role, city) {
    fetch(`/job_preview/${role}/${city}`)
      .then(response => response.json())
      .then(data => {
        const container = document.getElementById("job-results");
        container.innerHTML = "";
  
        data.slice(0, 5).forEach(job => {
          const card = `
            <div class="card">
              <h4>${job.title}</h4>
              <p><strong>From:</strong> ${job.source}</p>
              <p>${job.snippet}</p>
              <a href="${job.link}" target="_blank">🔗 View Job</a>
            </div>
          `;
          container.innerHTML += card;
        });
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
    updateJobLinks(citySelect.value);  // 기존 카드 링크 렌더링
  
    // 🔥 첫 번째 직무로 Job Preview 카드도 자동 불러오기
    const selectedCity = citySelect.value;
    const firstRole = roles[0]; // 가장 첫 직무
    if (firstRole && selectedCity) {
      fetchJobPreview(firstRole, selectedCity);
    }
  });