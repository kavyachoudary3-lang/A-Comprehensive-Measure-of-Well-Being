const form = document.getElementById('hdi-form');
const results = document.getElementById('results');

const scenarioValues = {
  1: {
    life_expectancy: 82,
    mean_years_schooling: 13.5,
    expected_years_schooling: 17.5,
    gni_per_capita: 62000,
  },
  2: {
    life_expectancy: 72,
    mean_years_schooling: 8.5,
    expected_years_schooling: 12.2,
    gni_per_capita: 9500,
  },
  3: {
    life_expectancy: 61,
    mean_years_schooling: 4.2,
    expected_years_schooling: 8,
    gni_per_capita: 1800,
  },
};

function populateForm(values) {
  document.getElementById('lifeExpectancy').value = values.life_expectancy;
  document.getElementById('meanYearsSchooling').value = values.mean_years_schooling;
  document.getElementById('expectedYearsSchooling').value = values.expected_years_schooling;
  document.getElementById('gniPerCapita').value = values.gni_per_capita;
}

document.querySelectorAll('.scenario-btn').forEach((button) => {
  button.addEventListener('click', () => {
    populateForm(scenarioValues[button.dataset.scenario]);
  });
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = {
    life_expectancy: document.getElementById('lifeExpectancy').value,
    mean_years_schooling: document.getElementById('meanYearsSchooling').value,
    expected_years_schooling: document.getElementById('expectedYearsSchooling').value,
    gni_per_capita: document.getElementById('gniPerCapita').value,
  };

  const response = await fetch('/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  if (!response.ok) {
    results.innerHTML = `<h2>Prediction</h2><p>${data.error || 'Unable to predict right now.'}</p>`;
    return;
  }

  results.innerHTML = `
    <h2>Prediction</h2>
    <p class="result-badge">${data.category} HDI</p>
    <p>Composite score: <strong>${data.score_percent}%</strong></p>
    <div class="metric-list">
      <div>Health score: <strong>${data.health_score}</strong></div>
      <div>Education score: <strong>${data.education_score}</strong></div>
      <div>Income score: <strong>${data.income_score}</strong></div>
    </div>
  `;
});
