#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DSH PreToolUse 钩子：执行前拦截（写前门禁）。

契约（@deepseek-ai/dsh-hook-protocol）：
  - stdin 收到 Codex 形状的 JSON 载荷（snake_case，无尾随换行）
  - 退出码 0            = 放行
  - 退出码 2 + stderr   = 拦截，stderr 全文作为模型可见的 reason
  - 其它非零退出码       = 记为失败，agent 继续（不拦截）
  - PreToolUse 只拿到「真实 tool_name」与「tool_input.command」（非 shell 工具参数不会暴露），
    因此本钩子只对 shell 命令行做判定，这是运行时的事实边界，不是设计缺口。

规则本体在 methodology_rules.py —— 与 MCP 的 methodology_precheck 工具共用同一份规则，
避免同一件事在两处各写一遍（方法论非协商规则 #3）。

自检（不需要 DSH）：
  py scripts/py/methodology_precheck_hook.py --selftest
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from methodology_rules import DISABLE_ENV, check_shell_command, force_utf8  # noqa: E402

BANNER = "[methodology-precheck] 已拦截此 shell 调用"


def evaluate(payload: dict) -> list[dict]:
    """从载荷判定；返回违规列表（空 = 放行）。"""
    tool = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input")
    command = ""
    if isinstance(tool_input, dict):
        command = str(tool_input.get("command") or "")
    if not command:
        return []
    hits = check_shell_command(command)
    for hit in hits:
        hit["tool_name"] = tool
    return hits


def render(hits: list[dict]) -> str:
    lines = [f"{BANNER}（工具：{hits[0].get('tool_name') or '未知'}）。命中的方法论门禁："]
    for hit in hits:
        lines.append(f"- 规则 {hit['rule']}：命中 `{hit['matched']}`")
        lines.append(f"  {hit['hint']}")
    lines.append(
        f"如需用户明确授权的例外：设置 {DISABLE_ENV}=1 后重试，"
        "或修改 scripts/py/methodology_rules.py 中的规则表。"
    )
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    force_utf8()
    if "--selftest" in argv:
        return selftest()

    if os.environ.get(DISABLE_ENV):
        return 0

    raw = sys.stdin.read()
    if not raw.strip():
        return 0
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        # 载荷不可解析时放行：钩子坏掉不应该让 agent 卡死
        return 0
    if not isinstance(payload, dict):
        return 0

    hits = evaluate(payload)
    if not hits:
        return 0
    sys.stderr.write(render(hits) + "\n")
    return 2


# ---------------------------------------------------------------- 自检

CASES: list[tuple[str, str, bool]] = [
    ("git status", "查看状态应放行", False),
    ("git add scripts/py/methodology_rules.py", "精确暂存应放行", False),
    ("git add -A", "整树暂存应拦截", True),
    ("git add .", "整树暂存应拦截", True),
    ("git commit -m 'x' -a", "commit -a 应拦截", True),
    ("git reset --hard HEAD~1", "reset --hard 应拦截", True),
    ("git clean -fd", "clean -fd 应拦截", True),
    ("git push origin main --force", "强推应拦截", True),
    ("git branch -D feature/x", "强删分支应拦截", True),
    ("Remove-Item -Recurse -Force skills/tech", "递归删源码应拦截", True),
    ("Set-Content runtime\\node_modules\\x.js 'y'", "写 node_modules 应拦截", True),
    ("Set-Content temp\\probe.md 'x'", "默认编码写文本应拦截", True),
    ("Set-Content temp\\probe.md 'x' -Encoding utf8NoBOM", "显式安全编码应放行", False),
    ("git diff --stat", "查看 diff 应放行", False),
    ("py scripts/py/audit_methodology.py --project-root .", "跑门禁应放行", False),
]


def selftest() -> int:
    failed = 0
    for command, label, should_block in CASES:
        payload = {"tool_name": "pwsh", "tool_input": {"command": command}}
        blocked = bool(evaluate(payload))
        ok = blocked == should_block
        if not ok:
            failed += 1
        print(f"  [{'OK' if ok else 'FAIL'}] {'拦截' if blocked else '放行'} | {label} | {command}")

    # 非 shell 工具：参数不暴露，必须放行而不是误判
    non_shell = {"tool_name": "write", "tool_input": {}}
    ok = evaluate(non_shell) == []
    failed += 0 if ok else 1
    print(f"  [{'OK' if ok else 'FAIL'}] 放行 | 非 shell 工具无 command | write")

    # 逃生阀
    os.environ[DISABLE_ENV] = "1"
    ok = main([]) == 0
    os.environ.pop(DISABLE_ENV, None)
    failed += 0 if ok else 1
    print(f"  [{'OK' if ok else 'FAIL'}] 放行 | 逃生阀 {DISABLE_ENV}=1 | (空 stdin)")

    total = len(CASES) + 2
    print(f"\n自检: {total - failed}/{total} 通过")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
