#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成中文版离线网站：site/index.html（自包含，双击即可用，无需服务器）。

特性：
  1. 自动加载全部内容：导读 / 规则 / 上手 / 方法论正文 / 模板 / Skill 索引 / 49 个 Skill 正文与配套 references / 校验结论。
  2. 49 个 Skill 由 skills/SKILL_MANIFEST.json 自动枚举（core 16 + governance 13 有正文，tech 20 用中文摘要），不漏不重。
  3. 中英对照：每篇都可切换「中文 / English / 并排对照」三种视图；英文侧直接取头部声明的源文件。
  4. 同步状态：用 90_校验/source_hash_baseline.txt 与源文件当前哈希比对，给出「已同步 / 源已变更 / 无需对照」，并统计中英章节数。
  5. 默认首页 = 核心方法论白皮书；另有「同步总览」页集中展示全量对照状态。

用法（在中文版根目录内执行）：
  py site/build_site.py --source-root "<英文方法论仓库路径>"

`--source-root` 省略时只生成中文侧（不加载英文对照）；`--out` 省略时输出到 `site/index.html`。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path

EDITION = Path(__file__).resolve().parent.parent
SOURCE_HEADER = re.compile(r"(?m)^>\s*\*\*源文件\*\*\s*[:：]\s*(.+?)\s*$")
VERSION_HEADER = re.compile(r"(?m)^>\s*\*\*源版本\*\*\s*[:：]\s*(.+?)\s*$")
HEADING = re.compile(r"(?m)^#{2,4} ")
TITLE = re.compile(r"(?m)^#\s+(.+?)\s*$")
TECH_SECTION = re.compile(r"(?m)^##\s+\d+\.\s+`([a-z0-9\-]+)`.*$")

GROUP_ORDER = [
    ("start", "起始与导读"),
    ("rules", "规则"),
    ("onboard", "上手与边界"),
    ("gov", "开源治理"),
    ("method", "方法论正文"),
    ("tpl", "文档模板"),
    ("idx", "Skill 索引"),
    ("skill", "Skill 正文（49 个）"),
    ("check", "校验与结论"),
]


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except (FileNotFoundError, UnicodeDecodeError):
        return ""


def title_of(text: str, fallback: str) -> str:
    m = TITLE.search(text)
    if not m:
        return fallback
    return m.group(1).replace("|", "丨").strip()


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


def source_tokens(text: str) -> list[str]:
    m = SOURCE_HEADER.search(text)
    if not m:
        return []
    raw = m.group(1).strip().strip("`")
    if raw.startswith("本版新增"):
        return []
    out: list[str] = []
    for token in split_source_tokens(raw):
        if not token or token.startswith("本版新增"):
            continue
        if any(c in token for c in "*?<>"):
            continue
        out.extend(expand_braces(token))
    # 去重并保序
    seen: set[str] = set()
    uniq: list[str] = []
    for p in out:
        p = p.replace("\\", "/")
        if p not in seen:
            seen.add(p)
            uniq.append(p)
    return uniq


def load_baseline() -> dict[str, str]:
    baseline: dict[str, str] = {}
    p = EDITION / "90_校验" / "source_hash_baseline.txt"
    if not p.exists():
        return baseline
    for line in read(p).splitlines():
        if "|" in line:
            rel, digest = line.rsplit("|", 1)
            baseline[rel.replace("\\", "/")] = digest.strip().upper()
    return baseline


def md5(path: Path) -> str:
    try:
        return hashlib.md5(path.read_bytes()).hexdigest().upper()
    except OSError:
        return ""


def sync_state(sources: list[str], source_root: Path | None, baseline: dict[str, str]) -> tuple[str, str]:
    """返回 (状态码, 状态中文)。"""
    if not sources:
        return ("new", "本版新增")
    if source_root is None:
        return ("unknown", "无法判定（未提供源目录）")
    changed = []
    for rel in sources:
        p = source_root / rel
        if not p.exists():
            changed.append("missing")
        elif rel in baseline and md5(p) != baseline[rel]:
            changed.append("changed")
    if "missing" in changed:
        return ("missing", "源文件缺失")
    if changed:
        return ("stale", "源已变更，待重同步")
    return ("ok", "已同步（源未变）")


