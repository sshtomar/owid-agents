const fs = require("fs");
const data = JSON.parse(fs.readFileSync("data/catalog/datasets/sdg--5-5-2--IC_GEN_MGTL.json", "utf8"));

const aggregateNames = new Set([
  "Africa", "Americas", "Asia", "Europe", "Oceania", "World",
  "Northern Africa", "Sub-Saharan Africa",
  "Central and Southern Asia", "Eastern and South-Eastern Asia",
  "Latin America and the Caribbean",
  "Northern America and Europe", "Australia and New Zealand",
  "Small Island Developing States (SIDS)",
  "Land-locked Developing Countries (LLDC)",
  "Least Developed Countries (LDCs)",
  "Northern America", "Western Europe", "Southern Asia", "Southern Europe",
  "Western Asia", "Northern Europe", "Eastern Europe", "Central Asia",
  "South-Eastern Asia", "Eastern Asia", "Caribbean", "Central America",
  "South America", "Western Africa", "Middle Africa", "Eastern Africa",
  "Southern Africa", "Melanesia", "Micronesia", "Polynesia"
]);

const latestByCountry = {};
data.data.forEach(d => {
  if (aggregateNames.has(d.countryName)) return;
  if (!latestByCountry[d.countryName] || d.year > latestByCountry[d.countryName].year) {
    latestByCountry[d.countryName] = d;
  }
});

const entries = Object.values(latestByCountry);
entries.sort((a, b) => b.value - a.value);

console.log("Total countries with any data:", entries.length);
console.log("");
entries.forEach(d => console.log(d.countryName + " | " + d.year + " | " + d.value));

// Also get the World aggregate trend
console.log("\n--- World trend ---");
const worldData = data.data.filter(d => d.countryName === "World").sort((a, b) => a.year - b.year);
worldData.forEach(d => console.log(d.year + " | " + d.value));

// Regional data for latest year
console.log("\n--- Regional aggregates (latest) ---");
const regionLatest = {};
data.data.forEach(d => {
  if (!aggregateNames.has(d.countryName)) return;
  if (!regionLatest[d.countryName] || d.year > regionLatest[d.countryName].year) {
    regionLatest[d.countryName] = d;
  }
});
Object.values(regionLatest).sort((a, b) => b.value - a.value).forEach(d => {
  console.log(d.countryName + " | " + d.year + " | " + d.value);
});
