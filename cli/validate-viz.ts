/**
 * Visualization Validation Harness
 *
 * Parses each HTML visualization, extracts inlined data, loads the
 * referenced catalog datasets, and flags mismatches between what
 * the chart shows and what the source data actually contains.
 *
 * Usage:
 *   npx tsx cli/validate-viz.ts              # validate all
 *   npx tsx cli/validate-viz.ts --id viz-001 # validate one
 *   npx tsx cli/validate-viz.ts --fix        # auto-fix value mismatches (future)
 */

import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { parseArgs } from "node:util";
import { readVizIndex, getDataset } from "../src/catalog.js";
import type { VizEntry, DatasetFile, DataPoint } from "../src/types.js";

const DATA_DIR = process.env.OWID_DATA_DIR ?? join(import.meta.dirname, "..", "data");
const VIZ_DIR = join(DATA_DIR, "visualizations", "viz");

// -- Types --

interface ExtractedData {
  variableName: string;
  values: Record<string, unknown>[];
  rawJson: string;
}

interface ValidationIssue {
  severity: "error" | "warning" | "info";
  message: string;
}

interface VizReport {
  vizId: string;
  title: string;
  datasetIds: string[];
  extractedArrays: number;
  extractedRows: number;
  issues: ValidationIssue[];
}

// -- Data extraction from HTML --

/**
 * Extracts JS array/object literals assigned to const/let/var in <script> tags.
 * Handles:
 *   const data = [...]
 *   const raw = [...]
 *   const data1960 = {...}
 */
function extractInlinedData(html: string): ExtractedData[] {
  const results: ExtractedData[] = [];

  // Extract contents of <script> tags (non-module and module)
  const scriptRegex = /<script[^>]*>([\s\S]*?)<\/script>/gi;
  let scriptMatch: RegExpExecArray | null;

  while ((scriptMatch = scriptRegex.exec(html)) !== null) {
    const scriptContent = scriptMatch[1];

    // Match variable assignments to arrays or objects
    // Patterns: const data = [...], let raw = [...], var items = [...]
    const assignRegex = /(?:const|let|var)\s+(\w+)\s*=\s*(\[[\s\S]*?\]);/g;
    let assignMatch: RegExpExecArray | null;

    while ((assignMatch = assignRegex.exec(scriptContent)) !== null) {
      const varName = assignMatch[1];
      const rawJson = assignMatch[2];

      try {
        // JSON.parse won't work on JS literals with unquoted keys,
        // so we normalize the common patterns
        const normalized = normalizeJsToJson(rawJson);
        const parsed = JSON.parse(normalized);

        if (Array.isArray(parsed) && parsed.length > 0) {
          results.push({
            variableName: varName,
            values: parsed as Record<string, unknown>[],
            rawJson,
          });
        }
      } catch {
        // Try a more lenient extraction: eval-like parse via Function
        // Skip -- if we can't parse it, we report it as an issue
        results.push({
          variableName: varName,
          values: [],
          rawJson,
        });
      }
    }
  }

  return results;
}

/**
 * Normalize JS object literal syntax to valid JSON.
 * Handles unquoted keys and trailing commas.
 */
function normalizeJsToJson(js: string): string {
  // Remove JS comments
  let s = js.replace(/\/\/[^\n]*/g, "").replace(/\/\*[\s\S]*?\*\//g, "");
  // Quote unquoted keys: {foo: -> {"foo":
  s = s.replace(/([{,]\s*)(\w+)\s*:/g, '$1"$2":');
  // Remove trailing commas before ] or }
  s = s.replace(/,\s*([}\]])/g, "$1");
  return s;
}

// -- Catalog data helpers --

interface SourceStats {
  countries: Set<string>;
  countryNames: Set<string>;
  years: Set<number>;
  minValue: number;
  maxValue: number;
  rowCount: number;
}

function computeSourceStats(data: DataPoint[]): SourceStats {
  const countries = new Set<string>();
  const countryNames = new Set<string>();
  const years = new Set<number>();
  let minValue = Infinity;
  let maxValue = -Infinity;

  for (const d of data) {
    countries.add(d.country);
    countryNames.add(d.countryName);
    years.add(d.year);
    if (d.value !== null) {
      if (d.value < minValue) minValue = d.value;
      if (d.value > maxValue) maxValue = d.value;
    }
  }

  return { countries, countryNames, years, minValue, maxValue, rowCount: data.length };
}