def extract_tech_section(index_text: str, name: str) -> str:
    """从 40_Skill索引/30_tech_20个Skill摘要.md 中抽出某个 Skill 的小节。"""
    matches = list(TECH_SECTION.finditer(index_text))
    for i, m in enumerate(matches):
        if m.group(1) == name:
            start = m.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(index_text)
            body = index_text[start:end]
            # 去掉末尾的附录小标题（附录属于整份索引，不属于单个 Skill）
            body = re.split(r"(?m)^##\s+(附录|Appendix)", body)[0]
            return body.rstrip() + "\n"
    return ""


def build_docs(source_root: Path | None) -> list[dict]:
    baseline = load_baseline()
    docs: list[dict] = []

    def add(group: str, rel: str, title: str | None = None, zh: str | None = None,
            sources: list[str] | None = None, badge: str = "") -> None:
        path = EDITION / rel
        zh_text = zh if zh is not None else read(path)
        if not zh_text.strip():
            return
        srcs = sources if sources is not None else source_tokens(zh_text)
        en_parts = []
        if source_root is not None:
            for s in srcs:
                p = source_root / s
                if p.exists():
                    en_parts.append(f"> **英文源文件**：`{s}`\n\n" + read(p))
        en_text = "\n\n".join(en_parts)
        state, state_cn = sync_state(srcs, source_root, baseline)
        docs.append({
            "id": rel.replace("\\", "/"),
            "group": group,
            "title": title or title_of(zh_text, rel),
            "zh": zh_text,
            "en": en_text,
            "sources": srcs,
            "version": (VERSION_HEADER.search(zh_text).group(1) if VERSION_HEADER.search(zh_text) else ""),
            "sync": state,
            "syncText": state_cn,
            "zhHeadings": len(HEADING.findall(zh_text)),
            "enHeadings": len(HEADING.findall(en_text)),
            "badge": badge,
        })

    # 1. 起始与导读
    add("start", "README.md", "中文版总索引")
    for rel in ["00_导读/01_阅读指南与边界.md", "00_导读/02_术语对照表.md", "00_导读/03_翻译口径与同步规则.md"]:
        add("start", rel)

    # 2. 规则
    for p in sorted((EDITION / "10_规则").glob("*.md")):
        add("rules", p.relative_to(EDITION).as_posix())

    # 3. 上手与边界
    for p in sorted((EDITION / "15_上手与边界").glob("*.md")):
        add("onboard", p.relative_to(EDITION).as_posix())

    # 3b. 开源治理
    gov_dir = EDITION / "17_开源治理"
    if gov_dir.exists():
        for p in sorted(gov_dir.glob("*.md")):
            add("gov", p.relative_to(EDITION).as_posix())

    # 4. 方法论正文（白皮书排第一）
    for p in sorted((EDITION / "20_方法论正文").glob("*.md")):
        add("method", p.relative_to(EDITION).as_posix())

    # 5. 模板
    for p in sorted((EDITION / "30_模板").rglob("*.md")):
        add("tpl", p.relative_to(EDITION).as_posix())

    tech_index_rel = "40_Skill索引/30_tech_20个Skill摘要.md"
    tech_index_text = read(EDITION / tech_index_rel)
    # tech 层优先用「中文要点」（更详细），没有再退回「中文摘要」
    tech_essentials_text = "\n".join(
        read(EDITION / f"40_Skill索引/{n}")
        for n in ("31_tech_10个Skill中文要点.md", "32_tech_10个Skill中文要点.md")
    )

    # 6. Skill 索引
    for p in sorted((EDITION / "40_Skill索引").glob("*.md")):
        add("idx", p.relative_to(EDITION).as_posix())

    # 7. 49 个 Skill（由清单自动枚举）
    manifest_path = (source_root / "skills/SKILL_MANIFEST.json") if source_root else None
    manifest = {}
    if manifest_path and manifest_path.exists():
        manifest = json.loads(read(manifest_path))
    skills = manifest.get("officialSkills", [])
    if skills:
        for item in sorted(skills, key=lambda s: (s.get("layer", ""), s.get("name", ""))):
            name = item.get("name", "")
            layer = item.get("layer", "")
            src_skill = item.get("path", "")
            body_rel = f"50_Skill正文中文版/{layer}/{name}.md"
            body = read(EDITION / body_rel)
            if body.strip():
                badge = "正文对照"
                add("skill", body_rel, None, body, [src_skill] if src_skill else [], badge)
            else:
                # tech 层：中文要点/摘要 + 英文原文
                section = extract_tech_section(tech_essentials_text, name)
                kind = "中文要点"
                if not section.strip():
                    section = extract_tech_section(tech_index_text, name)
                    kind = "中文摘要"
                if not section.strip():
                    continue
                head = (f"# `{name}` — {kind}（tech 层）\n\n"
                        f"> **源文件**：{src_skill}\n"
                        f"> **说明**：tech 层 Skill 的正文与 references 保留英文（避免与上游分叉），"
                        f"中文侧提供{kind}；右侧英文为本 Skill 的 `SKILL.md` 原文。\n\n{section}")
                add("skill", f"tech/{name}.md", f"`{name}` — {kind}", head,
                    [src_skill] if src_skill else [], f"{kind} + 英文原文")
        # 配套 references
        for layer in ("core", "governance"):
            ref_dir = EDITION / "50_Skill正文中文版" / layer / "references"
            if not ref_dir.exists():
                continue
            for p in sorted(ref_dir.glob("*.md")):
                rel = p.relative_to(EDITION).as_posix()
                add("skill", rel, None, None, None, "references 对照")

    # 8. 校验与结论（只收中文结论类文档，脚本与哈希基线不进站）
    for name in ("校验报告.md", "站点运行时校验.md", "源仓库问题清单.md", "源问题复核结论.md", "技术内容核查结论.md"):
        add("check", f"90_校验/{name}")
    return docs


