#!/usr/bin/env python3
"""Apply Skillcraft's non-voting behavioral evaluation verdict policy."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


class InvalidEvaluation(ValueError):
    """The evaluation packet cannot be aggregated safely."""


def _require_list(value: Any, name: str) -> list[Any]:
    if not isinstance(value, list):
        raise InvalidEvaluation(f"{name} must be an array")
    return value


def _require_nonempty_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidEvaluation(f"{name} must be a non-empty string")
    return value


def _unique_strings(value: Any, name: str, *, nonempty: bool = False) -> list[str]:
    items = _require_list(value, name)
    if nonempty and not items:
        raise InvalidEvaluation(f"{name} must not be empty")
    result = [_require_nonempty_string(item, f"{name}[]") for item in items]
    if len(result) != len(set(result)):
        raise InvalidEvaluation(f"{name} must contain unique values")
    return result


def _index_assessments(
    packet: dict[str, Any],
    field: str,
    id_field: str,
    allowed_statuses: set[str],
) -> dict[str, list[dict[str, Any]]]:
    indexed: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, assessment in enumerate(_require_list(packet.get(field), field)):
        if not isinstance(assessment, dict):
            raise InvalidEvaluation(f"{field}[{index}] must be an object")
        item_id = _require_nonempty_string(assessment.get(id_field), f"{field}[{index}].{id_field}")
        status = assessment.get("status")
        if status not in allowed_statuses:
            raise InvalidEvaluation(f"{field}[{index}].status is invalid: {status!r}")
        _require_nonempty_string(assessment.get("evaluator_id"), f"{field}[{index}].evaluator_id")
        evidence_ids = _require_list(assessment.get("evidence_ids"), f"{field}[{index}].evidence_ids")
        for evidence_index, evidence_id in enumerate(evidence_ids):
            _require_nonempty_string(evidence_id, f"{field}[{index}].evidence_ids[{evidence_index}]")
        if not evidence_ids:
            raise InvalidEvaluation(f"{field}[{index}] must cite evidence, including for an indeterminate result")
        indexed[item_id].append(assessment)
    return indexed


def aggregate(packet: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(packet, dict):
        raise InvalidEvaluation("evaluation packet must be an object")
    policy = packet.get("policy")
    if not isinstance(policy, dict):
        raise InvalidEvaluation("policy must be an object")

    required_ids = _unique_strings(
        policy.get("required_criterion_ids"),
        "policy.required_criterion_ids",
        nonempty=True,
    )
    invariant_ids = _unique_strings(
        policy.get("hard_invariant_ids"),
        "policy.hard_invariant_ids",
    )
    criteria = _index_assessments(
        packet,
        "criteria",
        "criterion_id",
        {"met", "unmet", "insufficient_evidence"},
    )
    invariants = _index_assessments(
        packet,
        "hard_invariants",
        "invariant_id",
        {"preserved", "violated", "indeterminate"},
    )
    trade_offs = _require_list(packet.get("trade_offs"), "trade_offs")

    blockers: list[dict[str, str]] = []
    gaps: list[dict[str, str]] = []

    for invariant_id in invariant_ids:
        assessments = invariants.get(invariant_id, [])
        if any(item["status"] == "violated" for item in assessments):
            blockers.append({"kind": "hard_invariant", "id": invariant_id, "reason": "demonstrated violation"})
        elif not assessments:
            gaps.append({"kind": "hard_invariant", "id": invariant_id, "reason": "missing assessment"})
        elif any(item["status"] == "indeterminate" for item in assessments):
            gaps.append({"kind": "hard_invariant", "id": invariant_id, "reason": "indeterminate assessment"})

    for criterion_id in required_ids:
        assessments = criteria.get(criterion_id, [])
        if any(item["status"] == "unmet" for item in assessments):
            blockers.append({"kind": "required_criterion", "id": criterion_id, "reason": "unmet"})
        elif not assessments:
            gaps.append({"kind": "required_criterion", "id": criterion_id, "reason": "missing assessment"})
        elif any(item["status"] == "insufficient_evidence" for item in assessments):
            gaps.append({"kind": "required_criterion", "id": criterion_id, "reason": "insufficient evidence"})

    verdict = "fail" if blockers else "incomplete" if gaps else "pass"
    return {
        "verdict": verdict,
        "blocking_findings": blockers,
        "evidence_gaps": gaps,
        "nonblocking_trade_offs": trade_offs,
        "policy": "hard violations and unmet requirements override favourable assessments; no majority vote",
    }


def _read_packet(path: str | None) -> dict[str, Any]:
    if path is None or path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evaluation", nargs="?", default="-", help="evaluation JSON path, or - for stdin")
    args = parser.parse_args()
    try:
        result = aggregate(_read_packet(args.evaluation))
    except (InvalidEvaluation, json.JSONDecodeError, OSError) as error:
        print(f"invalid evaluation: {error}", file=sys.stderr)
        return 2
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
