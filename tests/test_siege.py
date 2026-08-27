import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from siege import BLOCK_MINUTES, Decision, falsify, schedule  # noqa: E402


def test_reject_empty_metric():
    d = Decision("ship the thing now", "", "stop if broken", "none")
    assert "missing success metric" in falsify(d)
    assert schedule("x", d).status.startswith("REJECTED")


def test_arm_valid_decision():
    d = Decision(
        statement="Open health-audit issues on core repos",
        success_metric="issue exists on kerna-ledger",
        kill_condition="stop if GitHub write fails",
        evidence="audit tree already fetched",
    )
    b = schedule("health-audit", d)
    assert b.status == "ARMED"
    assert b.minutes == BLOCK_MINUTES
