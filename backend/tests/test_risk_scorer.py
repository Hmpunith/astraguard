"""
Unit tests for backend/app/risk_scorer.py

Covers all four risk levels (LOW, MEDIUM, HIGH, CRITICAL) and validates
scoring behavior for different object-type combinations.
"""
import sys
import os

# Allow importing app modules without installing the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from app.risk_scorer import score_risk
from app.models import RiskLevel


# ---------------------------------------------------------------------------
# LOW risk scenarios
# ---------------------------------------------------------------------------

class TestLowRisk:
    def test_large_miss_distance_returns_low(self):
        """A very large miss distance with slow relative velocity is LOW risk."""
        score, level = score_risk(
            miss_distance_km=100.0,
            relative_velocity_km_s=1.0,
            primary_type="PAYLOAD",
            secondary_type="PAYLOAD",
        )
        assert level == RiskLevel.LOW
        assert score < 25.0

    def test_score_below_25_for_safe_approach(self):
        """Score must be numerically below 25 for a safe conjunction."""
        score, level = score_risk(
            miss_distance_km=50.0,
            relative_velocity_km_s=5.0,
            primary_type="DEBRIS",
            secondary_type="DEBRIS",
        )
        assert level == RiskLevel.LOW
        assert 0.0 <= score < 25.0

    def test_low_velocity_reduces_risk(self):
        """Slow relative velocity should keep risk score low even at moderate distance."""
        score, level = score_risk(
            miss_distance_km=30.0,
            relative_velocity_km_s=0.5,
            primary_type="PAYLOAD",
            secondary_type="ROCKET_BODY",
        )
        assert level == RiskLevel.LOW


# ---------------------------------------------------------------------------
# MEDIUM risk scenarios
# ---------------------------------------------------------------------------

class TestMediumRisk:
    def test_moderate_distance_moderate_velocity(self):
        """A mid-range miss distance with moderate velocity should be MEDIUM."""
        score, level = score_risk(
            miss_distance_km=10.0,
            relative_velocity_km_s=8.0,
            primary_type="PAYLOAD",
            secondary_type="DEBRIS",
        )
        assert level == RiskLevel.MEDIUM
        assert 25.0 <= score < 50.0

    def test_score_in_medium_band(self):
        """Score must fall within [25, 50) for MEDIUM risk."""
        score, level = score_risk(
            miss_distance_km=8.0,
            relative_velocity_km_s=6.0,
            primary_type="PAYLOAD",
            secondary_type="DEBRIS",
        )
        assert level == RiskLevel.MEDIUM
        assert 25.0 <= score < 50.0

    def test_debris_vs_debris_reduces_score(self):
        """Two small debris objects carry a lower combined size factor, potentially MEDIUM."""
        score, level = score_risk(
            miss_distance_km=5.0,
            relative_velocity_km_s=7.0,
            primary_type="DEBRIS",
            secondary_type="DEBRIS",
        )
        # Score should be lower than PAYLOAD/PAYLOAD at the same distance
        score_payload, _ = score_risk(
            miss_distance_km=5.0,
            relative_velocity_km_s=7.0,
            primary_type="PAYLOAD",
            secondary_type="PAYLOAD",
        )
        assert score < score_payload


# ---------------------------------------------------------------------------
# HIGH risk scenarios
# ---------------------------------------------------------------------------

class TestHighRisk:
    def test_close_approach_high_velocity(self):
        """A 4 km miss distance with moderate-high velocity is HIGH risk."""
        score, level = score_risk(
            miss_distance_km=4.0,
            relative_velocity_km_s=8.0,
            primary_type="PAYLOAD",
            secondary_type="DEBRIS",
        )
        assert level == RiskLevel.HIGH
        assert 50.0 <= score < 75.0

    def test_score_in_high_band(self):
        """Score must fall within [50, 75) for HIGH risk."""
        score, level = score_risk(
            miss_distance_km=3.5,
            relative_velocity_km_s=12.0,
            primary_type="PAYLOAD",
            secondary_type="ROCKET_BODY",
        )
        assert level == RiskLevel.HIGH
        assert 50.0 <= score < 75.0

    def test_payload_vs_payload_raises_score(self):
        """Two active payloads have a higher combined size factor, pushing towards HIGH."""
        score_pp, level_pp = score_risk(
            miss_distance_km=3.0,
            relative_velocity_km_s=14.5,
            primary_type="PAYLOAD",
            secondary_type="PAYLOAD",
        )
        score_dd, _ = score_risk(
            miss_distance_km=3.0,
            relative_velocity_km_s=14.5,
            primary_type="DEBRIS",
            secondary_type="DEBRIS",
        )
        # PAYLOAD/PAYLOAD should score at least as high as DEBRIS/DEBRIS
        assert score_pp >= score_dd


