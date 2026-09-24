#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Skill precondition (frontmatter metadata.requires) governor.

让技能可用性在"加载前即可判定"：依据 skill_requirements_map.json，为技能
frontmatter 注入/校验 `metadata.requires`（bins / env / libs / path-vars /
scope / declared-by）。

- scan (默认): 输出每个技能的前置条件声明状态 JSONL。
- --fix:       对映射中有条目、且尚未声明的技能做文本级注入（只增不改，
               保留原 frontmatter、BOM、CRLF）；幂等，可重复运行。

作用域 scope: universal / project / runtime（见映射文件 _meta）。

Usage:
  python skill_requires_governor.py                 # scan all 3 libs -> JSONL
  python skill_requires_governor.py --fix           # inject declared requirements
  python skill_requires_governor.py --fix --roots <dir> ...
"""
import os, re, sys, json, argparse

DEFAULT_ROOTS = [
    r"C:\Users\Administrator\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.skills",
    r"C:\Users\Administrator\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.user_skills",
    r"G:\企业级梦境系统\skills",
]
DECLARED_BY = "enterprise-ai-dev-os"
MARK_RE = re.compile(r"(?m)^[ \t]+declared-by:\s*" + re.escape(DECLARED_BY) + r"\s*$")


def lib_of(d):
    if ".user_skills" in d:
        return "user"
    if "G:\\企业级梦境系统\\skills" in d:
        return "method"
    return "system"


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


def split_frontmatter(text):
    """返回 (fm_text, body_text, start, end)；无 frontmatter 返回 None 标记。"""
    m = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", text, re.S)
    if not m:
        return None
    return m.group(1), text[m.end():], m.start(1), m.end(1)


def has_own_requires(fm):
    """frontmatter 是否已有（非本工具标记的）requires。"""
    return bool(re.search(r"(?m)^[ \t]+requires\s*:", fm))


def build_requires_block(spec, base_indent="  "):
    """生成 requires 块文本（换行用 \\n）。base_indent 作用于 `requires:` 行。"""
    inner = base_indent + "  "  # requires 下字段缩进
    rows = [base_indent + "requires:"]

    def flow(vals, quoted=False):
        out = []
        for v in vals:
            if quoted or re.search(r"[\$\{\}\[\],]", v):
                out.append("'" + v.replace("'", "''") + "'")
            else:
                out.append(v)
        return "[" + ", ".join(out) + "]"

    if spec.get("bins"):
        rows.append(inner + "bins: " + flow(spec["bins"]))
    if spec.get("libs"):
        rows.append(inner + "libs: " + flow(spec["libs"]))
    if spec.get("env"):
        rows.append(inner + "env: " + flow(spec["env"]))
    if spec.get("path_vars"):
        rows.append(inner + "path-vars: " + flow(spec["path_vars"], quoted=True))
    rows.append(inner + "scope: " + spec["scope"])
    rows.append(inner + "declared-by: " + DECLARED_BY)
    return "\n".join(rows)


def inject(text, spec):
    """把 metadata.requires 注入 frontmatter；返回新文本或 None（无法处理）。"""
    parts = split_frontmatter(text)
    if parts is None:
        return None
    fm, body, s, e = parts
    fm_lines = fm.split("\n")

    meta_idx = None
    for i, line in enumerate(fm_lines):
        if re.match(r"^metadata\s*:", line):
            meta_idx = i
            break

    if meta_idx is None:
        # case A: 无 metadata -> frontmatter 末尾追加完整 metadata 块
        block = "metadata:\n" + build_requires_block(spec, base_indent="  ")
        # 去掉 fm 尾部空行，追加
        while fm_lines and fm_lines[-1].strip() == "":
            fm_lines.pop()
        new_fm = "\n".join(fm_lines) + "\n" + block
    else:
        # case B: 已有 metadata -> 在 metadata 块末尾插入 requires
        end = len(fm_lines)
        for j in range(meta_idx + 1, len(fm_lines)):
            line = fm_lines[j]
            if line.strip() != "" and not line[0].isspace():
                end = j
                break
        block = build_requires_block(spec, base_indent="  ")
        # 若 metadata 块末非空且无空行，直接在其后插；保持块内整洁
        new_lines = fm_lines[:end]
        if new_lines and new_lines[-1].strip() != "":
            pass
        new_lines = new_lines + block.split("\n") + fm_lines[end:]
        new_fm = "\n".join(new_lines)

    return text[:s] + new_fm + text[e:]


def read_skill_md(path):
    raw = open(path, "rb").read()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    enc = "utf-8-sig" if has_bom else "utf-8"
    text = raw.decode(enc, errors="replace")
    crlf = "\r\n" in text
    norm = text.replace("\r\n", "\n")
    return norm, has_bom, crlf


def write_skill_md(path, text, has_bom, crlf):
    if crlf:
        text = text.replace("\n", "\r\n")
    enc = "utf-8-sig" if has_bom else "utf-8"
    with open(path, "wb") as f:
        f.write(text.encode(enc))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--map", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "skill_requirements_map.json"))
    ap.add_argument("--roots", nargs="*", default=DEFAULT_ROOTS)
    args = ap.parse_args()

    req_map = json.load(open(args.map, encoding="utf-8"))
    stats = {"declared": 0, "missing": 0, "not_in_map": 0, "preexisting": 0,
             "fixed": 0, "skipped": 0, "error": 0, "no_frontmatter": 0}

    for root in args.roots:
        for d, name in collect_skill_dirs(root):
            lib = lib_of(d)
            key = "%s:%s" % (lib, name)
            spec = req_map.get(key)
            smd = os.path.join(d, "SKILL.md")
            rec = {"lib": lib, "name": name, "path": smd, "in_map": spec is not None}

            norm, has_bom, crlf = read_skill_md(smd)
            parts = split_frontmatter(norm)
            if parts is None:
                rec["status"] = "no_frontmatter"
                stats["no_frontmatter"] += 1
                sys.stdout.write(json.dumps(rec, ensure_ascii=False) + "\n")
                continue
            fm = parts[0]
            marked = bool(MARK_RE.search(fm))
            pre_req = has_own_requires(fm)

            if marked:
                rec["status"] = "declared"
                stats["declared"] += 1
            elif spec is None:
                rec["status"] = "not_in_map"
                stats["not_in_map"] += 1
            elif pre_req:
                rec["status"] = "preexisting"
                stats["preexisting"] += 1
            else:
                rec["status"] = "missing"
                stats["missing"] += 1

            if args.fix and rec["status"] == "missing":
                try:
                    new_text = inject(norm, spec)
                    if new_text is None:
                        rec["fix"] = "error-no-frontmatter"
                        stats["error"] += 1
                    else:
                        write_skill_md(smd, new_text, has_bom, crlf)
                        rec["fix"] = "fixed"
                        stats["fixed"] += 1
                except Exception as ex:
                    rec["fix"] = "error: %s" % ex
                    stats["error"] += 1
            elif args.fix:
                rec["fix"] = "skipped"
                stats["skipped"] += 1

            sys.stdout.write(json.dumps(rec, ensure_ascii=False) + "\n")

    sys.stderr.write(json.dumps(stats, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
