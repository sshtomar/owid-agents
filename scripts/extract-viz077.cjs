const fs = require("fs");
const raw = JSON.parse(fs.readFileSync("data/catalog/datasets/sdg--4-1-1--SE_TOT_PRFL.json", "utf8"));
const data = raw.data;

// Filter out regions and aggregates
const regionKeywords = ["Eastern and", "Europe and", "Latin America", "Northern Africa", "Oceania", "Central and Southern", "Sub-Saharan", "World", "Landlocked"];
const isRegion = c => regionKeywords.some(k => c.startsWith(k) || c === "Oceania" || c === "World");

// Get latest value per country, filter to 2019+ only
const latest = {};
data.forEach(d => {
  if (isRegion(d.countryName)) return;
  if (d.value === null) return;
  if (!latest[d.countryName] || d.year > latest[d.countryName].year) {
    latest[d.countryName] = d;
  }
});

// Filter to 2019+
const recent = Object.values(latest).filter(d => d.year >= 2019);
recent.sort((a, b) => b.value - a.value);

// Shorten some long country names
const nameMap = {
  "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
  "China, Hong Kong Special Administrative Region": "Hong Kong",
  "China, Macao Special Administrative Region": "Macao",
  "Russian Federation": "Russia",
  "Republic of Korea": "South Korea",
  "Netherlands (Kingdom of the)": "Netherlands",
  "Bolivia (Plurinational State of)": "Bolivia",
  "Democratic Republic of the Congo": "DR Congo",
  "Lao People's Democratic Republic": "Laos",
  "United Republic of Tanzania": "Tanzania",
  "T\u00fcrkiye": "Turkey",
  "Republic of Moldova": "Moldova",
  "North Macedonia": "N. Macedonia",
  "Brunei Darussalam": "Brunei",
  "United Arab Emirates": "UAE",
  "Iran (Islamic Republic of)": "Iran",
  "Bosnia and Herzegovina": "Bosnia & Herzegovina",
  "State of Palestine": "Palestine",
  "Syrian Arab Republic": "Syria",
  "C\u00f4te d'Ivoire": "Cote d'Ivoire",
  "Trinidad and Tobago": "Trinidad & Tobago",
  "Eswatini (Kingdom of)": "Eswatini"
};

const chartData = recent.map(d => ({
  name: nameMap[d.countryName] || d.countryName,
  value: Math.round(d.value * 10) / 10,
  year: d.year
}));

console.log("Total countries with 2019+ data:", chartData.length);
console.log("\nAll entries:");
chartData.forEach(d => console.log(`  ${d.name}: ${d.value}% (${d.year})`));

// Output as JSON for embedding
console.log("\n\nJSON for chart:");
console.log(JSON.stringify(chartData, null, 2));
