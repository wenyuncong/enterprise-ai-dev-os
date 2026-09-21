#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression test for the methodology guard: shared rules + PreToolUse hook + MCP server.

Why these tests exist (evidence, 2026-09-15):
  1. The first live DSH session that called the MCP tools showed `���ж����յȼ�` in the
     tool result and the model then **invented** a source path (`bootstrap/02_方法论落地`)
     that does not exist — it had reconstructed a plausible Chinese folder name from
     mojibake. Root cause: Windows Python defaults stdin/stdout/stderr to the system code
     page (cp936/gbk) while MCP stdio and hook payloads are UTF-8. `force_utf8()` fixes it;
     `test_hook_stderr_is_utf8` fails if that regresses.
  2. In the same session `methodology_route` returned `matched_route_id: null` for a Chinese
     task that matches locally — the task string itself had been decoded as GBK on the way in.

The tests drive the real contracts: hook exit code 2 + stderr is the blocking contract of
`@deepseek-ai/dsh-hook-protocol`, so it is asserted by spawning the hook as a process.

Run:  py scripts/py/test_methodology_guard.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import methodology_mcp_server as mcp  # noqa: E402
import methodology_rules as rules  # noqa: E402

HOOK = HERE / "methodology_precheck_hook.py"


def run_hook(payload: dict | str | None, extra_env: dict | None = None) -> subprocess.CompletedProcess:
    """Run the hook exactly as DSH does: JSON on stdin, verdict on the exit code."""
    stdin = "" if payload is None else (payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False))
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        env={**__import__("os").environ, **(extra_env or {})},
        timeout=30,
    )


class ShellRuleTable(unittest.TestCase):
    def test_blocks_bulk_staging(self) -> None:
        for command in ("git add -A", "git add .", "git add --all", "git commit -m x -a"):
            self.assertTrue(rules.check_shell_command(command), command)

    def test_blocks_destructive_git(self) -> None:
        for command in ("git reset --hard HEAD~1", "git clean -fd", "git checkout -- .",
                        "git push origin main --force", "git branch -D feature"):
            self.assertTrue(rules.check_shell_command(command), command)

    def test_blocks_node_modules_write(self) -> None:
        self.assertTrue(rules.check_shell_command(r"Set-Content runtime\node_modules\x.js 'y'"))

    def test_default_encoding_write_is_blocked_but_explicit_safe_encoding_is_not(self) -> None:
        # 规则本意是禁止「默认编码」，不是禁止写文件；显式 utf8NoBOM 是正确做法，必须放行。
        self.assertTrue(rules.check_shell_command(r"Set-Content temp\probe.md 'x'"))
        self.assertEqual(rules.check_shell_command(r"Set-Content temp\probe.md 'x' -Encoding utf8NoBOM"), [])

    def test_allows_precise_staging_and_reads(self) -> None:
        for command in ("git status", "git diff --stat", "git add scripts/py/rule_lint.py",
                        "py scripts/py/audit_methodology.py --project-root ."):
            self.assertEqual(rules.check_shell_command(command), [], command)

    def test_empty_command_is_not_a_violation(self) -> None:
        self.assertEqual(rules.check_shell_command(""), [])


class ContentRules(unittest.TestCase):
    def test_double_cr_is_blocking(self) -> None:
        codes = [v["rule"] for v in rules.check_bytes("skills/tech/x/SKILL.md", b"---\r\r\nname: x\r\n")]
        self.assertIn("double-cr", codes)
        self.assertIn("skill-frontmatter-delimiter", codes)

    def test_bom_and_clean_file(self) -> None:
        self.assertIn("bom", [v["rule"] for v in rules.check_bytes("a.md", b"\xef\xbb\xbf# a\r\n")])
        self.assertEqual(rules.check_bytes("a.md", "# a\r\nplain\r\n".encode()), [])

    def test_machine_path_and_hardcoded_color(self) -> None:
        codes = [v["rule"] for v in rules.check_bytes("a.md", "见 C:\\Users\\me\\x, 颜色 #ff0000\r\n".encode())]
        self.assertIn("machine-path", codes)
        self.assertIn("hardcoded-color", codes)

    def test_forbidden_names(self) -> None:
        self.assertTrue(rules.check_name("_temp_probe.py"))
        self.assertTrue(rules.check_name("deploy.ps1.bak"))
        self.assertEqual(rules.check_name("methodology_rules.py"), [])


