const fs = require("fs");
const raw = fs.readFileSync("data/catalog/datasets/wb--SE-SEC-ENRR.json", "utf8");
const dataset = JSON.parse(raw);

// 12 countries spanning development levels with good coverage
const selected = ["CN","ID","KE","EG","ET","GH","BD","IN","FR","DE","KR","CL"];

const data = dataset.data;
const byCountry = {};
data.forEach(d => {
  if (selected.includes(d.country)) {
    if (byCountry[d.country] === undefined) {
      byCountry[d.country] = [];
    }
    byCountry[d.country].push({ year: d.year, value: parseFloat(d.value.toFixed(1)), name: d.countryName });
  }
});

// Print JSON for each country
selected.forEach(code => {
  if (byCountry[code]) {
    const sorted = byCountry[code].sort((a, b) => a.year - b.year);
    console.log(code + " (" + sorted[0].name + "): " + sorted.length + " points, " + sorted[0].year + "-" + sorted[sorted.length-1].year);
    // Print first and last few
    sorted.forEach(d => {
      console.log("  " + d.year + ": " + d.value);
    });
  }
});
