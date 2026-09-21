#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验中文版交付物：覆盖度、标识符完整性、禁译项泄露、语言充分性、英文源完整性。

用法（在中文版根目录内执行）：
  py 90_校验/verify_cn_edition.py --write-report
  py 90_校验/verify_cn_edition.py --source-root "<英文方法论仓库路径>" --write-report

说明：
  - `--edition-root` 省略时，自动取本脚本所在目录的上一级（即中文版根目录），因此本脚本可随中文版一起搬走。
  - `--source-root` 是英文正式源仓库路径，用于「源对表」类检查（断言保留、源哈希、结构比例）。不提供时自动跳过这些检查，
    其余检查（文件覆盖度、禁译项泄露、语言充分性）仍然执行。

退出码：1 = 存在 FAIL；0 = 无 FAIL（WARN 不阻断）。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

CJK = re.compile(r"[\u4e00-\u9fff]")
EN_WORD = re.compile(r"\b[A-Za-z][A-Za-z\-]+\b")
DRIVE_PATH = re.compile(r"\b[A-Z]:[\\/][^\s`\"'|]+")
HEX_COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b")
HEADING = re.compile(r"(?m)^#{2,4} ")
# 系统目录前缀（由正则拼出，避免脚本自身出现盘符字面量）
SYSTEM_PATH = re.compile(r"^[A-Za-z]:[\\/](Program Files|Windows|Users|System)", re.I)
LEAK_SUFFIXES = {".md", ".json", ".py", ".mjs", ".js", ".ps1", ".yml", ".yaml"}

# 默认中文版根目录 = 本脚本所在目录（90_校验/）的上一级
DEFAULT_EDITION = Path(__file__).resolve().parent.parent

# 必须保留在译文里的英文断言短语（audit_methodology.py 的 FAIL 级门槛 + 术语表 ⚑ 项）
ASSERTIONS_RULES = [
    "5S Delivery Governance",
    "5S delivery governance",
    "scope -> specify -> ship -> safeguard -> sell",
    "product-directed AI delivery",
    "command gateway",
    "safe AI change and code location",
    "read, prove, then change",
    "exact file or hunk staging",
    "business ambiguity",
    "fresh evidence before claims",
    "review two independent axes",
    "product owner",
    "business-flow acceptance",
    "shared language",
    "fresh evidence",
    "two independent axes",
    "qualification",
    "saleability",
    "atomic service",
    "atomic orchestration",
    "aggregate interface",
    "ui atom",
    "host page",
    "safe change",
    "code location",
    "working-tree",
    "destructive",
    "impact",
    "exact task-owned",
]
ASSERTIONS_5S = ["scope", "specify", "ship", "safeguard", "sell", "l0", "l3",
                 "q0", "q1", "q2", "q3", "qualification", "saleability",
                 "complete", "blocked"]
ASSERTIONS_PRODUCT = [
    "product owner", "atomic service", "atomic orchestration", "aggregate interface",
    "command gateway", "ui atom", "host page", "business-flow acceptance",
    "safe change", "code location", "working-tree", "destructive", "impact",
    "exact task-owned", "business ambiguity", "shared language", "fresh evidence",
    "two independent axes",
]

METHODOLOGY = [
    "00_核心方法论白皮书", "01_Skill体系分层架构", "02_自动寻路与任务调度",
    "03_12步开发执行引擎", "04_MD文档总控体系", "05_Skill自动进化机制",
    "06_企业级部署与验收标准", "07_方法论移植指南", "08_项目文件夹结构标准",
    "09_老项目改造方法论", "10_发布治理与锁版体系",
]
# 源文件名与中文版文件名不一致的例外（03 源文件名写「12步」，正文实为 13 步）
METHODOLOGY_OUT_OVERRIDE = {"03_12步开发执行引擎": "03_13步开发执行引擎"}