class HookProcessContract(unittest.TestCase):
    """The blocking contract: exit 2 with the reason on stderr; exit 0 means allow."""

    def test_benign_command_exits_zero_with_no_reason(self) -> None:
        proc = run_hook({"tool_name": "pwsh", "tool_input": {"command": "git status"}})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stderr.strip(), "")

    def test_bulk_staging_is_blocked_with_reason(self) -> None:
        proc = run_hook({"tool_name": "pwsh", "tool_input": {"command": "git add -A"}})
        self.assertEqual(proc.returncode, 2, proc.stdout)
        self.assertIn("bulk-staging", proc.stderr)
        self.assertIn("git add <具体路径...>", proc.stderr)

    def test_non_shell_tool_payload_is_allowed(self) -> None:
        # PreToolUse does not expose non-shell tool arguments; the hook must not guess.
        proc = run_hook({"tool_name": "write", "tool_input": {}})
        self.assertEqual(proc.returncode, 0)

    def test_malformed_payload_fails_open(self) -> None:
        # A broken hook must never wedge the agent: unparsable input allows the call.
        proc = run_hook("{not json")
        self.assertEqual(proc.returncode, 0)

    def test_empty_stdin_is_allowed(self) -> None:
        self.assertEqual(run_hook(None).returncode, 0)

    def test_escape_hatch_disables_the_guard(self) -> None:
        proc = run_hook({"tool_name": "pwsh", "tool_input": {"command": "git add -A"}},
                        extra_env={rules.DISABLE_ENV: "1"})
        self.assertEqual(proc.returncode, 0)

    def test_hook_stderr_is_utf8(self) -> None:
        """Locks the gbk-mojibake defect: the reason must survive a strict UTF-8 decode."""
        proc = run_hook({"tool_name": "pwsh", "tool_input": {"command": "git add -A"}})
        self.assertNotIn("\ufffd", proc.stderr)
        self.assertTrue(any("\u4e00" <= ch <= "\u9fff" for ch in proc.stderr),
                        f"理由里应含中文且未乱码，实际：{proc.stderr[:80]!r}")


class StdioTransport(unittest.TestCase):
    """真实管道往返：MCP stdio 传输的分帧与编码，是 handle() 单测覆盖不到的一层。"""

    def test_pipe_round_trip_preserves_chinese_and_framing(self) -> None:
        proc = subprocess.Popen(
            [sys.executable, str(HERE / "methodology_mcp_server.py")],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="strict",
        )
        try:
            def send(obj: dict) -> None:
                proc.stdin.write(json.dumps(obj, ensure_ascii=False) + "\n")
                proc.stdin.flush()

            def recv() -> dict:
                return json.loads(proc.stdout.readline())

            send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                  "params": {"protocolVersion": "2025-06-18"}})
            self.assertEqual(recv()["result"]["protocolVersion"], "2025-06-18")

            send({"jsonrpc": "2.0", "method": "notifications/initialized"})  # 通知：不应有回包
            send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
            self.assertEqual(len(recv()["result"]["tools"]), 4)

            send({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                  "params": {"name": "methodology_route",
                             "arguments": {"task": "修复采购退货已记账单据的按钮不一致"}}})
            body = json.loads(recv()["result"]["content"][0]["text"])
            self.assertEqual(body["matched_route_id"], "route-business-flow")
            self.assertNotIn("\ufffd", json.dumps(body, ensure_ascii=False))
        finally:
            proc.stdin.close()
            proc.wait(timeout=30)
            stderr_text = proc.stderr.read()
            proc.stdout.close()
            proc.stderr.close()
        self.assertEqual(stderr_text.strip(), "", "服务端不应向 stderr 写任何东西")


@unittest.skipUnless(shutil.which("pwsh") or shutil.which("powershell"),
                     "需要 PowerShell 才能验证退出码传播")
class PowershellExitCodeContract(unittest.TestCase):
    """锁定最隐蔽的一个 fail-open：钩子经 PowerShell 执行时的退出码掩码。

    实测（2026-09-14）：钩子脚本 `raise SystemExit(2)` 时，`pwsh -Command "& python hook.py"`
    报回的退出码是 **1**，不是 2。dsh-hook-protocol 只把 2 当拦截，其它非零一律记为「钩子失败」
    并放行——于是门禁静默失效，命令照常执行（实测文件被创建）。
    修法是在命令末尾补 `; exit $LASTEXITCODE`。本测试同时锁住正反两面。
    """

    SHELL = shutil.which("pwsh") or shutil.which("powershell")
    BLOCKING_PAYLOAD = json.dumps(
        {"tool_name": "pwsh", "tool_input": {"command": "git add -A"}}, ensure_ascii=False)

    def _run(self, command: str) -> int:
        proc = subprocess.run([self.SHELL, "-NoProfile", "-Command", command],
                              input=self.BLOCKING_PAYLOAD, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=60)
        return proc.returncode

    def _base(self) -> str:
        return f'& "{sys.executable}" "{HOOK}"'

    def test_exit_last_exitcode_propagates_the_blocking_code(self) -> None:
        self.assertEqual(self._run(self._base() + "; exit $LASTEXITCODE"), 2)

    def test_without_exit_last_exitcode_the_blocking_code_is_masked(self) -> None:
        # 这条断言记录的是 PowerShell 的行为，不是我们想要的契约；它解释了门禁为何曾静默失效。
        masked = self._run(self._base())
        self.assertNotEqual(masked, 2, "若这里变成 2，说明 PowerShell 行为变了，hooks.json 可以简化")


