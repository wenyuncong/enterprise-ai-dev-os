#!/usr/bin/env node
// CLI smoke tests for scripts/js/cli.mjs (init --lite + validate).
// Run: node scripts/js/test_cli.mjs
// Exit 0 when all assertions pass.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, rmSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CLI = resolve(__dirname, 'cli.mjs');

test('cli init --lite creates a working project skeleton', () => {
  const target = mkdtempSync(join(tmpdir(), 'eaios-lite-'));
  try {
    const out = execFileSync(process.execPath, [CLI, 'init', target, '--lite'], { encoding: 'utf8' });
    assert.match(out, /Root AI entrypoint/);
    assert.ok(existsSync(join(target, 'AGENTS.md')), 'AGENTS.md must be created');
    assert.ok(existsSync(join(target, 'rules', 'AGENTS.md')), 'rules/AGENTS.md must be created');
    assert.ok(existsSync(join(target, 'docs', '全项目总控', 'TASK_BACKLOG.md')), 'TASK_BACKLOG.md must be created');
    assert.ok(existsSync(join(target, 'docs', '每日调研回写')), 'writeback dir must be created');
  } finally {
    rmSync(target, { recursive: true, force: true });
  }
});

test('cli validate reports OK for an initialized project', () => {
  const target = mkdtempSync(join(tmpdir(), 'eaios-val-'));
  try {
    execFileSync(process.execPath, [CLI, 'init', target, '--lite'], { encoding: 'utf8' });
    const out = execFileSync(process.execPath, [CLI, 'validate', target], { encoding: 'utf8' });
    assert.match(out, /\[OK\]/);
    assert.doesNotMatch(out, /\[MISS\]/);
  } finally {
    rmSync(target, { recursive: true, force: true });
  }
});

test('cli usage prints GitHub-direct note', () => {
  const out = execFileSync(process.execPath, [CLI], { encoding: 'utf8' });
  assert.match(out, /enterprise-ai-dev-os/);
  assert.match(out, /Until the npm package is published/);
});