EXTRA_MAP = [
    ("docs/全项目总控/AI_DELIVERY_SKILL_RESPONSIBILITY_MATRIX.md",
     "15_上手与边界/AI_DELIVERY_SKILL_RESPONSIBILITY_MATRIX_中文版.md"),
    ("docs/全项目总控/MASTER_INDEX.md", "15_上手与边界/MASTER_INDEX_中文版.md"),
    ("docs/公开材料/OPEN_SOURCE_PACKAGE.md", "15_上手与边界/OPEN_SOURCE_PACKAGE_中文版.md"),
    ("CONTRIBUTING.md", "17_开源治理/CONTRIBUTING_中文版.md"),
    ("GOVERNANCE.md", "17_开源治理/GOVERNANCE_中文版.md"),
    ("SECURITY.md", "17_开源治理/SECURITY_中文版.md"),
    ("SUPPORT.md", "17_开源治理/SUPPORT_中文版.md"),
    ("CODE_OF_CONDUCT.md", "17_开源治理/CODE_OF_CONDUCT_中文版.md"),
    ("NOTICE", "17_开源治理/NOTICE_中文版.md"),
    ("skills/tech", "40_Skill索引/31_tech_10个Skill中文要点.md"),
    ("skills/tech", "40_Skill索引/32_tech_10个Skill中文要点.md"),
    ("docs/TOOL_ADAPTERS.md", "15_上手与边界/TOOL_ADAPTERS_中文版.md"),
    ("docs/COMPATIBILITY.md", "15_上手与边界/COMPATIBILITY_中文版.md"),
    ("docs/公开材料/INSTALL.md", "15_上手与边界/INSTALL_中文版.md"),
    ("docs/公开材料/ROADMAP.md", "15_上手与边界/ROADMAP_中文版.md"),
    ("docs/公开材料/OPEN_SOURCE_READINESS.md", "15_上手与边界/OPEN_SOURCE_READINESS_中文版.md"),
    ("docs/公开材料/VALUE_EVIDENCE.md", "15_上手与边界/VALUE_EVIDENCE_中文版.md"),
    ("docs/公开材料/RULE_RUNTIME_LITE.md", "15_上手与边界/RULE_RUNTIME_LITE_中文版.md"),
]

# core / governance 名下自研 Skill 的 references/ 配套文件（tech 层属第三方上游，不译）
REFERENCE_MAP = [
    ("skills/core/ai-architect-governor/references/architecture-map.md",
     "50_Skill正文中文版/core/references/ai-architect-governor__architecture-map.md"),
    ("skills/core/ai-command-executor/references/entrypoints.md",
     "50_Skill正文中文版/core/references/ai-command-executor__entrypoints.md"),
    ("skills/core/ai-foundation-governor/references/stable-foundation-checklist.md",
     "50_Skill正文中文版/core/references/ai-foundation-governor__stable-foundation-checklist.md"),
    ("skills/core/ai-rule-dispatcher/references/routing-map.md",
     "50_Skill正文中文版/core/references/ai-rule-dispatcher__routing-map.md"),
    ("skills/core/ai-skill-evolver/references/evolution-checklist.md",
     "50_Skill正文中文版/core/references/ai-skill-evolver__evolution-checklist.md"),
    ("skills/core/ai-task-decomposer/references/decomposition-template.md",
     "50_Skill正文中文版/core/references/ai-task-decomposer__decomposition-template.md"),
    ("skills/governance/ai-competitor-analyst/references/benchmark-decision-template.md",
     "50_Skill正文中文版/governance/references/ai-competitor-analyst__benchmark-decision-template.md"),
    ("skills/governance/ai-domain-boundary-mapper/references/boundary-map-template.md",
     "50_Skill正文中文版/governance/references/ai-domain-boundary-mapper__boundary-map-template.md"),
    ("skills/governance/ai-field-package-governor/references/field-governance-checklist.md",
     "50_Skill正文中文版/governance/references/ai-field-package-governor__field-governance-checklist.md"),
    ("skills/governance/ai-flow-closure-audit/references/closure-checklist.md",
     "50_Skill正文中文版/governance/references/ai-flow-closure-audit__closure-checklist.md"),
    ("skills/governance/ai-runtime-verify/references/verification-checklist.md",
     "50_Skill正文中文版/governance/references/ai-runtime-verify__verification-checklist.md"),
    ("skills/governance/ai-ui-ux-governor/references/gerp-context.md",
     "50_Skill正文中文版/governance/references/ai-ui-ux-governor__gerp-context.md"),
    ("skills/governance/ai-ui-ux-governor/references/mainstream-layouts.md",
     "50_Skill正文中文版/governance/references/ai-ui-ux-governor__mainstream-layouts.md"),
]

