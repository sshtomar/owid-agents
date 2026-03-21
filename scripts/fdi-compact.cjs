const fs = require("fs");
const data = JSON.parse(fs.readFileSync("data/catalog/datasets/wb--BX-KLT-DINV-WD-GD-ZS.json", "utf8"));

const targets = ["CN", "IE", "IN", "BR", "CL", "JP", "KR", "ID", "AU", "ET"];
const nameOverrides = {
  "CN": "China",
  "IE": "Ireland",
  "IN": "India",
  "BR": "Brazil",
  "CL": "Chile",
  "JP": "Japan",
  "KR": "South Korea",
  "ID": "Indonesia",
  "AU": "Australia",
  "ET": "Ethiopia"
};

const result = {};
targets.forEach(code => {
  const countryData = data.data
    .filter(d => d.country === code && d.value !== null && d.value !== undefined)
    .sort((a, b) => a.year - b.year);
  if (countryData.length > 0) {
    result[code] = {
      name: nameOverrides[code] || countryData[0].countryName,
      data: countryData.map(d => [d.year, Math.round(d.value * 100) / 100])
    };
  }
});

// Output compact format
console.log(JSON.stringify(result));
