const fs = require("fs");
const data = JSON.parse(fs.readFileSync("data/catalog/datasets/wb--BX-KLT-DINV-WD-GD-ZS.json", "utf8"));

const targets = ["CN", "IE", "IN", "BR", "CL", "JP", "DE", "HK", "KR", "ID", "AU", "ET"];

targets.forEach(code => {
  const countryData = data.data.filter(d => d.country === code).sort((a, b) => a.year - b.year);
  const yearRange = countryData.length > 0 ? countryData[0].year + "-" + countryData[countryData.length - 1].year : "none";
  const values = countryData.map(d => d.value).filter(v => v !== null && v !== undefined);
  const avg = values.length > 0 ? (values.reduce((s, v) => s + v, 0) / values.length).toFixed(2) : "N/A";
  const max = values.length > 0 ? Math.max(...values).toFixed(2) : "N/A";
  const min = values.length > 0 ? Math.min(...values).toFixed(2) : "N/A";
  const name = countryData.length > 0 ? countryData[0].countryName : "unknown";
  console.log(code, name, "| range:", yearRange, "| pts:", countryData.length, "| avg:", avg, "| min:", min, "| max:", max);
});

// Now dump all the data for these countries as JSON for the viz
const vizData = {};
targets.forEach(code => {
  const countryData = data.data.filter(d => d.country === code && d.value !== null && d.value !== undefined).sort((a, b) => a.year - b.year);
  if (countryData.length > 0) {
    vizData[code] = {
      name: countryData[0].countryName,
      points: countryData.map(d => ({ year: d.year, value: Math.round(d.value * 100) / 100 }))
    };
  }
});

console.log("\n--- VIZ DATA ---");
console.log(JSON.stringify(vizData, null, 2));