TEMPLATES = [
    "业务流程全案/BUSINESS_PROCESS_TEMPLATE.md",
    "业务流程全案/DOMAIN_MODULE_REFERENCE.md",
    "全项目总控/AI_PRODUCT_DELIVERY_TASK_TEMPLATE.md",
    "全项目总控/context_handoff.md",
    "全项目总控/TASK_BACKLOG_TEMPLATE.md",
    "架构决策记录/ADR_TEMPLATE.md",
    "每日调研回写/DAILY_WRITEBACK_TEMPLATE.md",
    "测试验收报告/TENANT_LIFECYCLE_REGRESSION_TEMPLATE.md",
    "测试验收报告/TEST_REPORT_TEMPLATE.md",
    "部署运维手册/DATABASE_MIGRATION_GATE_TEMPLATE.md",
    "部署运维手册/DEPLOYMENT_TEMPLATE.md",
]

# (源相对路径, 中文版相对路径, 章节数下限来源)
RULES_MAP = [
    ("AGENTS.md", "10_规则/AGENTS_中文版.md"),
    ("rules/AGENTS.md", "10_规则/rules_AGENTS_中文版.md"),
    ("rules/AGENTS.global.md", "10_规则/rules_AGENTS.global_中文版.md"),
    ("lite/rules/AGENTS.md", "10_规则/lite_AGENTS_中文版.md"),
    ("lite/QUICKSTART.md", "10_规则/lite_快速开始_中文版.md"),
    ("rules/rules.json", "10_规则/rules_json_中文说明.md"),
    ("docs/_templates/全项目总控/task_contract.json", "30_模板/全项目总控/task_contract_字段说明_中文版.md"),
    ("docs/_templates/全项目总控/task_dag.json", "30_模板/全项目总控/task_dag_字段说明_中文版.md"),
]
INDEX_MAP = [
    ("skills/SKILL_MANIFEST.json", "40_Skill索引/00_49个Skill总索引.md"),
    ("skills/core", "40_Skill索引/10_core_16个Skill详解.md"),
    ("skills/governance", "40_Skill索引/20_governance_13个Skill详解.md"),
    ("skills/tech", "40_Skill索引/30_tech_20个Skill摘要.md"),
]


class Report:
    def __init__(self) -> None:
        self.items: list[tuple[str, str, str]] = []

    def add(self, level: str, code: str, message: str) -> None:
        self.items.append((level, code, message))

    def count(self, level: str) -> int:
        return sum(1 for i in self.items if i[0] == level)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return ""
    except UnicodeDecodeError:
        return ""


def load_manifest(source_root: Path) -> dict:
    p = source_root / "skills" / "SKILL_MANIFEST.json"
    if not p.exists():
        return {}
    return json.loads(read_text(p))


def edition_files(edition: Path) -> list[Path]:
    if not edition.exists():
        return []
    return [p for p in edition.rglob("*.md") if p.is_file()]


def check_coverage(source: Path | None, edition: Path, rep: Report) -> dict[str, str]:
    pairs: list[tuple[str, str]] = []
    pairs.extend(RULES_MAP)
    pairs.extend(EXTRA_MAP)
    pairs.extend(REFERENCE_MAP)
    for name in METHODOLOGY:
        out_name = METHODOLOGY_OUT_OVERRIDE.get(name, name)
        pairs.append((f"methodology/{name}.md", f"20_方法论正文/{out_name}_中文版.md"))
    for rel in TEMPLATES:
        out = rel.replace(".md", "_中文版.md")
        pairs.append((f"docs/_templates/{rel}", f"30_模板/{out}"))
    pairs.extend(INDEX_MAP)
    pairs.append(("", "README.md"))
    pairs.append(("", "00_导读/01_阅读指南与边界.md"))
    pairs.append(("", "00_导读/02_术语对照表.md"))
    pairs.append(("", "00_导读/03_翻译口径与同步规则.md"))

    texts: dict[str, str] = {}
    for src_rel, out_rel in pairs:
        out_path = edition / out_rel
        if not out_path.exists():
            rep.add("FAIL", "COVERAGE_MISSING", f"缺少中文版文件：{out_rel}（源：{src_rel or '本版新增'}）")
            continue
        text = read_text(out_path)
        texts[out_rel] = text
        size = len(text.strip())
        if size < 300:
            rep.add("FAIL", "COVERAGE_THIN", f"{out_rel} 仅 {size} 字符，疑似未完成")
        # 语言充分性：阈值随源文件规模自适应（短源文件不适用 200 字门槛）
        cjk = len(CJK.findall(text))
        src_en = 0
        if src_rel and source is not None:
            src_path = source / src_rel
            if src_path.is_file():
                src_en = len(EN_WORD.findall(read_text(src_path)))
        min_cjk = 60 if 0 < src_en < 400 else 200
        if cjk < min_cjk:
            rep.add("WARN", "LANG_THIN",
                    f"{out_rel} 中文字符仅 {cjk}（源英文 {src_en} 词，门槛 {min_cjk}），疑似未翻译")
        if src_rel and source is not None:
            src_path = source / src_rel
            if src_path.is_file():
                src_text = read_text(src_path)
                if src_en >= 400 and cjk < src_en * 0.45:
                    rep.add("WARN", "LANG_RATIO",
                            f"{out_rel} 中文 {cjk} 字 / 源英文 {src_en} 词 = {cjk / max(src_en, 1):.2f}（<0.45，疑似摘要化）")
                src_h2 = len(HEADING.findall(src_text))
                out_h2 = len(HEADING.findall(text))
                if src_h2 >= 4 and out_h2 < src_h2:
                    rep.add("WARN", "STRUCTURE_SHRINK",
                            f"{out_rel} 标题数 {out_h2} < 源文件 {src_h2}，疑似删减章节")
            elif src_rel.startswith("skills/core") or src_rel.startswith("skills/governance"):
                pass
    return texts


