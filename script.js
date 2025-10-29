// Replace <USERNAME> and <REPO> with your actual GitHub username and repository name
const normalCsvUrl = "https://raw.githubusercontent.com/fatimataha22/webscraping-automation/main/bitcoin_hourly_data.csv";
const optimizedCsvUrl = "https://raw.githubusercontent.com/fatimataha22/webscraping-automation/main/optimized_bitcoin_hourly_data.csv";

async function fetchAndDisplayCsv(csvUrl, containerId) {
  try {
    const response = await fetch(csvUrl);
    if (!response.ok) throw new Error("Network response was not ok " + response.statusText);
    const csvText = await response.text();
    const rows = csvText.trim().split("\n").map(row => row.split(","));
    createTable(rows, containerId);
  } catch (error) {
    console.error(`Error fetching CSV from ${csvUrl}:`, error);
    document.getElementById(containerId).innerHTML = `<p style="color: red;">Failed to load data.</p>`;
  }
}

function createTable(rows, containerId) {
  let html = "<table><thead><tr>";
  rows[0].forEach(header => { html += `<th>${header}</th>`; });
  html += "</tr></thead><tbody>";
  for (let i = 1; i < rows.length; i++) {
    html += "<tr>";
    rows[i].forEach(cell => { html += `<td>${cell}</td>`; });
    html += "</tr>";
  }
  html += "</tbody></table>";
  document.getElementById(containerId).innerHTML = html;
}

window.addEventListener("DOMContentLoaded", () => {
  fetchAndDisplayCsv(normalCsvUrl, "data-container");
  fetchAndDisplayCsv(optimizedCsvUrl, "optimized-data-container");
});
