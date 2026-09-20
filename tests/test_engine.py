import unittest

from rsm import AuditProfile, run_audit
from rsm.metrics import (
    compression_length_delta,
    sequence_distance,
    token_jaccard_distance,
)


METRICS = {
    "sequence": sequence_distance,
    "tokens": token_jaccard_distance,
}


class TestRSM(unittest.TestCase):
    def test_identity_is_stable_even_for_false_claim(self):
        false_claim = "The Sun orbits Earth once per day."
        result = run_audit(false_claim, lambda x: x, METRICS, steps=6)
        self.assertEqual(result.classification, "C1")
        self.assertEqual(result.peak_score, 0.0)
        self.assertEqual(result.cycle_periods, (1,))

    def test_progressive_loss_diverges(self):
        def erode(text: str) -> str:
            keep = max(0, len(text) // 2)
            return text[:keep]

        result = run_audit(
            "recursive structure should survive declared transforms",
            erode,
            METRICS,
            steps=6,
        )
        self.assertEqual(result.classification, "C3")
        self.assertGreater(result.peak_score, 0.35)

    def test_reversal_exposes_two_cycle(self):
        result = run_audit(
            "This sentence is false.",
            lambda x: x[::-1],
            {"sequence": sequence_distance},
            steps=6,
        )
        self.assertEqual(result.cycle_periods, (2,))
        self.assertEqual(result.mean_scores[0], 0.0)
        self.assertEqual(result.mean_scores[2], 0.0)

    def test_token_jaccard_ignores_order(self):
        self.assertEqual(token_jaccard_distance("alpha beta", "beta alpha"), 0.0)

    def test_compression_delta_is_bounded(self):
        value = compression_length_delta("aaaaa", "completely different text")
        self.assertGreaterEqual(value, 0.0)
        self.assertLessEqual(value, 1.0)

    def test_weights_must_match_metrics(self):
        with self.assertRaises(ValueError):
            run_audit(
                "x",
                lambda x: x,
                METRICS,
                profile=AuditProfile(weights={"sequence": 1.0}),
            )


if __name__ == "__main__":
    unittest.main()