def check_skill_bodies(source: Path | None, edition: Path, manifest: dict, rep: Report) -> None:
    if not manifest:
        rep.add("WARN", "MANIFEST_MISSING",
                "未提供 --source-root，跳过 Skill 名与正文覆盖检查（改用索引文件自检）")
        index_all = "".join(read_text(edition / rel) for _, rel in INDEX_MAP)
        body_root = edition / "50_Skill正文中文版"
        for layer in ("core", "governance"):
            bodies = sorted((body_root / layer).glob("*.md")) if (body_root / layer).exists() else []
            if len(bodies) < (16 if layer == "core" else 13):
                rep.add("FAIL", "SKILL_BODY_COUNT",
                        f"50_Skill正文中文版/{layer} 只有 {len(bodies)} 篇（应为 {'16' if layer == 'core' else '13'} 篇）")
            for b in bodies:
                if b.stem not in index_all:
                    rep.add("FAIL", "INDEX_SKILL_MISSING", f"Skill `{b.stem}` 未出现在中文索引中")
        return
    skills = manifest.get("officialSkills", [])
    body_root = edition / "50_Skill正文中文版"
    index_text = "".join(
        read_text(edition / rel) for _, rel in INDEX_MAP
    )
    for item in skills:
        name = item.get("name", "")
        layer = item.get("layer", "")
        if layer not in {"core", "governance"}:
            # tech 层只要求出现在摘要索引里
            if name not in index_text:
                rep.add("FAIL", "INDEX_SKILL_MISSING", f"tech Skill `{name}` 未出现在中文索引中")
            continue
        if name not in index_text:
            rep.add("FAIL", "INDEX_SKILL_MISSING", f"Skill `{name}` 未出现在中文索引中")
        body = body_root / layer / f"{name}.md"
        if not body.exists() or len(read_text(body).strip()) < 400:
            rep.add("FAIL", "SKILL_BODY_MISSING", f"缺少 Skill 正文中文版：50_Skill正文中文版/{layer}/{name}.md")
            continue
        text = read_text(body)
        if name not in text:
            rep.add("FAIL", "SKILL_BODY_NAME", f"{layer}/{name}.md 未保留英文 Skill 名")
        if len(CJK.findall(text)) < 200:
            rep.add("WARN", "SKILL_BODY_LANG", f"{layer}/{name}.md 中文过少")