# ---------------------------------------------------------------------------
# CRITICAL risk scenarios
# ---------------------------------------------------------------------------

class TestCriticalRisk:
    def test_very_close_approach_is_critical(self):
        """Sub-km miss distance with very high velocity must be CRITICAL."""
        score, level = score_risk(
            miss_distance_km=0.2,
            relative_velocity_km_s=15.0,
            primary_type="PAYLOAD",
            secondary_type="DEBRIS",
        )
        assert level == RiskLevel.CRITICAL
        assert score >= 75.0

    def test_zero_miss_distance_is_critical(self):
        """Miss distance of exactly zero (predicted collision) must be CRITICAL."""
        score, level = score_risk(
            miss_distance_km=0.0,
            relative_velocity_km_s=10.0,
            primary_type="PAYLOAD",
            secondary_type="ROCKET_BODY",
        )
        assert level == RiskLevel.CRITICAL
        assert score >= 75.0

    def test_score_capped_at_100(self):
        """Score must never exceed 100.0 even for worst-case inputs."""
        score, level = score_risk(
            miss_distance_km=0.0,
            relative_velocity_km_s=20.0,
            primary_type="PAYLOAD",
            secondary_type="PAYLOAD",
        )
        assert score <= 100.0
        assert level == RiskLevel.CRITICAL

    def test_score_never_negative(self):
        """Score must never be negative for any input combination."""
        score, level = score_risk(
            miss_distance_km=999.0,
            relative_velocity_km_s=0.0,
            primary_type="DEBRIS",
            secondary_type="DEBRIS",
        )
        assert score >= 0.0


# ---------------------------------------------------------------------------
# Edge cases and invariants
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_unknown_object_type_defaults_gracefully(self):
        """Unknown object types should not raise exceptions; treated as DEBRIS weight."""
        score, level = score_risk(
            miss_distance_km=5.0,
            relative_velocity_km_s=8.0,
            primary_type="UNKNOWN",
            secondary_type="UNKNOWN",
        )
        assert isinstance(score, float)
        assert isinstance(level, RiskLevel)

    def test_score_monotonically_increases_as_distance_decreases(self):
        """Score should increase as miss distance decreases (all else equal)."""
        distances = [50.0, 20.0, 10.0, 5.0, 2.0, 0.5]
        scores = [
            score_risk(d, 10.0, "PAYLOAD", "DEBRIS")[0]
            for d in distances
        ]
        for i in range(len(scores) - 1):
            assert scores[i] < scores[i + 1], (
                f"Score did not increase as distance decreased: "
                f"{distances[i]} km → {scores[i]:.2f}, "
                f"{distances[i+1]} km → {scores[i+1]:.2f}"
            )

    def test_score_increases_with_velocity(self):
        """Higher relative velocity should produce a higher score (all else equal)."""
        score_slow, _ = score_risk(2.0, 2.0, "PAYLOAD", "PAYLOAD")
        score_fast, _ = score_risk(2.0, 15.0, "PAYLOAD", "PAYLOAD")
        assert score_fast > score_slow

    def test_return_types(self):
        """score_risk must return (float, RiskLevel) tuple."""
        result = score_risk(10.0, 10.0, "PAYLOAD", "DEBRIS")
        assert isinstance(result, tuple)
        assert len(result) == 2
        score, level = result
        assert isinstance(score, float)
        assert isinstance(level, RiskLevel)

    @pytest.mark.parametrize("obj_type", ["PAYLOAD", "ROCKET_BODY", "DEBRIS"])
    def test_all_object_types_handled(self, obj_type):
        """All known object type strings should produce valid scores."""
        score, level = score_risk(5.0, 10.0, obj_type, obj_type)
        assert 0.0 <= score <= 100.0
        assert level in list(RiskLevel)