/**
 * Try to find a catalog country name that matches a chart label.
 * Chart labels are often shortened (e.g. "C. African Rep." vs "Central African Republic").
 */
function fuzzyCountryMatch(chartName: string, sourceNames: Set<string>): string | null {
  // Direct match
  if (sourceNames.has(chartName)) return chartName;

  // Case-insensitive match
  const lower = chartName.toLowerCase();
  for (const name of sourceNames) {
    if (name.toLowerCase() === lower) return name;
  }

  // Substring match (chart names are often abbreviations)
  for (const name of sourceNames) {
    if (name.toLowerCase().includes(lower) || lower.includes(name.toLowerCase())) {
      return name;
    }
  }

  // Common abbreviation patterns
  const ABBREVIATIONS: Record<string, string[]> = {
    "DR Congo": ["Congo, Dem. Rep.", "Democratic Republic of the Congo"],
    "C. African Rep.": ["Central African Republic"],
    "Korea": ["Korea, Rep.", "Korea, Dem. People's Rep."],
    "S. Korea": ["Korea, Rep."],
    "N. Korea": ["Korea, Dem. People's Rep."],
    "US": ["United States"],
    "USA": ["United States"],
    "UK": ["United Kingdom"],
    "UAE": ["United Arab Emirates"],
    "Iran": ["Iran, Islamic Rep."],
    "Egypt": ["Egypt, Arab Rep."],
    "Russia": ["Russian Federation"],
    "Venezuela": ["Venezuela, RB"],
    "Syria": ["Syrian Arab Republic"],
    "Laos": ["Lao PDR"],
    "Congo": ["Congo, Rep."],
    "Turkiye": ["Turkiye", "Turkey"],
    "Czechia": ["Czech Republic", "Czechia"],
    "Slovakia": ["Slovak Republic"],
  };

  for (const [abbr, expansions] of Object.entries(ABBREVIATIONS)) {
    if (chartName === abbr || chartName.toLowerCase() === abbr.toLowerCase()) {
      for (const exp of expansions) {
        if (sourceNames.has(exp)) return exp;
      }
    }
  }

  return null;
}

// -- Validation logic --

