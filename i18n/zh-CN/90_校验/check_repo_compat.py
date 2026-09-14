#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""兼容预检：中文版并入主仓库后，会不会让主仓库自己的 check_portability 判红。

主仓库的 `scripts/py/audit_methodology.py` 会扫描 `AGENTS.md / rules / skills / methodology / docs / README.md`
下的文件，命中「本机盘符路径」「本机源仓库名」「过期控制文档路径」或非法控制字符即 FAIL。
本脚本直接复用它的规则常量，对中文版**全部文件**做同样的检查，作为提交前的自检。

用法（在中文版根目录内执行）：
  py 90_校验/check_repo_compat.py --source-root "<英文方法论仓库路径>"

退出码：1 = 有命中（提交前必须修掉）；0 = 干净。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

EDITION = Path(__file__).resolve().parent.parent
SUFFIXES = {".md", ".json", ".py", ".mjs", ".js", ".ps1", ".yml", ".yaml"}


def main() -> int:
    ap = argparse.ArgumentParser(description="中文版与主仓库扫描规则的兼容预检")
    ap.add_argument("--source-root", required=True, help="英文方法论仓库路径")
    ap.add_argument("--edition-root", default=str(EDITION), help="中文版根目录；默认取本脚本上一级")
    args = ap.parse_args()

    source = Path(args.source_root).resolve()
    edition = Path(args.edition_root).resolve()
    sys.path.insert(0, str(source / "scripts" / "py"))
    try:
        import audit_methodology as am  # noqa: PLC0415
    except ImportError as exc:
        print(f"无法从 {source} 导入 audit_methodology：{exc}", file=sys.stderr)
        return 2

    hits: list[tuple[str, str]] = []
    scanned = 0
    for path in sorted(edition.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUFFIXES:
            continue
        scanned += 1
        rel = path.relative_to(edition).as_posix()
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            hits.append(("NOT_UTF8", rel))
            continue
        if am.CONTROL_CHARACTER_PATTERN.search(text):
            hits.append(("CONTROL_CHARACTER", rel))
        for rx, label in am.BLOCKED_PATTERNS:
            m = rx.search(text)
            if m:
                line = text.count("\n", 0, m.start()) + 1
                hits.append((label, f"{rel}:L{line}"))

    print(f"主仓库扫描规则兼容预检：扫描 {scanned} 个文件，命中 {len(hits)} 处")
    for label, loc in hits:
        print(f"  [{label}] {loc}（命中内容已隐去）")
    if hits:
        print("结论：提交前必须修掉以上命中项，否则主仓库 audit_methodology.py 会 FAIL。")
        return 1
    print("结论：干净——中文版不会让主仓库的 check_portability 变红。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
