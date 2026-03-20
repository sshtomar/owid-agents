import { parseArgs } from "node:util";
import { listDatasets, getDataset, readCatalogIndex, readVizIndex } from "../src/catalog.js";

const { positionals, values } = parseArgs({
  args: process.argv.slice(2),
  allowPositionals: true,
  options: {
    id: { type: "string" },
  },
});

const command = positionals[0];

function list() {
  const datasets = listDatasets();
  if (datasets.length === 0) {
    console.log("No datasets in catalog. Use 'discover save' to add some.");
    return;
  }

  console.log(`Catalog: ${datasets.length} dataset(s)\n`);
  for (const ds of datasets) {
    console.log(`  ${ds.id}`);
    console.log(`    ${ds.title}`);
    console.log(`    Provider: ${ds.source.provider} | Points: ${ds.dataPointCount} | Range: ${ds.dateRange.start}-${ds.dateRange.end}`);
    if (ds.topics.length > 0) console.log(`    Topics: ${ds.topics.join(", ")}`);
    console.log();
  }
}

function show() {
  const id = values.id;
  if (!id) {
    console.error("Error: --id is required");
    process.exit(1);
  }

  const dataset = getDataset(id);
  if (!dataset) {
    console.error(`Error: Dataset '${id}' not found`);
    process.exit(1);
  }

  const { meta, data } = dataset;
  console.log(`Dataset: ${meta.id}\n`);
  console.log(`Title: ${meta.title}`);
  console.log(`Description: ${meta.description}`);
  console.log(`Provider: ${meta.source.provider}`);
  console.log(`Indicator: ${meta.source.indicatorId} (${meta.source.indicatorName})`);
  console.log(`Source URL: ${meta.source.sourceUrl}`);
  console.log(`Last fetched: ${meta.source.lastFetched}`);
  console.log(`Topics: ${meta.topics.join(", ") || "(none)"}`);
  console.log(`Countries: ${meta.countries.length}`);
  console.log(`Date range: ${meta.dateRange.start} - ${meta.dateRange.end}`);
  console.log(`Data points: ${meta.dataPointCount}`);

  console.log(`\nSample data (first 10 points):`);
  for (const d of data.slice(0, 10)) {
    console.log(`  ${d.countryName} (${d.year}): ${d.value}`);
  }
}

function stats() {
  const catalog = readCatalogIndex();
  const viz = readVizIndex();

  console.log("Catalog Statistics\n");
  console.log(`Datasets: ${catalog.datasets.length}`);
  console.log(`Visualizations: ${viz.visualizations.length}`);
  console.log(`Last catalog update: ${catalog.lastUpdated}`);

  if (catalog.datasets.length > 0) {
    const providers = new Map<string, number>();
    const topicSet = new Set<string>();
    let totalPoints = 0;

    for (const ds of catalog.datasets) {
      providers.set(ds.source.provider, (providers.get(ds.source.provider) ?? 0) + 1);
      ds.topics.forEach((t) => topicSet.add(t));
      totalPoints += ds.dataPointCount;
    }

    console.log(`\nBy provider:`);
    for (const [p, count] of providers) {
      console.log(`  ${p}: ${count}`);
    }
    console.log(`\nTotal data points: ${totalPoints.toLocaleString()}`);
    if (topicSet.size > 0) {
      console.log(`Topics: ${[...topicSet].join(", ")}`);
    }
  }
}

switch (command) {
  case "list":
    list();
    break;
  case "show":
    show();
    break;
  case "stats":
    stats();
    break;
  default:
    console.log(`Usage: catalog <command> [options]

Commands:
  list      List all datasets in the catalog
  show      Show details for a specific dataset
            --id <string>
  stats     Show catalog statistics`);
}