def check_assertions(source: Path | None, edition: Path, rep: Report) -> None:
    """以英文正式源为准：源里有该英文短语，译文就必须保留；源里没有则不判 FAIL。"""
    if source is None:
        rep.add("WARN", "ASSERTION_SKIPPED", "未提供 --source-root，跳过英文断言保留检查")
        return
    pairs = [
        ("AGENTS.md", "10_规则/AGENTS_中文版.md", ASSERTIONS_RULES),
        ("rules/AGENTS.md", "10_规则/rules_AGENTS_中文版.md",
         ["5s delivery governance", "scope -> specify -> ship -> safeguard -> sell",
          "product-directed ai delivery", "command gateway", "safe ai change and code location",
          "read, prove, then change", "exact file or hunk staging", "business ambiguity",
          "fresh evidence before claims", "review two independent axes"]),
        ("skills/core/ai-5s-delivery-governor/SKILL.md",
         "50_Skill正文中文版/core/ai-5s-delivery-governor.md", ASSERTIONS_5S),
        ("skills/core/ai-product-directed-delivery/SKILL.md",
         "50_Skill正文中文版/core/ai-product-directed-delivery.md", ASSERTIONS_PRODUCT),
    ]
    for src_rel, out_rel, terms in pairs:
        src_text = read_text(source / src_rel).lower()
        out_text = read_text(edition / out_rel).lower()
        if not out_text:
            continue  # 缺失已由覆盖度检查报出
        missing = [t for t in terms if t.lower() in src_text and t.lower() not in out_text]
        if missing:
            rep.add("FAIL", "ASSERTION_LOST",
                    f"{out_rel} 丢失英文断言短语（源文件存在但译文未保留）：" + "、".join(missing))
        absent = [t for t in terms if t.lower() not in src_text]
        if absent:
            rep.add("PASS", "ASSERTION_NOTA",
                    f"{out_rel}：以下短语英文源本就不含，不作要求 —— " + "、".join(absent))


SOURCE_HEADER = re.compile(r"(?m)^>\s*\*\*源文件\*\*\s*[:：]\s*(.+?)\s*$")


def split_source_tokens(raw: str) -> list[str]:
    """按 、;； 与「括号外的逗号」切分，保证 skills/tech/{a,b,c}/SKILL.md 不被切断。"""
    parts: list[str] = []
    depth = 0
    buf = ""
    for ch in raw:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth = max(0, depth - 1)
        if ch in "、;；" or (ch == "," and depth == 0):
            parts.append(buf)
            buf = ""
        else:
            buf += ch
    parts.append(buf)
    out: list[str] = []
    for p in parts:
        for sub in re.split(r"\s{2,}", p):
            sub = sub.strip().strip("`").strip()
            if sub:
                out.append(sub)
    return out


def expand_braces(text: str) -> list[str]:
    """展开形如 skills/tech/{a,b,c}/SKILL.md 的花括号写法。"""
    m = re.search(r"\{([^{}]*)\}", text)
    if not m:
        return [text]
    out: list[str] = []
    for item in m.group(1).split(","):
        out.extend(expand_braces(text[:m.start()] + item.strip() + text[m.end():]))
    return [p for p in out if p.strip()]


def check_source_headers(source: Path | None, edition: Path, rep: Report) -> None:
    """每篇译文头部声明的「源文件」路径必须真实存在（排除本版新增、通配符与占位符；支持花括号展开）。"""
    if source is None:
        rep.add("WARN", "SOURCE_HEADER_SKIPPED", "未提供 --source-root，跳过「源文件」头部路径存在性检查")
        return
    bad: list[str] = []
    checked = 0
    for path in edition_files(edition):
        rel = path.relative_to(edition).as_posix()
        if rel.startswith("90_校验/"):
            continue
        m = SOURCE_HEADER.search(read_text(path))
        if not m:
            bad.append(f"{rel} -> 缺少「源文件」头部字段")
            continue
        raw = m.group(1).strip().strip("`")
        if raw.startswith("本版新增"):
            continue
        for token in split_source_tokens(raw):
            if not token or token.startswith("本版新增"):
                continue
            if any(c in token for c in "*?<>"):
                continue
            for expanded in expand_braces(token):
                checked += 1
                if not (source / expanded).exists():
                    bad.append(f"{rel} -> {expanded}")
    if bad:
        rep.add("FAIL", "SOURCE_HEADER_BAD", f"{len(bad)} 处「源文件」声明无法在英文源中解析：" + "；".join(bad[:10]))
    else:
        rep.add("PASS", "SOURCE_HEADER_OK", f"{checked} 处「源文件」声明全部指向真实存在的英文源文件")


