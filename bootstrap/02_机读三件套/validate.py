#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""机读三件套校验：用 JSON Schema 校验 project-profile / task-routing / gates 及其示例。

- 本机装有 jsonschema 时使用完整校验；
- 未安装时退化为轻量结构校验（required / enum / type / items / additionalProperties），
  仍然能挡住"漏字段、枚举写错、结构错位"这类最常见问题。

用法（在 bootstrap/02_机读三件套 目录内或任意位置）：
  py validate.py
  py validate.py --dir .

退出码：0 = 全部通过；1 = 有失败项。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import jsonschema  # type: ignore
    HAS_JSONSCHEMA = True
except ImportError:  # pragma: no cover
    HAS_JSONSCHEMA = False


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def light_validate(instance, schema: dict, path: str = "$") -> list[str]:
    """轻量结构校验：只覆盖模板真正会用到的关键字。"""
    errors: list[str] = []
    if not isinstance(schema, dict):
        return errors

    stype = schema.get("type")
    if stype == "object":
        if not isinstance(instance, dict):
            return [f"{path}: 期望 object，实际 {type(instance).__name__}"]
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}: 缺少必填字段 {key}")
        props = schema.get("properties", {})
        for key, value in instance.items():
            if key in props:
                errors.extend(light_validate(value, props[key], f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: 未声明字段 {key}")
    elif stype == "array":
        if not isinstance(instance, list):
            return [f"{path}: 期望 array，实际 {type(instance).__name__}"]
        items = schema.get("items", {})
        for i, item in enumerate(instance):
            errors.extend(light_validate(item, items, f"{path}[{i}]"))
    elif stype == "string":
        if not isinstance(instance, str):
            errors.append(f"{path}: 期望 string，实际 {type(instance).__name__}")
    elif stype == "integer":
        if not isinstance(instance, int) or isinstance(instance, bool):
            errors.append(f"{path}: 期望 integer，实际 {type(instance).__name__}")
    elif stype == "boolean":
        if not isinstance(instance, bool):
            errors.append(f"{path}: 期望 boolean，实际 {type(instance).__name__}")

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {instance!r} 不在允许集合 {schema['enum']}")

    # definitions / $ref 仅在 jsonschema 可用时处理
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description="校验机读三件套")
    ap.add_argument("--dir", default=str(Path(__file__).resolve().parent))
    args = ap.parse_args()
    root = Path(args.dir).resolve()

    mode = "jsonschema 完整校验" if HAS_JSONSCHEMA else "轻量结构校验（未安装 jsonschema）"
    print(f"校验模式：{mode}")
    print(f"根目录：{root.name}/\n")

    targets = [
        ("project-profile.schema.json", ["examples"]),
        ("task-routing.schema.json", ["examples"]),
        ("gates.schema.json", ["examples"]),
    ]

    total = 0
    failed = 0
    for schema_name, _ in targets:
        schema_path = root / schema_name
        if not schema_path.exists():
            print(f"[FAIL] 缺少 Schema：{schema_name}")
            failed += 1
            continue
        schema = load(schema_path)
        print(f"[Schema] {schema_name} —— {schema.get('title', '')}")

        stem = schema_name.split(".")[0]
        for instance_path in sorted((root / "examples").rglob("*.json")):
            instance = load(instance_path)
            # 用文件名前缀把示例归到对应 schema
            if not instance_path.name.startswith(stem.replace("project-profile", "project-profile")
                                                 .replace("task-routing", "task-routing")
                                                 .replace("gates", "gates")):
                continue
            total += 1
            rel = instance_path.relative_to(root).as_posix()
            if HAS_JSONSCHEMA:
                try:
                    jsonschema.validate(instance, schema)
                    print(f"  [OK]   {rel}")
                except jsonschema.ValidationError as exc:  # type: ignore
                    failed += 1
                    print(f"  [FAIL] {rel}: {exc.message} @ {list(exc.absolute_path)}")
            else:
                errors = light_validate(instance, schema)
                if errors:
                    failed += 1
                    print(f"  [FAIL] {rel}")
                    for e in errors[:8]:
                        print(f"         - {e}")
                else:
                    print(f"  [OK]   {rel}")
        print()

    print(f"示例文件校验：{total - failed}/{total} 通过")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
