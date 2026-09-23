#!/usr/bin/env python3
"""Skill health scan across all three skill libraries.

Scans system skills (Doubao runtime), user skills, and the project
methodology skill tree; reports readability (frontmatter + body) and
executability (references, commands, python libs, platform differences).

Judgments: OK / PARTIAL / BROKEN (unreadable).
Reference misses are classified: real_missing (hard), external (designed
to run inside another project root, e.g. gerp codebase), runtime (generated
artifacts / placeholders / wildcards).

Usage: python scan_skill_health.py > result.jsonl
Output: one JSON object per skill, UTF-8.
"""# -*- coding: utf-8 -*-
"""批量技能体检 v3：降低误报。
- 命令：python3->python、pip->python -m pip 视为平台差异而非缺失；
- 引用：裸文件名在技能目录递归查找；跨技能引用单独统计；目录引用单独统计；
- 库：只统计真实 import（排除文档示例代码块）。
"""
import os, re, sys, json, subprocess

SKILL_ROOTS = [
    r"C:\Users\Administrator\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.skills",
    r"C:\Users\Administrator\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.user_skills",
    r"G:\企业级梦境系统\skills",
]

# 命令 -> (真实命令, 是否仅平台差异)
CMD_ALIAS = {
    "python3": ("python", True),
    "pip": ("python", True),
    "pip3": ("python", True),
    "slides": ("lark-cli", True),
}

# PATH 外探测表：工具已安装但未加入 PATH 时的常见安装位置。
# 命中这些位置说明工具"已安装（可用/部分可用）"，不应判为缺失。
# 维护方法：本机实测安装位置 + 各工具官方默认安装目录。
KNOWN_INSTALL_LOCATIONS = {
    "codex": [
        r"C:\Users\Administrator\AppData\Local\OpenAI\Codex\bin\247581e40ee272fb\codex.exe",
        r"C:\Users\Administrator\.codex",
        # 通用：%LOCALAPPDATA%\OpenAI\Codex\bin\*\codex.exe（见 probe_dir）
    ],
    "flutter": [
        r"D:\flutter\bin\flutter.bat",
        r"G:\DevTools\flutter\bin\flutter.bat",
        r"C:\flutter\bin\flutter.bat",
    ],
    "playwright": [
        r"C:\Users\Administrator\AppData\Local\ms-playwright",
    ],
    "docker": [
        r"C:\Program Files\Docker\Docker\resources\bin\docker.exe",
        r"C:\Program Files\Docker\Docker\Docker Desktop.exe",
        # 注意：C:\ProgramData\DockerDesktop 仅含安装日志（残留），不是可用安装，不作为命中。
    ],
    "code": [
        r"C:\Program Files\Microsoft VS Code\bin\code.cmd",
        r"C:\Users\Administrator\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd",
    ],
    "mysql": [
        r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
    ],
    "go": [r"C:\Program Files\Go\bin\go.exe", r"C:\Go\bin\go.exe"],
    "psql": [r"C:\Program Files\PostgreSQL\*\bin\psql.exe"],
    "soffice": [r"C:\Program Files\LibreOffice\program\soffice.exe"],
    "codex_extra": [],  # placeholder
}

def _probe_install_location(cmd):
    """在 PATH 外探测已知安装位置；命中返回 True。"""
    locs = KNOWN_INSTALL_LOCATIONS.get(cmd, [])
    for loc in locs:
        if "*" in loc:
            # 支持单个 * 通配（如 PostgreSQL 版本目录）
            import glob as _glob
            hits = _glob.glob(loc)
            if hits:
                return True
            continue
        try:
            if os.path.exists(loc):
                return True
        except Exception:
            continue
    # 通用探测：OpenAI Codex bin 下任意版本子目录
    if cmd == "codex":
        base = os.path.expandvars(r"%LOCALAPPDATA%\OpenAI\Codex\bin")
        if os.path.isdir(base):
            for sub in os.listdir(base):
                if os.path.isfile(os.path.join(base, sub, "codex.exe")):
                    return True
    return False