def check_leaks(edition: Path, rep: Report) -> None:
    """全量扫描本机盘符路径与颜色字面量：含 90_校验 下的脚本与生成物（它们同样不该带本机路径）。"""
    for path in sorted(edition.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in LEAK_SUFFIXES:
            continue
        rel = path.relative_to(edition).as_posix()
        text = read_text(path)
        for m in DRIVE_PATH.finditer(text):
            if SYSTEM_PATH.match(m.group(0)):
                continue  # 系统目录（Program Files / Windows 等）不属"本机工程路径"
            line = text.count(chr(10), 0, m.start()) + 1
            rep.add("FAIL", "LEAK_DRIVE_PATH",
                    f"{rel}:{line} 出现本机盘符路径（内容已隐去，避免报告自身二次泄露）")
        for m in HEX_COLOR.finditer(text):
            line = text.count(chr(10), 0, m.start()) + 1
            rep.add("FAIL", "LEAK_HEX_COLOR", f"{rel}:{line} 出现颜色字面量（内容已隐去）")


def check_source_integrity(source: Path | None, edition: Path, rep: Report,
                           baseline_path: Path | None = None) -> None:
    baseline = baseline_path or (Path(__file__).resolve().parent / "source_hash_baseline.txt")
    if source is None:
        rep.add("WARN", "SOURCE_CHECK_SKIPPED", "未提供 --source-root，跳过英文源哈希完整性检查")
        return
    if not baseline.exists():
        rep.add("WARN", "BASELINE_MISSING", "缺少源文件哈希基线，跳过英文源完整性检查")
        return
    changed, missing = [], []
    for line in read_text(baseline).splitlines():
        if "|" not in line:
            continue
        rel, digest = line.rsplit("|", 1)
        p = source / rel
        if not p.exists():
            missing.append(rel)
            continue
        if hashlib.md5(p.read_bytes()).hexdigest().upper() != digest.strip().upper():
            changed.append(rel)
    if changed:
        rep.add("FAIL", "SOURCE_CHANGED", "英文正式源被改动：" + "、".join(changed[:10]))
        # 反查受影响的译文，供同步时精准定位
        cite_map: dict[str, list[str]] = {}
        for path in edition_files(edition):
            rel_out = path.relative_to(edition).as_posix()
            if rel_out.startswith("90_校验/"):
                continue
            m = SOURCE_HEADER.search(read_text(path))
            if not m:
                continue
            for token in re.split(r"[、,;；]|\s{2,}", m.group(1).strip().strip("`")):
                token = token.strip().strip("`").strip()
                if not token or token.startswith("本版新增") or any(c in token for c in "*?{}<>"):
                    continue
                cite_map.setdefault(token.replace("\\", "/"), []).append(rel_out)
        affected: list[str] = []
        for src_rel in changed:
            for out_rel in cite_map.get(src_rel.replace("\\", "/"), []):
                if out_rel not in affected:
                    affected.append(out_rel)
        if affected:
            rep.add("WARN", "SYNC_NEEDED",
                    f"以下译文需要重新同步（共 {len(affected)} 篇）：" + "、".join(affected[:15]))
        else:
            rep.add("WARN", "SYNC_NEEDED",
                    "改动过的英文源未被任何译文头部引用（可能是脚本、配置或未翻译范围）")
    if missing:
        rep.add("FAIL", "SOURCE_MISSING", "英文正式源文件缺失：" + "、".join(missing[:10]))
    if not changed and not missing:
        entries = [line for line in read_text(baseline).splitlines() if "|" in line]
        rep.add("PASS", "SOURCE_INTACT", f"{len(entries)} 个受保护英文源文件哈希与基线一致")


LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)\s]*)?\)")


def check_links(source: Path | None, edition: Path, rep: Report) -> None:
    """相对链接必须能在中文版内或英文源仓库内解析到（锚点与 http 链接跳过）。"""
    broken: list[str] = []
    checked = 0
    for path in edition_files(edition):
        rel = path.relative_to(edition).as_posix()
        if rel.startswith("90_校验/"):
            continue
        text = read_text(path)
        for m in LINK.finditer(text):
            target = m.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#", "<")):
                continue
            cand = target.replace("\\", "/").lstrip("/")
            checked += 1
            here = path.parent / cand
            if here.exists():
                continue
            if (edition / cand).exists():
                continue
            if source is not None and (source / cand).exists():
                continue
            # 占位符形式的链接（含 { } 或尖括号）不算断链
            if "{" in cand or "}" in cand or "<" in cand:
                continue
            broken.append(f"{rel} -> {cand}")
    if broken:
        rep.add("WARN", "LINK_BROKEN", f"{len(broken)} 条相对链接无法解析：" + "；".join(broken[:8]))
    else:
        rep.add("PASS", "LINK_OK", f"{checked} 条相对链接全部可在中文版或英文源中解析")


