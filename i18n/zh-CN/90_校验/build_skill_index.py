#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 40_Skill索引/00_49个Skill总索引.md。

数据来源：
  - `<英文源仓库>/skills/SKILL_MANIFEST.json`（name / layer / path / maturity / description）
  - 同目录的 10_core_16个Skill详解.md、20_governance_13个Skill详解.md、30_tech_20个Skill摘要.md
    （从中提取「## N. `skill-name` — 中文名」与紧随其后的小节内容，取中文名与一句话职责）

用法（在中文版根目录内执行）：
  py 90_校验/build_skill_index.py --source-root "<英文方法论仓库路径>"

`--edition-root` 省略时自动取本脚本的上一级目录，因此本脚本可随中文版一起搬走。
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

EDITION = Path(__file__).resolve().parent.parent
INDEX_DIR = EDITION / "40_Skill索引"

SECTION = re.compile(r"(?m)^##\s+\d+\.\s+`([a-z0-9\-]+)`\s+[—-]\s*(.+?)\s*$")
LAYER_CN = {"core": "core（核心引擎）", "governance": "governance（治理）", "tech": "tech（技术栈）"}

WHEN_HINTS = {
    "core": "任务路由/拆解/规划与进化时",
    "governance": "改动业务代码、页面、真相边界或需要验收证据时",
    "tech": "进入对应技术栈开发时",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def extract_sections(path: Path) -> dict[str, str]:
    """返回 {skill name: 中文名}"""
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for m in SECTION.finditer(path.read_text(encoding="utf-8-sig")):
        out[m.group(1)] = m.group(2).strip()
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="生成 49 个 Skill 总索引")
    ap.add_argument("--source-root", required=True,
                    help="英文方法论仓库路径（需含 skills/SKILL_MANIFEST.json）")
    ap.add_argument("--edition-root", default=str(EDITION),
                    help="中文版根目录；默认取本脚本上一级目录")
    args = ap.parse_args()

    source = Path(args.source_root)
    edition = Path(args.edition_root)
    index_dir = edition / "40_Skill索引"

    manifest = load_json(source / "skills" / "SKILL_MANIFEST.json")
    names: dict[str, str] = {}
    names.update(extract_sections(index_dir / "10_core_16个Skill详解.md"))
    names.update(extract_sections(index_dir / "20_governance_13个Skill详解.md"))
    names.update(extract_sections(index_dir / "30_tech_20个Skill摘要.md"))

    skills = manifest.get("officialSkills", [])
    lines = [
        "# 49 个正式 Skill 总索引 | Official Skill Index",
        "",
        "> **源文件**：skills/SKILL_MANIFEST.json",
        f"> **源版本**：updatedAt {manifest.get('updatedAt', '未标注')}；schemaVersion {manifest.get('schemaVersion', '未标注')}",
        "> **译文日期**：2026-09-14",
        "> **术语依据**：00_导读/02_术语对照表.md",
        "> **说明**：Skill 名（`ai-*` / 框架类名）是路由键与部署键，**保持英文，不得翻译**；中文名仅用于阅读。",
        "",
        f"正式 Skill 共 **{len(skills)}** 个：core {sum(1 for s in skills if s.get('layer') == 'core')} 个、"
        f"governance {sum(1 for s in skills if s.get('layer') == 'governance')} 个、"
        f"tech {sum(1 for s in skills if s.get('layer') == 'tech')} 个。",
        "",
        "本索引是导航入口；**core/governance 的中文详解**见 `10_core_16个Skill详解.md`、`20_governance_13个Skill详解.md`，"
        "**tech 中文摘要**见 `30_tech_20个Skill摘要.md`，**core/governance 正文中文对照**见 `50_Skill正文中文版/`。",
        "",
        "---",
        "",
    ]

    for layer in ("core", "governance", "tech"):
        group = [s for s in skills if s.get("layer") == layer]
        if not group:
            continue
        lines += [f"## {LAYER_CN.get(layer, layer)}（{len(group)} 个）", "",
                  "| Skill（英文，不可译） | 中文名 | 源路径 | 成熟度 | 何时加载 |",
                  "|---|---|---|---|---|"]
        for s in group:
            name = s.get("name", "")
            cn = names.get(name, "（尚未生成中文名，见对应详解文件）")
            when = WHEN_HINTS.get(layer, "")
            lines.append(f"| `{name}` | {cn} | `{s.get('path', '')}` | {s.get('maturity', '')} | {when} |")
        lines.append("")

    lines += [
        "---",
        "",
        "## 关键分组速查",
        "",
        "| 场景 | 应加载的 Skill（英文名） |",
        "|---|---|",
        "| 新项目/新任务开工 | `ai-project-classifier` → `ai-rule-dispatcher` → `ai-task-decomposer` |",
        "| 产品主导的全 AI 交付 | `ai-product-directed-delivery` |",
        "| 版本化交付 / 发布 / 热修复 | `ai-5s-delivery-governor`、`ai-delivery-contract-governor` |",
        "| 页面与前端 | `ai-single-truth-enforcer`、`ai-component-standardizer`、`ai-ui-ux-governor`、`ai-frontend-audit` |",
        "| 宣布「完成」之前 | `ai-runtime-verify`、`ai-flow-closure-audit` |",
        "| 老项目改造 | `ai-brownfield-analyzer` |",
        "| 架构与领域边界 | `ai-atomic-architect`、`ai-architect-governor`、`ai-atomic-governance`、`ai-domain-boundary-mapper` |",
        "| 字段与元数据 | `ai-field-package-governor` |",
        "| 工具缺失/环境异常 | `ai-tool-bootstrapper`、`ai-command-executor` |",
        "| 复盘与进化 | `ai-skill-evolver`、`ai-skill-governor` |",
        "",
        "## 未纳入正文翻译的 Skill（tech 层）",
        "",
        "tech 层 20 个 Skill 只提供中文摘要，正文保留英文。其中 8 个源自上游第三方"
        "（`vue`、`vue-best-practices`、`vue-pinia-best-practices`、`flutter-expert`、`flutter-animations`、"
        "`docker-expert`、`springboot-patterns`、`springboot-security`），翻译正文等于与上游分叉，"
        "并且会破坏署名与升级同步。详见 `30_tech_20个Skill摘要.md` 附录 B。",
    ]

    out = index_dir / "00_49个Skill总索引.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    missing = [s.get("name") for s in skills if s.get("name") not in names]
    print(f"已生成：{out}")
    print(f"Skill 总数：{len(skills)}；未提取到中文名：{missing or '无'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
