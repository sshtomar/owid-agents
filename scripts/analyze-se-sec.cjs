const fs = require("fs");
const raw = fs.readFileSync("data/catalog/datasets/wb--SE-SEC-ENRR.json", "utf8");
const dataset = JSON.parse(raw);

const targetCodes = ["US","GB","DE","JP","KR","BR","IN","CN","NG","ET","BD","ZA","MX","ID","EG","GH","VN","CL","PK","KE","AU","FR","IT","RU","TR","TH","PH","CO","PE","MA","TZ","MW","NE","ML","SN","RW","UG","MZ","MM","NP","LK","MY"];

const data = dataset.data;
const countriesInData = {};
data.forEach(d => {
  if (targetCodes.includes(d.country)) {
    if (countriesInData[d.country] === undefined) {
      countriesInData[d.country] = { name: d.countryName, years: [], values: [] };
    }
    countriesInData[d.country].years.push(d.year);
    countriesInData[d.country].values.push(d.value);
  }
});

Object.entries(countriesInData).forEach(([code, info]) => {
  const minY = Math.min(...info.years);
  const maxY = Math.max(...info.years);
  console.log(code + " | " + info.name + " | " + minY + "-" + maxY + " | " + info.years.length + " pts | first=" + info.values[0].toFixed(1) + " last=" + info.values[info.values.length-1].toFixed(1));
});