def cmd_exists(cmd):
    try:
        r = subprocess.run(["where" if os.name=="nt" else "which", cmd], capture_output=True, timeout=5)
        return r.returncode == 0
    except Exception:
        return False

def collect_skill_dirs(root):
    out = []
    if not os.path.isdir(root):
        return out
    for name in sorted(os.listdir(root)):
        d = os.path.join(root, name)
        if not os.path.isdir(d):
            continue
        if os.path.exists(os.path.join(d, "SKILL.md")):
            out.append((d, name))
        else:
            for sub in sorted(os.listdir(d)):
                dd = os.path.join(d, sub)
                if os.path.isdir(dd) and os.path.exists(os.path.join(dd, "SKILL.md")):
                    out.append((dd, name + "/" + sub))
    return out

def scan_skill(d, name):
    rec = {"name": name, "path": d, "has_skill_md": False, "readable": False,
           "skill_md_bytes": 0, "refs_real_missing": [], "refs_cross_skill": [],
           "refs_external": [], "refs_runtime": [], "refs_dir_missing": [],
           "cmds_missing": [], "cmds_platform_diff": [], "cmds_installed_no_path": [],
           "libs_missing": [], "verdict": "UNKNOWN", "issues": []}
    if ".user_skills" in d:
        rec["lib"] = "user"
    elif "G:\\企业级梦境系统\\skills" in d:
        rec["lib"] = "methodology"
    else:
        rec["lib"] = "system"
    smd = os.path.join(d, "SKILL.md")
    if not os.path.isfile(smd):
        rec["issues"].append("无 SKILL.md")
        rec["verdict"] = "EMPTY"
        return rec
    rec["has_skill_md"] = True
    rec["skill_md_bytes"] = os.path.getsize(smd)
    try:
        txt = open(smd, encoding="utf-8-sig", errors="replace").read()
    except Exception as e:
        txt = ""
        rec["issues"].append("SKILL.md读取失败: %s" % e)
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", txt, re.S)
    fm = m.group(1) if m else ""
    fm_name = bool(re.search(r"(?im)^name\s*:", fm))
    fm_desc = bool(re.search(r"(?im)^description\s*:", fm))
    body = txt[m.end():] if m else txt
    rec["readable"] = fm_name and fm_desc and len(body.strip()) >= 200
    if not rec["readable"]:
        rec["issues"].append("frontmatter缺name/description或正文<200字符")
        rec["verdict"] = "BROKEN"
        return rec

    # ---- 引用检查（更严格） ----
    # 外部项目上下文目录：引用首段命中这些目录且技能目录内不存在时，
    # 视为"运行位置错位"（设计为在特定项目根运行），不判硬缺失。
    EXTERNAL_DIRS = {
        "agent-studio", "backend", "frontend", "database", "scripts", "docs",
        "tools", "methodology", "rules", "deployment", "src", "lib", "bin",
        "assets", "examples", "schemas", "templates", "test", "tests", "config",
    }
    lines = txt.splitlines()
    refs = {}
    def is_example_line(line):
        l = line.strip().lower()
        if l.startswith("|") and "example" in l:
            return True
        if "example:" in l or "examples:" in l:
            return True
        if l.startswith("**example**") or l.startswith("- **example"):
            return True
        if l.startswith("see ") or l.startswith("> see ") or l.endswith(". see"):
            return True
        return False
    for i, line in enumerate(lines):
        if is_example_line(line):
            continue
        for mm in re.finditer(r"\]\(([^)#\s]+)\)", line):
            p = mm.group(1).lstrip("./")
            if p.startswith(("http://","https://","#","mailto:","data:")):
                continue
            refs.setdefault(p, i + 1)
        for mm in re.finditer(r"`([^`]*\.(?:py|js|mjs|cjs|ts|ps1|sh|bat|cmd|json|md|yml|yaml|toml|sql))`", line):
            refs.setdefault(mm.group(1).lstrip("./"), i + 1)
    all_skill_names = set()
    for root in SKILL_ROOTS:
        for dd, nm in collect_skill_dirs(root):
            all_skill_names.add(nm.split("/")[-1])
    for ref in sorted(refs):
        if " " in ref or "$" in ref or "{" in ref:
            continue
        # 通配符 / 占位符 / 运行时生成物 / 纯扩展名 / URL 占位 → 非硬缺失
        base = os.path.basename(ref).lower()
        low = ref.lower()
        if ("*" in ref or "?" in ref or "<" in ref or ">" in ref or "【" in ref or "】" in ref
                or "url" in low or low.startswith("http")
                or "yyyy" in low or ref.lower() == "url"
                or ref.startswith("@") or ref.startswith("~")
                or base in ("cmd", "json", "md", "py", "ps1", "ts", "js", "yml", "yaml", "sql", "sh")
                or "shturl.cc" in low
                or low.startswith("附件") or low.startswith("doc_url") or low.startswith("图片url")
                or "_internal_do_not_deliver" in low or "do_not_deliver" in low
                or low.startswith("final_reply_body") or low.startswith("00_resume")
                or low.startswith("workflow/") or low.startswith("output/") or low.startswith("parts/")
                or low.startswith("manuscript/") or low.startswith("platforms/")
                or low.startswith("references/playbooks/") or low.startswith("references/module-details/")
                or "ledger" in base or "handoff" in low or "manifest" in base
                or "brief" in base or "intake" in base or "checklist" in base
                or "report" in base or "facts" in base or "state" in base
                or "schema" in base or "brief" in low):
            if not hasattr(rec, "refs_runtime"):
                rec["refs_runtime"] = []
            rec["refs_runtime"].append(ref)
            continue
        # 跨技能引用（如 lark-task/SKILL.md）
        parts = ref.split("/")
        if len(parts) >= 2 and parts[0] in all_skill_names and parts[0] != name.split("/")[-1]:
            rec["refs_cross_skill"].append(ref)
            continue
        # 目录引用（如 scripts/ps1/）
        if ref.endswith("/"):
            rec["refs_dir_missing"].append(ref)  # 目录引用，单独统计，不作为硬缺失
            continue
        fp = os.path.normpath(os.path.join(d, ref))
        if os.path.exists(fp):
            continue
        # 裸文件名：递归查找
        base = os.path.basename(ref)
        found = False
        for dirpath, dirnames, filenames in os.walk(d):
            if base in filenames:
                found = True
                break
        if not found:
            # 外部项目上下文引用（设计为在特定项目根运行）→ 软缺失
            first_seg = parts[0]
            if first_seg in EXTERNAL_DIRS:
                if not hasattr(rec, "refs_external"):
                    rec["refs_external"] = []
                rec["refs_external"].append(ref)
                continue
            rec["refs_real_missing"].append(ref)

    # ---- 命令检查（等价替代） ----
    cmd_mentions = set()
    for mm in re.finditer(r"`([^`]{2,80})`", txt):
        s = mm.group(1).strip()
        first = re.split(r"\s+", s)[0] if s else ""
        first = first.split("\\")[-1].split("/")[-1]
        if first and first.lower() in CMD_ALIAS or (first and first.lower() in ["python","python3","py","node","npm","npx","git","java","javac","mysql","lark-cli","mediakit-cli","cnb","wecom-cli","dws","tmeet","ffmpeg","yt-dlp","docker","flutter","code","codex","playwright","curl","wget","jq","dotnet","go","cargo","rustc","psql","redis-cli","soffice","unzip","tar"]):
            cmd_mentions.add(first.lower())
    for c in sorted(cmd_mentions):
        if cmd_exists(c):
            continue
        if c in CMD_ALIAS:
            alias, is_diff = CMD_ALIAS[c]
            if cmd_exists(alias):
                rec["cmds_platform_diff"].append(c)
                continue
        if _probe_install_location(c):
            # 已安装但不在 PATH：记入"已安装未入PATH"，不判缺失
            if not hasattr(rec, "cmds_installed_no_path"):
                rec["cmds_installed_no_path"] = []
            rec["cmds_installed_no_path"].append(c)
            continue
        rec["cmds_missing"].append(c)

    # ---- Python 库（只统计代码块内的 import，避免示例误报） ----
    libs = set()
    STDLIB = set("""os sys re json subprocess argparse pathlib typing datetime collections itertools math
        time random shutil tempfile io base64 hashlib urllib functools string glob csv sqlite3 abc
        dataclasses enum traceback logging unicodedata html xml copy weakref contextlib signal socket
        ssl http select struct zlib gzip bz2 lzma zipfile tarfile threading queue multiprocessing
        asyncio concurrent ctypes platform stat sysconfig textwrap pprint numbers decimal fractions
        operator bisect array calendar codecs difflib dis fnmatch getpass gettext grp heapq hmac
        imp importlib inspect keyword linecache locale marshal mmap msvcrt netrc nntplib optparse
        pickle pipes pkgutil poplib posixpath profile pstats pty pwd py_compile pyclbr pydoc quopri
        reprlib rlcompleter runpy sched secrets selectors shelve shlex smtpd smtplib sndhdr spwd
        statistics stringprep struct sunau symtable sysconfig tabnanny telnetlib tempfile termios
        test textwrap thread time timeit tkinter token tokenize trace tracemalloc turtle types uuid
        venv warnings wave weakref webbrowser winreg winsound wsgiref xdrlib xml xmlrpc zipapp
        zoneinfo typing""".split())
    for mm in re.finditer(r"```[^\n]*\n(.*?)```", body, re.S):
        block = mm.group(1)
        for im in re.finditer(r"(?m)^\s*(?:import|from)\s+([\w\.]+)", block):
            top = im.group(1).split(".")[0]
            if top and top not in STDLIB and top not in ("__future__",):
                libs.add(top)
    for l in sorted(libs):
        try:
            import importlib.util
            if importlib.util.find_spec(l) is None:
                rec["libs_missing"].append(l)
        except Exception:
            rec["libs_missing"].append(l)

    # ---- 判定 ----
    hard = rec["refs_real_missing"]
    soft = (rec["cmds_missing"] or rec["libs_missing"] or rec["cmds_platform_diff"]
            or rec["refs_dir_missing"] or rec["refs_external"] or rec["refs_runtime"]
            or getattr(rec, "cmds_installed_no_path", []))
    if hard:
        rec["verdict"] = "PARTIAL"
        rec["issues"].append("引用文件真实缺失 %d 处（硬伤）" % len(hard))
    elif soft:
        rec["verdict"] = "PARTIAL"
        kinds = []
        if rec["cmds_missing"]: kinds.append("命令缺失%d" % len(rec["cmds_missing"]))
        if rec["libs_missing"]: kinds.append("库缺失%d" % len(rec["libs_missing"]))
        if rec["cmds_platform_diff"]: kinds.append("平台差异%d" % len(rec["cmds_platform_diff"]))
        if rec["refs_dir_missing"]: kinds.append("目录引用%d" % len(rec["refs_dir_missing"]))
        if rec["refs_external"]: kinds.append("外部项目引用%d" % len(rec["refs_external"]))
        if rec["refs_runtime"]: kinds.append("运行时/占位引用%d" % len(rec["refs_runtime"]))
        if getattr(rec, "cmds_installed_no_path", []): kinds.append("已装未入PATH%d" % len(rec["cmds_installed_no_path"]))
        rec["issues"].append("软缺失：" + "、".join(kinds))
    else:
        rec["verdict"] = "OK"
    return rec

def main():
    for root in SKILL_ROOTS:
        for d, name in collect_skill_dirs(root):
            sys.stdout.write(json.dumps(scan_skill(d, name), ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()

