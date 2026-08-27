#!/usr/bin/env python3
"""
Siege OS v1.0 — zero-budget operator system.

Decisions must survive a falsification check before they enter a
90-minute execution block. No motivational fluff in the trust path.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import List

BLOCK_MINUTES = 90


@dataclass(frozen=True)
class Decision:
    statement: str
    success_metric: str
    kill_condition: str
    evidence: str


@dataclass(frozen=True)
class Block:
    title: str
    minutes: int
    decision: Decision
    status: str


def falsify(decision: Decision) -> List[str]:
    defects: List[str] = []
    if len(decision.statement.strip()) < 12:
        defects.append("statement too vague")
    if not decision.success_metric.strip():
        defects.append("missing success metric")
    if not decision.kill_condition.strip():
        defects.append("missing kill condition")
    if not decision.evidence.strip():
        defects.append("missing evidence")
    return defects


def schedule(title: str, decision: Decision) -> Block:
    defects = falsify(decision)
    if defects:
        return Block(title=title, minutes=0, decision=decision, status="REJECTED:" + ",".join(defects))
    return Block(title=title, minutes=BLOCK_MINUTES, decision=decision, status="ARMED")


def demo() -> None:
    good = Decision(
        statement="Ship GridPulse receipt tests and open the health issue",
        success_metric="CI green on jabrahns-source/GridPulse",
        kill_condition="If tests cannot run on Python 3.12 without extra deps",
        evidence="receipt.py + tests/test_receipt.py exist",
    )
    print(json.dumps(asdict(schedule("block-1", good)), indent=2))


if __name__ == "__main__":
    demo()
