const citySelect = document.getElementById("city-select");
const customCity = document.getElementById("custom-city");
const jobLinks = document.getElementById("job-links");
const roles = JSON.parse(document.getElementById("roles-json").textContent);

function updateJobLinks(city) {
  jobLinks.innerHTML = '';
  roles.forEach(role => {
    const link = document.createElement('a');
    link.href = `https://www.google.com/search?q=${encodeURIComponent(role)} Job in ${encodeURIComponent(city)}`;
    link.target = "_blank";
    link.textContent = `${role} Job in ${city}`;

    const li = document.createElement('li');
    li.appendChild(link);
    jobLinks.appendChild(li);
  });
}

citySelect.addEventListener("change", () => {
  const selected = citySelect.value;
  if (selected === "Custom") {
    customCity.style.display = "inline-block";
  } else {
    customCity.style.display = "none";
    updateJobLinks(selected);
  }
});

customCity.addEventListener("input", () => {
  if (customCity.value.trim() !== "") {
    updateJobLinks(customCity.value.trim());
  }
});
