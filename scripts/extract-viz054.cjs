const fs = require("fs");
const raw = JSON.parse(fs.readFileSync("data/catalog/datasets/wb--SP-ADO-TFRT.json", "utf8"));
const data = raw.data;

// Selected 12 countries for diverse trajectories:
// Dramatic decline: South Korea (KR), Bangladesh (BD), India (IN), Bhutan (BT)
// High-income low rates: Japan (JP), Denmark (DK)
// Moderate decline: Brazil (BR), Honduras (HN)
// High / increasing: Angola (AO), Central African Republic (CF), Chad (TD)
// Stagnant: Azerbaijan (AZ)

const selected = ["KR","BD","IN","BT","JP","DK","BR","HN","AO","CF","TD","AZ"];

const selectedData = data.filter(d => selected.includes(d.country) && d.value != null);

selected.forEach(code => {
  const rows = selectedData.filter(d => d.country === code).sort((a,b) => a.year - b.year);
  if (rows.length > 0) {
    console.log(code, rows[0].countryName, "years:", rows[0].year, "-", rows[rows.length-1].year, "points:", rows.length);
  }
});

const output = selectedData.map(d => ({
  c: d.country,
  n: d.countryName,
  y: d.year,
  v: Math.round(d.value * 10) / 10
})).sort((a,b) => a.y - b.y || a.c.localeCompare(b.c));

console.log("\nTotal data points:", output.length);
console.log("JSON size (approx):", JSON.stringify(output).length, "bytes");
console.log("\n--- DATA START ---");
console.log(JSON.stringify(output));
console.log("--- DATA END ---");