function validateViz(entry: VizEntry): VizReport {
  const report: VizReport = {
    vizId: entry.id,
    title: entry.title,
    datasetIds: entry.datasetIds,
    extractedArrays: 0,
    extractedRows: 0,
    issues: [],
  };

  // 1. Load HTML
  const htmlPath = join(VIZ_DIR, `${entry.id}.html`);
  if (!existsSync(htmlPath)) {
    report.issues.push({ severity: "error", message: `HTML file missing: ${htmlPath}` });
    return report;
  }

  let html: string;
  try {
    html = readFileSync(htmlPath, "utf-8");
  } catch (err) {
    report.issues.push({
      severity: "error",
      message: `Failed to read HTML: ${err instanceof Error ? err.message : String(err)}`,
    });
    return report;
  }

  // 2. Extract inlined data
  const extracted = extractInlinedData(html);
  report.extractedArrays = extracted.length;

  if (extracted.length === 0) {
    report.issues.push({
      severity: "warning",
      message: "No parseable data arrays found in HTML. May use a format not yet supported by the harness.",
    });
    return report;
  }

  const totalRows = extracted.reduce((sum, e) => sum + e.values.length, 0);
  report.extractedRows = totalRows;

  // Flag unparseable arrays
  for (const ex of extracted) {
    if (ex.values.length === 0 && ex.rawJson.length > 0) {
      report.issues.push({
        severity: "warning",
        message: `Variable '${ex.variableName}' could not be parsed. Manual review needed.`,
      });
    }
  }

  // 3. Load source datasets
  const sourceDatasets: Map<string, DatasetFile> = new Map();
  for (const dsId of entry.datasetIds) {
    const ds = getDataset(dsId);
    if (!ds) {
      report.issues.push({
        severity: "error",
        message: `Referenced dataset '${dsId}' not found in catalog.`,
      });
    } else {
      sourceDatasets.set(dsId, ds);
    }
  }

  if (sourceDatasets.size === 0) {
    report.issues.push({
      severity: "error",
      message: "No source datasets could be loaded. Cannot validate data.",
    });
    return report;
  }

  // 4. Merge all source data for cross-dataset charts
  const allSourceData: DataPoint[] = [];
  for (const ds of sourceDatasets.values()) {
    allSourceData.push(...ds.data);
  }
  const sourceStats = computeSourceStats(allSourceData);

  // 5. Validate each extracted array
  for (const ex of extracted) {
    if (ex.values.length === 0) continue;

    // Skip arrays that look like legends, config, or metadata
    const LEGEND_VAR_NAMES = ["legend", "legendItems", "legendData", "legendGroups", "legItems", "cols", "categories", "PALETTE"];
    if (LEGEND_VAR_NAMES.includes(ex.variableName)) continue;

    const sample = ex.values[0];
    const keys = Object.keys(sample);

    // Try to identify country/name fields
    const nameKeys = keys.filter((k) =>
      ["n", "name", "country", "c", "countryName", "label"].includes(k)
    );

    // Try to identify value fields
    const valueKeys = keys.filter((k) =>
      ["v", "value", "a", "b", "le", "gdp", "val", "rate", "pct", "y1960", "y2023"].includes(k)
    );

    // Try to identify year fields
    const yearKeys = keys.filter((k) =>
      ["y", "year", "yr", "date"].includes(k)
    );

    // 5a. Country name validation
    if (nameKeys.length > 0) {
      const nameKey = nameKeys[0];
      const chartNames = new Set(
        ex.values
          .map((v) => v[nameKey])
          .filter((v): v is string => typeof v === "string")
      );

      let unmatchedCount = 0;
      const unmatched: string[] = [];
      for (const chartName of chartNames) {
        const match = fuzzyCountryMatch(chartName, sourceStats.countryNames);
        if (!match) {
          unmatchedCount++;
          unmatched.push(chartName);
        }
      }

      if (unmatchedCount > 0 && unmatchedCount <= 5) {
        report.issues.push({
          severity: "warning",
          message: `${unmatchedCount} country name(s) in '${ex.variableName}' not found in source: ${unmatched.join(", ")}`,
        });
      } else if (unmatchedCount > 5) {
        report.issues.push({
          severity: "warning",
          message: `${unmatchedCount} of ${chartNames.size} country names in '${ex.variableName}' not found in source datasets. Sample: ${unmatched.slice(0, 3).join(", ")}...`,
        });
      }
    }

    // 5b. Value range validation
    for (const vk of valueKeys) {
      const chartValues = ex.values
        .map((v) => v[vk])
        .filter((v): v is number => typeof v === "number");

      if (chartValues.length === 0) continue;

      const chartMin = Math.min(...chartValues);
      const chartMax = Math.max(...chartValues);

      // Allow 20% margin for rounding / aggregation differences
      const rangeMargin = (sourceStats.maxValue - sourceStats.minValue) * 0.2;
      const lowerBound = sourceStats.minValue - rangeMargin;
      const upperBound = sourceStats.maxValue + rangeMargin;

      if (chartMin < lowerBound || chartMax > upperBound) {
        report.issues.push({
          severity: "warning",
          message: `Values in '${ex.variableName}.${vk}' [${chartMin.toFixed(1)}-${chartMax.toFixed(1)}] exceed source range [${sourceStats.minValue.toFixed(1)}-${sourceStats.maxValue.toFixed(1)}] by >20%`,
        });
      }
    }

    // 5c. Year range validation
    for (const yk of yearKeys) {
      const chartYears = ex.values
        .map((v) => v[yk])
        .filter((v): v is number => typeof v === "number" && v > 1900 && v < 2100);

      if (chartYears.length === 0) continue;

      const chartMinYear = Math.min(...chartYears);
      const chartMaxYear = Math.max(...chartYears);
      const sourceMinYear = Math.min(...sourceStats.years);
      const sourceMaxYear = Math.max(...sourceStats.years);

      if (chartMinYear < sourceMinYear - 1 || chartMaxYear > sourceMaxYear + 1) {
        report.issues.push({
          severity: "warning",
          message: `Years in '${ex.variableName}' [${chartMinYear}-${chartMaxYear}] outside source range [${sourceMinYear}-${sourceMaxYear}]`,
        });
      }
    }

    // 5d. Row count plausibility
    if (ex.values.length > sourceStats.rowCount) {
      report.issues.push({
        severity: "warning",
        message: `Chart data has ${ex.values.length} rows but source dataset(s) have ${sourceStats.rowCount} total. Chart may contain fabricated rows.`,
      });
    }
  }

  // 6. Spot-check: verify a few specific values against source
  for (const ex of extracted) {
    if (ex.values.length === 0) continue;

    const sample = ex.values[0];
    const keys = Object.keys(sample);
    const nameKey = keys.find((k) => ["n", "name", "country", "c", "countryName"].includes(k));
    const yearKey = keys.find((k) => ["y", "year", "yr"].includes(k));
    const valueKey = keys.find((k) => ["v", "value", "a", "le", "rate", "pct"].includes(k));

    if (!nameKey || !valueKey) continue;

    // Spot-check up to 3 data points
    const samplesToCheck = ex.values.slice(0, 3);
    for (const row of samplesToCheck) {
      const chartName = row[nameKey] as string;
      const chartValue = row[valueKey] as number;
      const chartYear = yearKey ? (row[yearKey] as number) : undefined;

      if (typeof chartName !== "string" || typeof chartValue !== "number") continue;

      const matchedSourceName = fuzzyCountryMatch(chartName, sourceStats.countryNames);
      if (!matchedSourceName) continue;

      // Find the corresponding source data point
      const sourceMatch = allSourceData.find((d) => {
        if (d.countryName !== matchedSourceName) return false;
        if (chartYear !== undefined && d.year !== chartYear) return false;
        return true;
      });

      if (sourceMatch && sourceMatch.value !== null) {
        const diff = Math.abs(chartValue - sourceMatch.value);
        const tolerance = Math.abs(sourceMatch.value) * 0.05; // 5% tolerance for rounding

        if (diff > tolerance && diff > 1) {
          report.issues.push({
            severity: "error",
            message: `Value mismatch: ${chartName}${chartYear ? ` (${chartYear})` : ""} chart=${chartValue}, source=${sourceMatch.value} (diff=${diff.toFixed(2)})`,
          });
        }
      }
    }
  }

  return report;
}

