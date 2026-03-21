const fs = require("fs");
const raw = JSON.parse(fs.readFileSync("data/catalog/datasets/sdg--4-1-1--SE_TOT_PRFL.json", "utf8"));
const data = raw.data;
const countries = [...new Set(data.map(d => d.countryName))].sort();
console.log("Total data points:", data.length);
console.log("Unique countries/regions:", countries.length);

const years = [...new Set(data.map(d => d.year))].sort();
console.log("Years:", years);

const regionKeywords = ["Eastern and", "Europe and", "Latin America", "Northern Africa", "Oceania", "Central and Southern", "Sub-Saharan", "World", "Landlocked"];
const isRegion = c => regionKeywords.some(k => c.startsWith(k) || c === "Oceania" || c === "World");
const regions = countries.filter(isRegion);
const nonRegions = countries.filter(c => !isRegion(c));
console.log("Regions:", regions);
console.log("Actual countries:", nonRegions.length);

// Get latest year per country (non-regions only)
const latest = {};
data.forEach(d => {
  if (isRegion(d.countryName)) return;
  if (!latest[d.countryName] || d.year > latest[d.countryName].year) {
    latest[d.countryName] = d;
  }
});

const sorted = Object.values(latest).sort((a, b) => b.value - a.value);
console.log("\nTop 25 by latest value:");
sorted.slice(0, 25).forEach(d => console.log(`  ${d.countryName}: ${d.value}% (${d.year})`));
console.log("\nBottom 25 by latest value:");
sorted.slice(-25).forEach(d => console.log(`  ${d.countryName}: ${d.value}% (${d.year})`));

const vals = data.map(d => d.value).filter(v => v !== null);
console.log("\nValue range:", Math.min(...vals), "-", Math.max(...vals));

// Count by latest year
const yearCounts = {};
Object.values(latest).forEach(d => {
  yearCounts[d.year] = (yearCounts[d.year] || 0) + 1;
});
console.log("\nLatest year distribution:", yearCounts);

// How many have 2019+ data
const recent = Object.values(latest).filter(d => d.year >= 2019);
console.log("Countries with 2019+ data:", recent.length);

// Median value
const sortedVals = Object.values(latest).map(d => d.value).sort((a, b) => a - b);
console.log("Median latest value:", sortedVals[Math.floor(sortedVals.length / 2)]);

// Count above/below 50%
const above50 = Object.values(latest).filter(d => d.value >= 50).length;
const below50 = Object.values(latest).filter(d => d.value < 50).length;
console.log("Above 50%:", above50, "Below 50%:", below50);