class McpProtocol(unittest.TestCase):
    def test_initialize_echoes_client_protocol_version(self) -> None:
        reply = mcp.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                            "params": {"protocolVersion": "2025-03-26"}})
        self.assertEqual(reply["result"]["protocolVersion"], "2025-03-26")
        self.assertEqual(reply["result"]["serverInfo"]["name"], "methodology-mcp")

    def test_tools_list_exposes_the_four_tools(self) -> None:
        reply = mcp.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        names = sorted(t["name"] for t in reply["result"]["tools"])
        self.assertEqual(names, ["methodology_gate", "methodology_precheck",
                                 "methodology_route", "methodology_sync"])

    def test_every_tool_declares_an_input_schema(self) -> None:
        for tool in mcp.TOOLS:
            self.assertEqual(tool["inputSchema"]["type"], "object", tool["name"])
            self.assertTrue(tool["description"].strip(), tool["name"])

    def test_call_returns_json_content_and_flags_temp_scripts(self) -> None:
        reply = mcp.handle({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                            "params": {"name": "methodology_precheck",
                                       "arguments": {"paths": ["scripts/py/_temp_probe.py"]}}})
        body = json.loads(reply["result"]["content"][0]["text"])
        self.assertFalse(body["allow"])
        self.assertIn("forbidden-name", [v["rule"] for v in body["violations"]])

    def test_chinese_survives_the_content_round_trip(self) -> None:
        """Locks the gbk-mojibake defect in both directions.

        Inbound: the Chinese task must reach the server intact — otherwise keyword matching
        fails and `matched_route_id` comes back null (observed live before force_utf8()).
        Outbound: the returned body must contain readable CJK, never U+FFFD.
        """
        reply = mcp.handle({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
                            "params": {"name": "methodology_route",
                                       "arguments": {"task": "修复采购退货已记账单据的按钮不一致"}}})
        text = reply["result"]["content"][0]["text"]
        self.assertNotIn("\ufffd", text)
        body = json.loads(text)
        self.assertEqual(body["matched_route_id"], "route-business-flow",
                         "中文 task 必须能命中中文关键词路由；返回 null 说明入站字符串被按 GBK 解坏了")
        self.assertTrue(any("\u4e00" <= ch <= "\u9fff" for ch in text), "返回体应含可读中文")

    def test_unknown_tool_is_a_protocol_error(self) -> None:
        reply = mcp.handle({"jsonrpc": "2.0", "id": 5, "method": "tools/call",
                            "params": {"name": "nope", "arguments": {}}})
        self.assertEqual(reply["error"]["code"], -32602)

    def test_unknown_method_is_a_protocol_error(self) -> None:
        reply = mcp.handle({"jsonrpc": "2.0", "id": 6, "method": "resources/list"})
        self.assertEqual(reply["error"]["code"], -32601)

    def test_notification_produces_no_response(self) -> None:
        self.assertIsNone(mcp.handle({"jsonrpc": "2.0", "method": "notifications/initialized"}))

    def test_gate_and_sync_report_real_repo_state(self) -> None:
        gate = json.loads(mcp.handle({"jsonrpc": "2.0", "id": 7, "method": "tools/call",
                                      "params": {"name": "methodology_gate",
                                                 "arguments": {"level": "L1"}}})["result"]["content"][0]["text"])
        self.assertIn(gate["pass"], (True, False))
        self.assertTrue(gate["results"], "gate 至少要返回一项真实执行结果")
        sync = json.loads(mcp.handle({"jsonrpc": "2.0", "id": 8, "method": "tools/call",
                                      "params": {"name": "methodology_sync",
                                                 "arguments": {}}})["result"]["content"][0]["text"])
        self.assertGreater(sync["synced"], 0)


if __name__ == "__main__":
    rules.force_utf8()  # 测试自身的输出也要 UTF-8，否则中文断言失败信息在本机控制台是乱码
    unittest.main(verbosity=2)