def build_sync_overview(docs: list[dict]) -> dict:
    rows = []
    for d in docs:
        if d["group"] not in ("rules", "method", "tpl", "skill", "onboard", "start", "idx"):
            continue
        if not d["sources"] and d["sync"] == "new":
            continue
        parity = ""
        if d["en"]:
            parity = f'{d["enHeadings"]} / {d["zhHeadings"]}'
        rows.append({
            "title": d["title"],
            "id": d["id"],
            "group": dict(GROUP_ORDER).get(d["group"], d["group"]),
            "sources": "、".join(d["sources"]) or "（本版新增）",
            "sync": d["sync"],
            "syncText": d["syncText"],
            "parity": parity,
        })
    return {"type": "overview", "rows": rows}


def main() -> int:
    ap = argparse.ArgumentParser(description="生成中文版离线网站")
    ap.add_argument("--source-root", default="")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    source_root = Path(args.source_root).resolve() if args.source_root.strip() else None
    docs = build_docs(source_root)
    if not docs:
        print("没有可生成的文档，请检查中文版目录。")
        return 1

    payload = {"docs": docs, "overview": build_sync_overview(docs),
               "generated": date.today().isoformat(),
               "counts": {
                   "docs": len(docs),
                   "skills": len([d for d in docs if d["group"] == "skill"]),
                   "groups": len({d["group"] for d in docs}),
                   "stale": len([d for d in docs if d["sync"] == "stale"]),
                   "ok": len([d for d in docs if d["sync"] == "ok"]),
                   "new": len([d for d in docs if d["sync"] == "new"]),
               }}
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")

    template = (Path(__file__).resolve().parent / "template.html").read_text(encoding="utf-8")
    html = template.replace("/*__PAYLOAD__*/", data)

    out = Path(args.out).resolve() if args.out.strip() else (EDITION / "site" / "index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"已生成：{out}（{out.stat().st_size / 1024:.0f} KB，文档 {payload['counts']['docs']} 篇，"
          f"其中 Skill 相关 {payload['counts']['skills']} 篇；已同步 {payload['counts']['ok']}，"
          f"源已变更 {payload['counts']['stale']}，本版新增 {payload['counts']['new']}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