// -- CLI --

const { values } = parseArgs({
  args: process.argv.slice(2),
  options: {
    id: { type: "string" },
    json: { type: "boolean", default: false },
    verbose: { type: "boolean", short: "v", default: false },
  },
});

const vizIndex = readVizIndex();
let entries = vizIndex.visualizations;

if (values.id) {
  entries = entries.filter((v) => v.id === values.id);
  if (entries.length === 0) {
    console.error(`Visualization '${values.id}' not found.`);
    process.exit(1);
  }
}

const reports: VizReport[] = [];

for (const entry of entries) {
  const report = validateViz(entry);
  reports.push(report);
}

// -- Output --

if (values.json) {
  console.log(JSON.stringify(reports, null, 2));
} else {
  let totalErrors = 0;
  let totalWarnings = 0;
  let totalClean = 0;

  for (const r of reports) {
    const errors = r.issues.filter((i) => i.severity === "error");
    const warnings = r.issues.filter((i) => i.severity === "warning");
    totalErrors += errors.length;
    totalWarnings += warnings.length;

    if (errors.length === 0 && warnings.length === 0) {
      totalClean++;
      if (values.verbose) {
        console.log(`  OK  ${r.vizId} -- ${r.title} (${r.extractedRows} rows, ${r.extractedArrays} arrays)`);
      }
      continue;
    }

    const marker = errors.length > 0 ? "FAIL" : "WARN";
    console.log(`  ${marker}  ${r.vizId} -- ${r.title}`);
    console.log(`        datasets: ${r.datasetIds.join(", ")}`);
    console.log(`        extracted: ${r.extractedArrays} array(s), ${r.extractedRows} row(s)`);

    for (const issue of r.issues) {
      const prefix = issue.severity === "error" ? "  ERR " : issue.severity === "warning" ? "  WRN " : "  INF ";
      console.log(`       ${prefix} ${issue.message}`);
    }
    console.log();
  }

  console.log("---");
  console.log(`Validated ${reports.length} visualization(s): ${totalClean} clean, ${totalErrors} error(s), ${totalWarnings} warning(s)`);

  if (totalErrors > 0) {
    process.exit(1);
  }
}
