"""Deterministic educational readiness scoring."""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from open_mic_lab.domain.enums import Difficulty
from open_mic_lab.domain.performance import PerformanceVersion
from open_mic_lab.domain.practice import PracticeSession

DIFFICULTY_MULTIPLIER = {
    Difficulty.SIMPLE: Decimal("1.00"),
    Difficulty.MODERATE: Decimal("0.92"),
    Difficulty.CHALLENGING: Decimal("0.82"),
}


@dataclass(frozen=True, slots=True)
class ReadinessResult:
    """Readiness score, category, and explanatory breakdown."""

    score: Decimal
    category: str
    breakdown: tuple[str, ...]


def calculate_readiness(
    version: PerformanceVersion, sessions: tuple[PracticeSession, ...] = ()
) -> ReadinessResult:
    """Calculate a 0-100 educational comparison score.

    Formula: weighted skill average on a 0-10 scale (memory 30%, vocal 25%,
    accompaniment 25%, recovery 20%) multiplied by ten, then adjusted by an
    arrangement difficulty multiplier. If matching practice sessions are supplied,
    add up to five points for at least 90 recent-like minutes and subtract up to
    five points for mistake density. Dates are not interpreted in milestone 1;
    supplied sessions are treated as the learner's chosen evidence window.
    """
    skill = (
        version.memory_confidence * Decimal("0.30")
        + version.vocal_comfort * Decimal("0.25")
        + version.accompaniment_stability * Decimal("0.25")
        + version.recovery_confidence * Decimal("0.20")
    )
    base = skill * Decimal("10")
    adjusted = base * DIFFICULTY_MULTIPLIER[version.arrangement_difficulty]
    base_text = base.quantize(Decimal("0.1"))
    multiplier = DIFFICULTY_MULTIPLIER[version.arrangement_difficulty]
    breakdown = [
        f"Skill base: {base_text}/100 from memory, vocal, accompaniment, and recovery.",
        f"Difficulty adjustment: {version.arrangement_difficulty.value} x {multiplier}.",
    ]
    matching = tuple(s for s in sessions if s.performance_version_identifier == version.identifier)
    if matching:
        minutes = sum(s.duration_minutes for s in matching)
        mistakes = sum(s.mistake_count for s in matching)
        practice_bonus = min(Decimal("5"), Decimal(minutes) / Decimal("18"))
        mistake_penalty = min(Decimal("5"), Decimal(mistakes) / Decimal("4"))
        adjusted = adjusted + practice_bonus - mistake_penalty
        breakdown.append(
            f"Practice evidence: +{practice_bonus.quantize(Decimal('0.1'))} for {minutes} minutes."
        )
        penalty = mistake_penalty.quantize(Decimal("0.1"))
        breakdown.append(f"Mistake-density caution: -{penalty} for {mistakes} mistakes.")
    score = max(Decimal("0"), min(Decimal("100"), adjusted)).quantize(
        Decimal("0.1"), rounding=ROUND_HALF_UP
    )
    category = _category(score)
    breakdown.append(
        f"Recommendation: {category}; use this as a comparison tool, not a prediction."
    )
    return ReadinessResult(score=score, category=category, breakdown=tuple(breakdown))


def _category(score: Decimal) -> str:
    if score < Decimal("45"):
        return "not ready"
    if score < Decimal("70"):
        return "developing"
    if score < Decimal("85"):
        return "nearly ready"
    return "performance ready"