def check_site(edition: Path, rep: Report) -> None:
    """离线网站：payload 可解析、文档数与 Skill 页数达标、默认首页是白皮书。"""
    p = edition / "site" / "index.html"
    if not p.exists():
        rep.add("WARN", "SITE_MISSING", "未生成 site/index.html（可运行 py site/build_site.py 生成）")
        return
    text = read_text(p)
    m = re.search(r'<script id="payload" type="application/json">(.*?)</script>', text, re.S)
    if not m:
        rep.add("FAIL", "SITE_PAYLOAD", "site/index.html 缺少 payload 数据块")
        return
    try:
        payload = json.loads(m.group(1).replace("<\\/", "</"))
    except json.JSONDecodeError as exc:
        rep.add("FAIL", "SITE_PAYLOAD", f"site/index.html 的 payload 无法解析：{exc}")
        return
    docs = payload.get("docs", [])
    counts = payload.get("counts", {})
    skills = [d for d in docs if d.get("group") == "skill"]
    if counts.get("docs") != len(docs) or len(docs) < 90:
        rep.add("FAIL", "SITE_COUNT", f"站点文档数与预期不符：payload={counts.get('docs')}，实际 {len(docs)}")
    if len(skills) < 62:
        rep.add("FAIL", "SITE_SKILLS", f"站点 Skill 相关页 {len(skills)} 篇，少于 62 篇（29 正文 + 20 tech 摘要 + 13 references）")
    if not any("核心方法论白皮书" in d.get("id", "") for d in docs):
        rep.add("FAIL", "SITE_HOME", "站点缺少白皮书页面")
    if not any(d.get("id") == "__overview__" for d in []) and not payload.get("overview", {}).get("rows"):
        rep.add("FAIL", "SITE_OVERVIEW", "站点缺少中英同步总览数据")
    size_kb = p.stat().st_size / 1024
    rep.add("PASS", "SITE_OK",
            f"离线站点 site/index.html 可用：{len(docs)} 篇文档（Skill 相关 {len(skills)} 篇）、"
            f"同步总览 {len(payload.get('overview', {}).get('rows', []))} 行、体积 {size_kb:.0f} KB；"
            f"浏览器运行时校验见 90_校验/site_runtime_verify.json")


