import copy
import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "aggregate_behavioral_verdict.py"
SPEC = importlib.util.spec_from_file_location("aggregate_behavioral_verdict", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def packet():
    return {
        "policy": {
            "required_criterion_ids": ["criterion-login"],
            "hard_invariant_ids": ["invariant-authz"],
        },
        "criteria": [
            {
                "criterion_id": "criterion-login",
                "evaluator_id": "task-completion",
                "status": "met",
                "evidence_ids": ["e-login"],
            }
        ],
        "hard_invariants": [
            {
                "invariant_id": "invariant-authz",
                "evaluator_id": "security",
                "status": "preserved",
                "evidence_ids": ["e-authz"],
            }
        ],
        "trade_offs": [],
    }


class AggregateVerdictTests(unittest.TestCase):
    def test_passes_when_all_required_assessments_are_satisfied(self):
        self.assertEqual(MODULE.aggregate(packet())["verdict"], "pass")

    def test_one_demonstrated_invariant_violation_overrides_preserving_votes(self):
        data = packet()
        data["hard_invariants"].extend(
            [
                {
                    "invariant_id": "invariant-authz",
                    "evaluator_id": "architecture",
                    "status": "preserved",
                    "evidence_ids": ["e-arch"],
                },
                {
                    "invariant_id": "invariant-authz",
                    "evaluator_id": "security-2",
                    "status": "violated",
                    "evidence_ids": ["e-bypass"],
                },
            ]
        )
        result = MODULE.aggregate(data)
        self.assertEqual(result["verdict"], "fail")
        self.assertEqual(result["blocking_findings"][0]["id"], "invariant-authz")

    def test_unmet_required_criterion_overrides_met_assessment(self):
        data = packet()
        data["criteria"].append(
            {
                "criterion_id": "criterion-login",
                "evaluator_id": "task-completion-2",
                "status": "unmet",
                "evidence_ids": ["e-missing-flow"],
            }
        )
        self.assertEqual(MODULE.aggregate(data)["verdict"], "fail")

    def test_blocker_takes_precedence_over_evidence_gap(self):
        data = packet()
        data["criteria"] = []
        data["hard_invariants"][0]["status"] = "violated"
        result = MODULE.aggregate(data)
        self.assertEqual(result["verdict"], "fail")
        self.assertEqual(result["blocking_findings"][0]["id"], "invariant-authz")
        self.assertEqual(result["evidence_gaps"][0]["id"], "criterion-login")

    def test_insufficient_or_missing_required_assessment_is_incomplete(self):
        insufficient = packet()
        insufficient["criteria"][0]["status"] = "insufficient_evidence"
        insufficient["criteria"][0]["evidence_ids"] = ["e-indeterminate"]
        self.assertEqual(MODULE.aggregate(insufficient)["verdict"], "incomplete")

        missing = packet()
        missing["hard_invariants"] = []
        self.assertEqual(MODULE.aggregate(missing)["verdict"], "incomplete")

    def test_trade_offs_are_reported_but_do_not_change_the_verdict(self):
        data = packet()
        data["trade_offs"] = [{"id": "t-1", "summary": "slower response"}]
        result = MODULE.aggregate(data)
        self.assertEqual(result["verdict"], "pass")
        self.assertEqual(result["nonblocking_trade_offs"], data["trade_offs"])

    def test_every_assessment_requires_evidence(self):
        data = packet()
        data["hard_invariants"][0] = {
            "invariant_id": "invariant-authz",
            "evaluator_id": "security",
            "status": "violated",
            "evidence_ids": [],
        }
        with self.assertRaises(MODULE.InvalidEvaluation):
            MODULE.aggregate(data)

        data = packet()
        data["criteria"][0]["evidence_ids"] = []
        with self.assertRaises(MODULE.InvalidEvaluation):
            MODULE.aggregate(data)

    def test_input_is_not_mutated(self):
        data = packet()
        original = copy.deepcopy(data)
        MODULE.aggregate(data)
        self.assertEqual(data, original)


if __name__ == "__main__":
    unittest.main()
