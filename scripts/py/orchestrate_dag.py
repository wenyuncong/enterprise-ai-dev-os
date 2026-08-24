#!/usr/bin/env python3
"""DAG orchestrator: validate a task DAG and emit a parallel execution plan.

Turns ai-multi-agent-orchestration's dependency matrix into a runnable plan:
validate node ids and edges, detect cycles, topologically sort into parallel
layers, and print which nodes can run concurrently. This is a planner, not a
dispatcher — actual fan-out is the host runtime's job (subagents / jobs).

Usage:
  orchestrate_dag.py --dag docs/_templates/全项目总控/task_dag.json [--json]
Exit code: 1 on invalid DAG (unknown dependency or cycle), 0 otherwise.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict, deque
from pathlib import Path


def load_dag(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def plan(dag: dict) -> list[list[dict]]:
    nodes = dag.get("nodes", [])
    ids = {n["id"] for n in nodes}
    if len(ids) != len(nodes):
        raise ValueError("duplicate node id")
    for n in nodes:
        for dep in n.get("depends", []):
            if dep not in ids:
                raise ValueError(f"node '{n['id']}' depends on unknown node '{dep}'")

    # Kahn topological sort into layers.
    indeg = {n["id"]: len(n.get("depends", [])) for n in nodes}
    dependents = defaultdict(list)
    for n in nodes:
        for dep in n.get("depends", []):
            dependents[dep].append(n["id"])

    queue = deque([n["id"] for n in nodes if indeg[n["id"]] == 0])
    layers = []
    while queue:
        layer = []
        for _ in range(len(queue)):
            nid = queue.popleft()
            node = next(n for n in nodes if n["id"] == nid)
            layer.append({"id": nid, "name": node.get("name", nid),
                          "depends": node.get("depends", [])})
            for child in dependents[nid]:
                indeg[child] -= 1
                if indeg[child] == 0:
                    queue.append(child)
        layers.append(layer)

    if sum(len(l) for l in layers) != len(nodes):
        raise ValueError("cycle detected in task DAG")
    return layers


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a task DAG and emit a parallel plan.")
    parser.add_argument("--dag", required=True, help="Path to task_dag.json")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    dag_path = Path(args.dag).resolve()
    try:
        dag = load_dag(dag_path)
        layers = plan(dag)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1

    out = {
        "dag": str(dag_path),
        "nodes": len(dag.get("nodes", [])),
        "layers": len(layers),
        "plan": [{"layer": i + 1, "parallel": [n["id"] for n in layer],
                  "names": [n["name"] for n in layer]} for i, layer in enumerate(layers)],
        "contracts": dag.get("contracts", []),
    }
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"Task DAG: {out['nodes']} nodes, {out['layers']} sequential layers")
        for l in out["plan"]:
            parallel = " | ".join(l["names"])
            print(f"  Layer {l['layer']} (parallel): {parallel}")
        if out["contracts"]:
            print(f"  Contracts: {len(out['contracts'])} integration point(s) defined")
    return 0


if __name__ == "__main__":
    sys.exit(main())
