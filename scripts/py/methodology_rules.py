#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""方法论规则单点 | Single source of truth for methodology guard rules.

同一份规则同时被两处消费，避免「同一件事在两个地方各写一遍」（方法论非协商规则 #3）：

  scripts/py/methodology_mcp_server.py   -> methodology_precheck 工具（按文件路径/内容检查）
  scripts/py/methodology_precheck_hook.py -> DSH PreToolUse 钩子（按 shell 命令行检查）

规则来源：AGENTS.md §0.7 安全修改与精准定位、§1 核心哲学、§6 非协商规则，
以及仓库实战缺陷（0D 0D 0A 行尾、UTF-8 BOM、盘符硬编码、硬编码颜色）。
"""

from __future__ import annotations

import re
import sys


def force_utf8() -> None:
    """把 stdio 三流钉死为 UTF-8。

    必须做：Windows 下 Python 的 stdin/stdout/stderr 默认跟随系统代码页（简体中文机器上是
    cp936/gbk），而 MCP 的 stdio 传输与 DSH 钩子载荷都是 UTF-8 字节。不修就会出现
    「写出去的 UTF-8 被按 GBK 解」→ 模型看到乱码，并且会照着乱码**编造**路径/名称
    （实测：把 bootstrap/02_机读三件套 编成了 02_方法论落地）。
    """
    for name in ("stdin", "stdout", "stderr"):
        stream = getattr(sys, name, None)
        if stream is None:
            continue
        try:
            if name == "stdin":
                stream.reconfigure(encoding="utf-8", errors="replace")
            else:
                # newline="\n" 确保 JSON-RPC 行协议恰好用 LF 分帧，而不是 Windows 的 CRLF
                stream.reconfigure(encoding="utf-8", errors="replace", newline="\n")
        except (AttributeError, ValueError):  # 已被重定向为不支持 reconfigure 的对象
            pass

# ---------------------------------------------------------------- 文件/内容规则

#: 禁止写入源码目录的文件名（母版 E2：下划线临时文件污染；备份残留；Windows 保留名）
FORBIDDEN_NAMES = [
    (re.compile(r"^_temp_.*\.py$"), "临时脚本不得进入源码目录（母版 E2：下划线临时文件污染）"),
    (re.compile(r"^_patch.*\.py$"), "补丁脚本不得进入源码目录（母版 E2）"),
    (re.compile(r"^_.*\.py$"), "下划线前缀的临时脚本不得进入源码目录（母版 E2）"),
    (re.compile(r".*\.(bak|orig|rej)$"), "备份/冲突残留文件不得进入源码目录"),
    (re.compile(r"^nul$"), "Windows 保留名 null 文件（母版根目录曾出现 nul）"),
]

DRIVE_PATH = re.compile(rb"\b[A-Z]:[\\/][^\s`\"'|]+")
HEX_COLOR = re.compile(rb"#[0-9a-fA-F]{6}\b")
CONTROL_CHAR = re.compile(rb"[\x00-\x08\x0B\x0C\x0E-\x1F]")
#: SKILL.md 必须以 '---' + CRLF/LF 开头；'---\r\r\n' 会让运行时静默丢弃整个技能
SKILL_OPENING = re.compile(rb"^---[ \t]*(\r\n|\n)")

#: 关闭钩子拦截的逃生阀（需要显式设置；生产默认拦截）
DISABLE_ENV = "METHODOLOGY_HOOK_DISABLE"


def check_bytes(rel_name: str, data: bytes) -> list[dict]:
    """按内容检查一个已存在的文件；返回违规列表（空 = 通过）。"""
    violations: list[dict] = []

    def add(rule: str, hint: str, at: int | None = None) -> None:
        item = {"rule": rule, "file": rel_name, "hint": hint}
        if at is not None:
            item["line"] = data.count(b"\n", 0, at) + 1
        violations.append(item)

    if data[:16].startswith(b"\xef\xbb\xbf"):
        add("bom", "文件以 UTF-8 BOM 开头；技能/规则文件应保持无 BOM。")
    if rel_name.endswith("SKILL.md") and not SKILL_OPENING.match(data[:16]):
        add("skill-frontmatter-delimiter",
            "SKILL.md 必须以 '---' + CRLF/LF 开头；0D 0D 0A 双 CR 会让运行时静默丢弃该技能。")
    if b"\r\r\n" in data:
        add("double-cr", "存在 0D 0D 0A 双 CR 行尾；应规范为 CRLF 或 LF。", data.index(b"\r\r\n"))
    m = DRIVE_PATH.search(data)
    if m:
        add("machine-path", "出现本机盘符路径；示例请使用仓库相对路径。", m.start())
    m = HEX_COLOR.search(data)
    if m:
        add("hardcoded-color", "出现十六进制颜色字面量；请使用主题变量。", m.start())
    m = CONTROL_CHAR.search(data)
    if m:
        add("control-char", "出现禁用控制字符。", m.start())
    return violations


def check_name(name: str) -> list[dict]:
    """按文件名检查（无需文件存在）。"""
    return [{"rule": "forbidden-name", "file": name, "hint": hint}
            for pattern, hint in FORBIDDEN_NAMES if pattern.match(name)]


# ---------------------------------------------------------------- shell 命令行规则

#: (编译后正则, 规则 id, 原因与替代做法)。正则大小写不敏感、容忍多空格。
SHELL_RULES: list[tuple[re.Pattern, str, str]] = [
    (
        re.compile(r"git\s+add\s+(-A|--all)\b|git\s+add\s+\.\s*$|git\s+commit\s+[^\n]*\s-a\b", re.I),
        "bulk-staging",
        "禁止整树暂存（git add -A / . / commit -a）：AGENTS.md §0.7 要求用精确文件或 hunk 暂存，"
        "并先检查 diff。请改为 `git add <具体路径...>`。",
    ),
    (
        re.compile(r"git\s+reset\s+--hard|git\s+checkout\s+--\s+\.|git\s+clean\s+-[a-z]*[fd]", re.I),
        "destructive-git",
        "禁止破坏性 Git 操作（reset --hard / checkout -- . / clean -fd）：会不可恢复地丢弃工作区改动。"
        "AGENTS.md §0.7：共享/未知/租户数据默认保全，破坏性操作需用户明示确认与恢复证据。",
    ),
    (
        re.compile(r"git\s+push\s+[^\n]*--force|git\s+push\s+[^\n]*\s-f\b|git\s+branch\s+-D\b", re.I),
        "force-push-or-branch-delete",
        "禁止强推或强删分支（push --force / branch -D）：需用户明示授权，并给出回滚路径。",
    ),
    (
        re.compile(r"node_modules[\\/]", re.I),
        "write-into-node-modules",
        "禁止写入 node_modules：DSH 是已安装发行版，升级脚本会覆盖该目录。"
        "要改行为请改 profile 的 cordis.patch.yml，或向 DSH 上游反馈。",
    ),
    (
        re.compile(r"remove-item[^\n]*-recurse[^\n]*-force[^\n]*(skills|docs|scripts|rules|i18n|methodology)"
                   r"|rm\s+-[a-z]*r[a-z]*f?\s+[^\n]*(skills|docs|scripts|rules|i18n)"
                   r"|rmdir\s+/s\s+/q[^\n]*(skills|docs|scripts|rules|i18n)"
                   r"|del\s+/[fsq][^\n]*(skills|docs|scripts|rules|i18n)", re.I),
        "recursive-delete-source",
        "禁止对源码目录递归强删（skills/docs/scripts/rules/i18n）：分类为破坏性操作，"
        "需用户明示确认与恢复证据（AGENTS.md §0.7）。",
    ),
    (
        re.compile(r"out-file[^\n]*-encoding\s+(utf8|ascii)\b[^\n]*\.(md|py|json|yml|yaml)"
                   r"|set-content[^\n]*\.(md|py|json|yml|yaml)", re.I),
        "encoding-risk-write",
        "写入文本文件请避免 PowerShell 默认编码（UTF-8 带 BOM 会触发 SKILL_FRONTMATTER_BOM；"
        "BOM/双 CR 会让运行时静默丢技能）。优先用 write/edit 工具，或显式加 `-Encoding utf8NoBOM`。",
    ),
]

#: 规则例外：命中即放行。规则本意是禁止「默认编码」，不是禁止写文件本身——
#: 显式声明安全编码时必须放行，否则会把正确做法也拦掉（实战发现的误报）。
RULE_EXCEPTIONS: dict[str, re.Pattern] = {
    "encoding-risk-write": re.compile(r"-Encoding\s+(utf8NoBOM|utf8)\b", re.I),
}


def check_shell_command(command: str) -> list[dict]:
    """按 shell 命令行检查；返回违规列表（空 = 放行）。"""
    if not command:
        return []
    hits = []
    for pattern, rule, hint in SHELL_RULES:
        m = pattern.search(command)
        if not m:
            continue
        exception = RULE_EXCEPTIONS.get(rule)
        if exception is not None and exception.search(command):
            continue
        hits.append({"rule": rule, "matched": m.group(0).strip(), "hint": hint})
    return hits
