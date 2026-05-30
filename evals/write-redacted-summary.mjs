#!/usr/bin/env node

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const allowedStatuses = new Set([
  'PASS',
  'FAIL',
  'BLOCKED',
  'UNVERIFIED',
  'PASS_WITH_CAVEATS',
]);
const allowedCommandIds = new Set([
  'summary-only',
  'selector-stability',
  'browser-smoke',
  'provider-full',
]);

const here = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(here, '..');
const outputPath = resolve(here, 'artifacts/latest/provider-summary.redacted.json');

function parseArgs(argv) {
  const args = {
    status: 'UNVERIFIED',
    commandId: 'summary-only',
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--') {
      continue;
    }
    if (arg === '--status') {
      args.status = argv[index + 1];
      index += 1;
      continue;
    }
    if (arg === '--command-id') {
      args.commandId = argv[index + 1];
      index += 1;
      continue;
    }
    throw new Error(`Unknown argument: ${arg}`);
  }

  if (!allowedStatuses.has(args.status)) {
    throw new Error(`Unsupported status: ${args.status}`);
  }
  if (!allowedCommandIds.has(args.commandId)) {
    throw new Error(`Unsupported command id: ${args.commandId}`);
  }

  return args;
}

function providerVersion() {
  try {
    const packageJson = JSON.parse(readFileSync(resolve(repoRoot, 'package.json'), 'utf8'));
    return String(packageJson.version ?? 'unknown');
  } catch {
    return 'unknown';
  }
}

function caseStatus(overallStatus, caseId) {
  if (overallStatus === 'PASS') {
    return 'PASS';
  }
  if (overallStatus === 'PASS_WITH_CAVEATS' && caseId !== 'fixture-provider-browser-smoke') {
    return 'PASS';
  }
  return overallStatus;
}

function buildSummary(args) {
  const version = providerVersion();
  const cases = [
    {
      case_id: 'fixture-provider-selector-stability',
      status: caseStatus(args.status, 'fixture-provider-selector-stability'),
      summary: 'Provider-owned selector stability gate for fixture pages.',
    },
    {
      case_id: 'fixture-provider-browser-smoke',
      status: caseStatus(args.status, 'fixture-provider-browser-smoke'),
      summary: 'Provider-owned browser smoke gate for fixture scenarios.',
    },
    {
      case_id: 'fixture-provider-replay-seed-contract',
      status: caseStatus(args.status, 'fixture-provider-replay-seed-contract'),
      summary: 'Provider-owned replay fixture seeding contract remains outside WebAgentFlow.',
    },
  ];

  return {
    schema_version: 'waf.eval.result.v1',
    status: args.status,
    generated_at: new Date().toISOString(),
    provider: {
      kind: 'fixture_site',
      name: 'WebAgentFlow-Fixture-Site',
      version,
    },
    target: {
      target_ref: 'fixture-site-provider',
      redacted: true,
    },
    operator_actions: [
      {
        surface: 'external_provider',
        action: 'write_redacted_provider_summary',
        command: args.commandId,
        timestamp: new Date().toISOString(),
      },
    ],
    case_results: cases,
    artifacts: [
      {
        path: 'evals/artifacts/latest/provider-summary.redacted.json',
        kind: 'redacted_provider_summary',
        redacted: true,
      },
    ],
  };
}

const args = parseArgs(process.argv.slice(2));
const summary = buildSummary(args);

mkdirSync(dirname(outputPath), { recursive: true });
writeFileSync(outputPath, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
console.log(`Wrote ${outputPath}`);