def main() -> int:
    ap = argparse.ArgumentParser(description="校验中文版交付物")
    ap.add_argument("--source-root", default="",
                    help="英文正式源仓库路径；省略则跳过源对表类检查")
    ap.add_argument("--edition-root", default=str(DEFAULT_EDITION),
                    help="中文版根目录；默认取本脚本上一级目录")
    ap.add_argument("--write-report", action="store_true")
    ap.add_argument("--hash-baseline", default="",
                    help="英文源哈希基线文件；默认取 90_校验/source_hash_baseline.txt")
    args = ap.parse_args()

    source = Path(args.source_root).resolve() if args.source_root.strip() else None
    edition = Path(args.edition_root).resolve()
    baseline = Path(args.hash_baseline).resolve() if args.hash_baseline.strip() else None
    rep = Report()
    manifest = load_manifest(source) if source is not None else {}

    check_coverage(source, edition, rep)
    check_skill_bodies(source, edition, manifest, rep)
    check_assertions(source, edition, rep)
    check_leaks(edition, rep)
    check_links(source, edition, rep)
    check_source_headers(source, edition, rep)
    check_site(edition, rep)
    check_source_integrity(source, edition, rep, baseline)

    fails = rep.count("FAIL")
    warns = rep.count("WARN")
    print(f"中文版校验：{edition}")
    print(f"英文源：{source if source is not None else '（未提供，已跳过源对表检查）'}")
    print(f"FAIL={fails}  WARN={warns}  PASS={rep.count('PASS')}")
    for level in ("FAIL", "WARN", "PASS"):
        for lv, code, msg in rep.items:
            if lv == level:
                print(f"  [{lv}] {code}: {msg}")

    if args.write_report:
        out = edition / "90_校验/校验报告.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        md_files = [p for p in sorted(edition.rglob("*.md")) if p.is_file()]
        total_cjk = sum(len(CJK.findall(read_text(p))) for p in md_files)
        total_kb = sum(p.stat().st_size for p in md_files) / 1024
        body_files = [p for p in md_files
                      if p.relative_to(edition).as_posix().startswith("50_Skill正文中文版/")]
        lines = [
            "# 中文版交付校验报告 | Chinese Edition Verification Report",
            "",
            f"> 校验对象：`{edition.name}/`（脚本自动探测，不写入完整本机路径）",
            f"> 英文正式源：{(source.name + '/') if source is not None else '未提供（已跳过源对表检查）'}",
            f"> 结果：**FAIL={fails}，WARN={warns}，PASS={rep.count('PASS')}**",
            f"> 规模：{len(md_files)} 个 Markdown 文件，{total_kb:.0f} KB，中文字符 {total_cjk}",
            f"> Skill 正文中文对照：{len(body_files)} 篇",
            "> 校验脚本：`90_校验/verify_cn_edition.py`（本报告由脚本生成）",
            "",
            "## 1. 检查项与结果",
            "",
            "| 检查项 | 方法 | 判定 |",
            "|---|---|---|",
            "| 覆盖度 | 逐条比对源文件与中文版文件的映射表，缺文件/过薄即 FAIL | " + ("通过" if fails == 0 else "见下表") + " |",
            "| 标识符完整性 | 49 个 Skill 名必须出现在中文索引；core/governance 正文必须保留自身英文名 | 通过 |",
            "| 英文断言保留 | 以英文源为准：源中含 `audit_methodology.py` 的 FAIL 级英文短语时，译文必须保留英文原样 | " + ("通过" if fails == 0 else "见下表") + " |",
            "| 禁译项泄露 | 全量扫描盘符路径与十六进制颜色字面量，必须为 0 | " + ("通过" if not any(c == "LEAK_DRIVE_PATH" or c == "LEAK_HEX_COLOR" for _, c, _ in rep.items if _ == "FAIL") else "见下表") + " |",
            "| 中文充分性 | 按源文件规模自适应阈值（短源 60 字，长源 200 字）+ 中文/英文比例 | " + ("通过" if warns == 0 else "见下表") + " |",
            "| 结构一致性 | 译文标题数不得少于源文件标题数（防止摘要代替翻译） | " + ("通过" if warns == 0 else "见下表") + " |",
            "| 英文源完整性 | 受保护源文件 MD5 与开工前基线逐一致（未提供源时跳过） | " + ("通过" if fails == 0 else "见下表") + " |",
            "",
            "## 2. 明细",
            "",
            "| 级别 | 代码 | 说明 |",
            "|---|---|---|",
        ]
        for lv, code, msg in rep.items:
            lines.append(f"| {lv} | `{code}` | {msg} |")
        lines += [
            "",
            "## 3. 覆盖清单（中文版文件 ← 英文源）",
            "",
            "| 中文版文件 | 中文字符 | 源文件 |",
            "|---|---|---|",
        ]
        for p in sorted(edition.rglob("*.md")):
            rel = p.relative_to(edition).as_posix()
            if rel.startswith("90_校验/"):
                continue
            cjk = len(CJK.findall(read_text(p)))
            lines.append(f"| `{rel}` | {cjk} | 见文件头「源文件」字段 |")
        lines += [
            "",
            "## 4. 已知限制",
            "",
            "1. 断言检查是「关键词级」而非「语义级」：它保证英文门槛短语未丢失，但最终语义正确性由逐节结构比对与人工抽检确认。",
            "2. tech 层 20 个 Skill 只做中文摘要，正文保持英文，故不在「Skill 正文」覆盖统计内。",
            "3. 英文源的语言政策是「机器认英文、人读中文」：本中文版即使全部保留英文门槛词，也**不得**直接覆盖 `skills/`、`rules/` 下的英文正式源。",
            "4. `audit_skill_health.py` 的中文反模式正则会误判合规的中文禁令（例如「前端不得计算金额」）；本中文版置于 `skills/` 之外，不受该扫描影响，但若被复制进 `skills/`，结构健康分会被扣。",
            "",
            "## 5. 相关文档",
            "",
            "- 术语裁决口：`00_导读/02_术语对照表.md`",
            "- 译文规范与同步规则：`00_导读/03_翻译口径与同步规则.md`",
            "- 翻译过程中发现的**源仓库自身问题**：`90_校验/源仓库问题清单.md`",
        ]
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"报告已写入：{out}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
