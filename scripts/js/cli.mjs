#!/usr/bin/env node
// Enterprise AI Methodology CLI
// Usage: npx enterprise-ai-methodology <command>

import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, statSync, copyFileSync } from 'node:fs';
import { join, dirname, resolve, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PKG_ROOT = resolve(__dirname, '..', '..');

const USAGE = `
enterprise-ai-methodology <command>

Commands:
  init [path]      Initialize methodology in a project (default: current dir)
    --lite          Use lite version (2 rules, minimal docs)
    --full          Use full version (42 skills, all docs) [default]

  validate [path]  Check project methodology health
  sync [path]      Sync skills from upstream source

Examples:
  npx enterprise-ai-methodology init ./my-project --lite
  npx enterprise-ai-methodology validate
`;

function usage() {
  console.log(USAGE);
  process.exit(0);
}

function copyDir(src, dest) {
  if (!existsSync(src)) return;
  mkdirSync(dest, { recursive: true });
  for (const entry of readdirSync(src)) {
    const srcPath = join(src, entry);
    const destPath = join(dest, entry);
    if (statSync(srcPath).isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      copyFileSync(srcPath, destPath);
    }
  }
}

function countFiles(dir) {
  if (!existsSync(dir)) return 0;
  let count = 0;
  for (const entry of readdirSync(dir)) {
    const p = join(dir, entry);
    if (statSync(p).isDirectory()) {
      count += countFiles(p);
    } else {
      count++;
    }
  }
  return count;
}

// ── init ──────────────────────────────────────────────
function cmdInit(targetPath, mode = 'full') {
  const target = resolve(targetPath || '.');
  const sourceRoot = mode === 'lite'
    ? join(PKG_ROOT, 'lite')
    : PKG_ROOT;

  console.log(`\n  Initializing ${mode === 'lite' ? 'lite' : 'full'} methodology in:`);
  console.log(`  ${target}\n`);

  const copies = mode === 'lite' ? [
    { src: join(sourceRoot, 'rules'), dest: join(target, 'rules'), label: 'Rules engine' },
    { src: join(sourceRoot, 'docs', '_templates'), dest: join(target, 'docs', '_templates'), label: 'Doc templates' },
  ] : [
    { src: join(sourceRoot, 'rules'), dest: join(target, 'rules'), label: 'Rules engine' },
    { src: join(sourceRoot, 'skills', 'core'), dest: join(target, 'skills', 'core'), label: 'Core skills (7)' },
    { src: join(sourceRoot, 'skills', 'governance'), dest: join(target, 'skills', 'governance'), label: 'Governance skills (4)' },
    { src: join(sourceRoot, 'docs', '_templates'), dest: join(target, 'docs', '_templates'), label: 'Doc templates' },
  ];

  for (const { src, dest, label } of copies) {
    if (!existsSync(src)) {
      console.log(`  [SKIP] ${label} — source not found`);
      continue;
    }
    copyDir(src, dest);
    const n = countFiles(dest);
    console.log(`  [OK]   ${label} (${n} files)`);
  }

  // Create empty runtime doc dirs
  const runtimeDirs = ['每日调研回写', '全项目总控'];
  if (mode === 'full') {
    runtimeDirs.push('架构决策记录', '业务流程全案', '部署运维手册', '测试验收报告', '发布闭环');
  }
  for (const d of runtimeDirs) {
    const p = join(target, 'docs', d);
    if (!existsSync(p)) {
      mkdirSync(p, { recursive: true });
      console.log(`  [OK]   Created docs/${d}/`);
    }
  }

  console.log(`\n  Done. AI will read rules/AGENTS.md on next session.\n`);
}

// ── validate ──────────────────────────────────────────
function cmdValidate(targetPath) {
  const target = resolve(targetPath || '.');
  console.log(`\n  Validating: ${target}\n`);

  const checks = [
    { file: join(target, 'rules', 'AGENTS.md'), label: 'rules/AGENTS.md' },
    { file: join(target, 'docs', '_templates', '每日调研回写', 'DAILY_WRITEBACK_TEMPLATE.md'), label: 'Doc templates' },
    { dir: join(target, 'docs', '每日调研回写'), label: 'docs/每日调研回写/' },
    { dir: join(target, 'docs', '全项目总控'), label: 'docs/全项目总控/' },
  ];

  let ok = 0, fail = 0, warn = 0;

  for (const check of checks) {
    if (check.file) {
      if (existsSync(check.file)) {
        console.log(`  [OK]   ${check.label}`);
        ok++;
      } else {
        console.log(`  [MISS] ${check.label} — not found`);
        fail++;
      }
    }
    if (check.dir) {
      if (existsSync(check.dir)) {
        const files = readdirSync(check.dir).filter(f => f.endsWith('.md'));
        if (files.length > 0) {
          console.log(`  [OK]   ${check.label} (${files.length} records)`);
          ok++;
        } else {
          console.log(`  [WARN] ${check.label} — empty, create your first record`);
          warn++;
        }
      } else {
        console.log(`  [MISS] ${check.dir} — not found`);
        fail++;
      }
    }
  }

  // Check for skills
  const skillsDir = join(target, 'skills');
  if (existsSync(skillsDir)) {
    const n = countFiles(skillsDir);
    console.log(`  [OK]   skills/ (${n} files)`);
    ok++;
  } else {
    console.log(`  [INFO] No skills/ — lite mode or not yet added`);
  }

  console.log(`\n  ${ok} ok, ${warn} warnings, ${fail} missing\n`);
  process.exit(fail > 0 ? 1 : 0);
}

// ── sync ──────────────────────────────────────────────
function cmdSync(targetPath) {
  const target = resolve(targetPath || '.');
  console.log(`\n  Sync is not yet implemented.`);
  console.log(`  To update your skills, re-run: npx enterprise-ai-methodology init .\n`);
}

// ── main ──────────────────────────────────────────────
const args = process.argv.slice(2);
if (args.length === 0 || args[0] === '--help' || args[0] === '-h') usage();

const cmd = args[0];
const rest = args.slice(1);
const modeFlag = rest.includes('--lite') ? 'lite' : 'full';
const pathArg = rest.filter(a => !a.startsWith('--'))[0] || '.';

switch (cmd) {
  case 'init':
    cmdInit(pathArg, modeFlag);
    break;
  case 'validate':
    cmdValidate(pathArg);
    break;
  case 'sync':
    cmdSync(pathArg);
    break;
  default:
    console.error(`  Unknown command: ${cmd}`);
    usage();
}
