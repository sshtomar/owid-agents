import { parseArgs } from "node:util";
import * as worldBank from "../src/api-clients/world-bank.js";
import * as whoGho from "../src/api-clients/who-gho.js";
import * as unSdg from "../src/api-clients/un-sdg.js";
import * as eurostat from "../src/api-clients/eurostat.js";
import * as unhcr from "../src/api-clients/unhcr.js";
import * as imf from "../src/api-clients/imf.js";
import * as owid from "../src/api-clients/owid.js";
import * as unesco from "../src/api-clients/unesco.js";
import * as irena from "../src/api-clients/irena.js";
import * as ember from "../src/api-clients/ember.js";
import * as eia from "../src/api-clients/eia.js";
import { addDataset } from "../src/catalog.js";
import type { DatasetEntry, DatasetFile, Provider } from "../src/types.js";

const { values, positionals } = parseArgs({
  args: process.argv.slice(2),
  allowPositionals: true,
  options: {
    provider: { type: "string", short: "p" },
    topic: { type: "string", short: "t" },
    query: { type: "string", short: "q" },
    indicator: { type: "string", short: "i" },
    countries: { type: "string", short: "c" },
    title: { type: "string" },
    topics: { type: "string" },
    limit: { type: "string", short: "l" },
  },
});

const command = positionals[0];

// eslint-disable-next-line @typescript-eslint/no-explicit-any -- API clients share a loose interface
function getProvider(): { provider: Provider; client: any } {
  const p = values.provider as Provider;
  if (p === "world-bank") return { provider: p, client: worldBank };
  if (p === "who-gho") return { provider: p, client: whoGho };
  if (p === "un-sdg") return { provider: p, client: unSdg };
  if (p === "eurostat") return { provider: p, client: eurostat };
  if (p === "unhcr") return { provider: p, client: unhcr };
  if (p === "imf") return { provider: p, client: imf };
  if (p === "owid") return { provider: p, client: owid };
  if (p === "unesco") return { provider: p, client: unesco };
  if (p === "irena") return { provider: p, client: irena };
  if (p === "ember") return { provider: p, client: ember };
  if (p === "eia") return { provider: p, client: eia };
  console.error(
    "Error: --provider must be one of: world-bank, who-gho, un-sdg, eurostat, unhcr, imf, owid, unesco, irena, ember, eia"
  );
  process.exit(1);
}

async function search() {
  const { provider, client } = getProvider();
  const query = values.topic ?? values.query;
  if (!query) {
    console.error("Error: --topic or --query is required for search");
    process.exit(1);
  }
  const limit = values.limit ? parseInt(values.limit, 10) : 20;

  console.log(`Searching ${provider} for "${query}" (limit: ${limit})...\n`);
  const results = await client.searchIndicators(query, limit);

  if (results.length === 0) {
    console.log("No indicators found.");
    return;
  }

  console.log(`Found ${results.length} indicators:\n`);
  for (const r of results) {
    console.log(`  ${r.id}`);
    console.log(`    ${r.name}`);
    if (r.description) console.log(`    ${r.description.slice(0, 120)}...`);
    if (r.topics.length > 0) console.log(`    Topics: ${r.topics.join(", ")}`);
    console.log();
  }
}

async function fetchData() {
  const { provider, client } = getProvider();
  const indicator = values.indicator;
  if (!indicator) {
    console.error("Error: --indicator is required for fetch");
    process.exit(1);
  }

  console.log(`Fetching ${provider} indicator ${indicator}...`);
  const result = await client.fetchIndicatorData(indicator, values.countries);

  console.log(`\nIndicator: ${result.name}`);
  console.log(`Data points: ${result.data.length}`);

  if (result.data.length > 0) {
    const countries = [...new Set(result.data.map((d: any) => d.country))];
    const years = result.data.map((d: any) => d.year);
    console.log(`Countries: ${countries.length}`);
    console.log(`Year range: ${Math.min(...years)} - ${Math.max(...years)}`);
    console.log(`\nSample (first 5 points):`);
    for (const d of result.data.slice(0, 5)) {
      console.log(`  ${d.countryName} (${d.year}): ${d.value}`);
    }
  }
}

async function save() {
  const { provider, client } = getProvider();
  const indicator = values.indicator;
  if (!indicator) {
    console.error("Error: --indicator is required for save");
    process.exit(1);
  }

  console.log(`Fetching ${provider} indicator ${indicator}...`);
  const result = await client.fetchIndicatorData(indicator, values.countries);

  if (result.data.length === 0) {
    console.error("Error: No data returned for this indicator");
    process.exit(1);
  }

  const countries: string[] = [...new Set(result.data.map((d: any) => d.country))] as string[];
  const years = result.data.map((d: any) => d.year);
  const prefixMap: Record<Provider, string> = {
    "world-bank": "wb",
    "who-gho": "who",
    "un-sdg": "sdg",
    eurostat: "eu",
    unhcr: "unhcr",
    imf: "imf",
    owid: "owid",
    unesco: "unesco",
    irena: "irena",
    ember: "ember",
    eia: "eia",
  };
  const prefix = prefixMap[provider];
  const idSafe = indicator.replace(/[.:]/g, "-");
  const id = `${prefix}--${idSafe}`;

  const sourceUrl = client.getSourceUrl(indicator);

  const entry: DatasetEntry = {
    id,
    title: values.title ?? result.name,
    description: `${result.name} from ${provider}`,
    source: {
      provider,
      indicatorId: indicator,
      indicatorName: result.name,
      sourceUrl,
      lastFetched: new Date().toISOString(),
    },
    topics: values.topics?.split(",").map((t) => t.trim()) ?? [],
    countries,
    dateRange: {
      start: String(Math.min(...years)),
      end: String(Math.max(...years)),
    },
    dataPointCount: result.data.length,
    dataFilePath: `datasets/${id}.json`,
  };

  const file: DatasetFile = {
    meta: entry,
    data: result.data,
  };

  await addDataset(entry, file);
  console.log(`\nSaved dataset: ${id}`);
  console.log(`  Title: ${entry.title}`);
  console.log(`  Data points: ${result.data.length}`);
  console.log(`  Countries: ${countries.length}`);
  console.log(`  Year range: ${entry.dateRange.start} - ${entry.dateRange.end}`);
}

async function main() {
  switch (command) {
    case "search":
      await search();
      break;
    case "fetch":
      await fetchData();
      break;
    case "save":
      await save();
      break;
    default:
      console.log(`Usage: discover <command> [options]

Commands:
  search    Search for indicators
            --provider <world-bank|who-gho|un-sdg|eurostat>
            --topic <string>        Topic filter
            --query <string>        Keyword search
            --limit <number>        Max results (default: 20)

  fetch     Preview data for an indicator
            --provider <world-bank|who-gho|un-sdg|eurostat>
            --indicator <string>
            --countries <string>    Comma-separated ISO3 codes

  save      Fetch and save a dataset to the catalog
            --provider <world-bank|who-gho|un-sdg|eurostat>
            --indicator <string>
            --title <string>        Human-readable title
            --topics <string>       Comma-separated topic tags`);
  }
}

main().catch((err) => {
  console.error("Error:", err instanceof Error ? err.message : err);
  process.exit(1);
});
