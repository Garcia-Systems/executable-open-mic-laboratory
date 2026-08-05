"""Transparent Chapter 1 song-suitability calculations."""

# Evidence basis for scoring and recommendation services.
#
# Purpose: provide deterministic educational comparisons for repertoire,
# practice, stagecraft, audio workflow, audience scenarios, recovery,
# improvisation, and reflection.
# Inputs: typed domain objects and bounded scenario data in the repository.
# Outputs: scores, categories, warnings, recommendations, and explanation text.
# Evidence Basis: music education, performance psychology, feedback research,
# self-regulated learning, cognitive-load theory, live-sound practice, and
# simulation-based learning motivate the concepts represented here.
# Repository Contribution: exact weights, thresholds, and formula structures are
# original educational heuristics designed for transparent experimentation.
# Limitations: outputs are non-predictive learning aids. They are not validated
# measurements of artistic worth, audience response, technical safety, or future
# performance success.

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from open_mic_lab.domain import (
    Difficulty,
    EnergyLevel,
    PerformanceRole,
    PerformanceVersion,
    Repertoire,
    SongSelectionProfile,
    Venue,
)
from open_mic_lab.services.readiness_service import ReadinessResult, calculate_readiness

DEFAULT_WEIGHTS: dict[str, Decimal] = {
    "vocal": Decimal("0.18"),
    "accompaniment": Decimal("0.12"),
    "readiness": Decimal("0.16"),
    "audience": Decimal("0.10"),
    "connection": Decimal("0.12"),
    "venue": Decimal("0.08"),
    "role": Decimal("0.08"),
    "energy": Decimal("0.07"),
    "flexibility": Decimal("0.05"),
    "preference": Decimal("0.04"),
}
_DIFFICULTY_VALUE = {Difficulty.SIMPLE: 1, Difficulty.MODERATE: 2, Difficulty.CHALLENGING: 3}
_ENERGY_VALUE = {
    EnergyLevel.VERY_LOW: 1,
    EnergyLevel.LOW: 2,
    EnergyLevel.MEDIUM: 3,
    EnergyLevel.HIGH: 4,
    EnergyLevel.VERY_HIGH: 5,
}


@dataclass(frozen=True, slots=True)
class CriterionScore:
    """One suitability criterion with scoring metadata."""

    name: str
    score: Decimal
    weight: Decimal
    available: bool
    explanation: str


@dataclass(frozen=True, slots=True)
class SuitabilityResult:
    """Structured suitability result for one opportunity."""

    version_id: str
    score: Decimal
    criteria: tuple[CriterionScore, ...]
    positive_factors: tuple[str, ...]
    concerns: tuple[str, ...]
    adaptations: tuple[str, ...]
    recommendation: str
    completeness: Decimal
    hard_constraints: tuple[str, ...]
    explanation: str

    @property
    def strongest_factor(self) -> str:
        """Return the strongest available factor explanation."""
        available = [c for c in self.criteria if c.available]
        return (
            max(available, key=lambda c: (c.score, c.weight, c.name)).explanation
            if available
            else "No scored factors."
        )

    @property
    def largest_concern(self) -> str:
        """Return the largest concern or first hard constraint."""
        if self.hard_constraints:
            return self.hard_constraints[0]
        available = [c for c in self.criteria if c.available]
        return (
            min(available, key=lambda c: (c.score, c.name)).explanation
            if available
            else "Missing information limits confidence."
        )


@dataclass(frozen=True, slots=True)
class CandidateComparison:
    """Comparison of multiple candidates for the same profile."""

    results: tuple[SuitabilityResult, ...]
    excluded: tuple[tuple[str, tuple[str, ...]], ...]
    observations: tuple[str, ...]


class SongSuitabilityService:
    """Evaluate and compare songs without declaring artistic truth."""

    def evaluate(
        self,
        version: PerformanceVersion,
        repertoire: Repertoire,
        profile: SongSelectionProfile,
        venue: Venue,
        readiness: ReadinessResult | None = None,
    ) -> SuitabilityResult:
        """Evaluate one performance version with bounded weighted criteria."""
        weights = _validated_weights(profile.weights or DEFAULT_WEIGHTS)
        song = repertoire.get_song(version.song_identifier)
        readiness = readiness or calculate_readiness(version)
        hard = _hard_constraints(version, profile, venue)
        criteria = (
            _vocal(version, profile, weights["vocal"]),
            _accompaniment(version, profile, weights["accompaniment"]),
            CriterionScore(
                "readiness",
                readiness.score,
                weights["readiness"],
                True,
                f"Current readiness is {readiness.score}/100.",
            ),
            _audience(song.estimated_audience_familiarity, profile, venue, weights["audience"]),
            _optional_rating(
                "connection",
                version.performer_connection,
                weights["connection"],
                "Performer connection is learner-supplied and subjective.",
            ),
            _venue(version, profile, venue, weights["venue"]),
            _role(version, profile, weights["role"]),
            _energy(version, profile, weights["energy"]),
            _flexibility(version, profile, weights["flexibility"]),
            _preference(version, profile, weights["preference"]),
        )
        completeness = (
            Decimal(sum(1 for c in criteria if c.available))
            / Decimal(len(criteria))
            * Decimal("100")
        ).quantize(Decimal("0.1"))
        weighted = sum((c.score * c.weight for c in criteria), Decimal("0"))
        total_weight = sum((c.weight for c in criteria), Decimal("0"))
        score = (weighted / total_weight).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        if hard:
            score = min(score, Decimal("44.0"))
        positives = tuple(c.explanation for c in criteria if c.available and c.score >= 75)[:4]
        concerns = (
            tuple(c.explanation for c in criteria if (not c.available) or c.score < 55) + hard
        )
        adaptations = _adaptations(version, profile, hard, concerns)
        rec = _recommendation(score, hard, completeness)
        explanation = (
            f"{rec} Score reflects this opportunity, not song quality. "
            f"Completeness {completeness}%; missing optional data receives a neutral "
            "50 and lowers completeness."
        )
        return SuitabilityResult(
            version.identifier,
            score,
            criteria,
            positives,
            concerns,
            adaptations,
            rec,
            completeness,
            hard,
            explanation,
        )

    def compare(
        self,
        versions: tuple[PerformanceVersion, ...],
        repertoire: Repertoire,
        profile: SongSelectionProfile,
        venue: Venue,
        include_constrained: bool = True,
    ) -> CandidateComparison:
        """Evaluate candidates with stable deterministic sorting and observations."""
        if not versions:
            return CandidateComparison(
                (), (), ("No candidate performance versions were supplied.",)
            )
        results = tuple(self.evaluate(v, repertoire, profile, venue) for v in versions)
        excluded = tuple(
            (r.version_id, r.hard_constraints)
            for r in results
            if r.hard_constraints and not include_constrained
        )
        kept = tuple(r for r in results if include_constrained or not r.hard_constraints)
        ranked = tuple(sorted(kept, key=lambda r: (-r.score, r.version_id)))
        return CandidateComparison(ranked, excluded, _observations(ranked, repertoire))


def _validated_weights(weights: dict[str, Decimal]) -> dict[str, Decimal]:
    missing = set(DEFAULT_WEIGHTS) - set(weights)
    extra = set(weights) - set(DEFAULT_WEIGHTS)
    if missing or extra:
        raise ValueError(
            f"Weights must match criteria. Missing {sorted(missing)}, extra {sorted(extra)}."
        )
    if any(w < 0 for w in weights.values()) or sum(weights.values()) <= 0:
        raise ValueError("Criterion weights must be non-negative with a positive total.")
    total = sum(weights.values())
    return {k: v / total for k, v in weights.items()}


def _rating_score(value: Decimal) -> Decimal:
    return (value * Decimal("10")).quantize(Decimal("0.1"))


def _optional_rating(
    name: str, value: Decimal | None, weight: Decimal, explanation: str
) -> CriterionScore:
    if value is None:
        return CriterionScore(
            name, Decimal("50.0"), weight, False, f"Missing {name} information; neutral score used."
        )
    return CriterionScore(
        name, _rating_score(value), weight, True, f"{explanation} Rating {value}/10."
    )


def _vocal(
    version: PerformanceVersion, profile: SongSelectionProfile, weight: Decimal
) -> CriterionScore:
    if version.required_vocal_range is None or profile.comfortable_vocal_range is None:
        return CriterionScore(
            "vocal",
            Decimal("50.0"),
            weight,
            False,
            "Missing vocal range information; neutral score used.",
        )
    outside = profile.comfortable_vocal_range.outside_distance(version.required_vocal_range)
    score = max(Decimal(0), Decimal(100 - outside * 15))
    return CriterionScore(
        "vocal",
        score,
        weight,
        True,
        f"Vocal range {version.required_vocal_range} is {outside} semitones outside comfort range.",
    )


def _accompaniment(
    version: PerformanceVersion, profile: SongSelectionProfile, weight: Decimal
) -> CriterionScore:
    excess = max(
        0,
        _DIFFICULTY_VALUE[version.arrangement_difficulty]
        - _DIFFICULTY_VALUE[profile.maximum_arrangement_difficulty],
    )
    score = max(Decimal(0), _rating_score(version.accompaniment_stability) - Decimal(excess * 20))
    return CriterionScore(
        "accompaniment",
        score,
        weight,
        True,
        f"Accompaniment stability is {version.accompaniment_stability}/10 "
        f"with {version.arrangement_difficulty.value} difficulty.",
    )


def _audience(
    value: Decimal, profile: SongSelectionProfile, venue: Venue, weight: Decimal
) -> CriterionScore:
    low, high = profile.target_audience_familiarity
    if low <= value <= high:
        score = Decimal("90")
    else:
        score = max(
            Decimal(0), Decimal("90") - min(abs(value - low), abs(value - high)) * Decimal("12")
        )
    if profile.prefer_familiar_songs:
        score = (
            score + _rating_score(value) + _rating_score(venue.audience_familiarity_preference)
        ) / 3
    return CriterionScore(
        "audience",
        score.quantize(Decimal("0.1")),
        weight,
        True,
        f"Audience familiarity estimate is {value}/10 for this venue context.",
    )


def _venue(
    version: PerformanceVersion, profile: SongSelectionProfile, venue: Venue, weight: Decimal
) -> CriterionScore:
    score = Decimal("85")
    if version.primary_instrument.name.startswith("PIANO") and not venue.available_piano:
        score -= 45
    if not venue.amplification_available and version.energy_level in {
        EnergyLevel.HIGH,
        EnergyLevel.VERY_HIGH,
    }:
        score -= 15
    return CriterionScore(
        "venue",
        max(Decimal(0), score),
        weight,
        True,
        f"Venue fit considers instruments, amplification, and slot length at {venue.name}.",
    )


def _role(
    version: PerformanceVersion, profile: SongSelectionProfile, weight: Decimal
) -> CriterionScore:
    match = (
        profile.desired_performance_role in version.supported_roles
        or PerformanceRole.FLEXIBLE in version.supported_roles
    )
    return CriterionScore(
        "role",
        Decimal("90") if match else Decimal("45"),
        weight,
        True,
        f"Role fit for {profile.desired_performance_role.value} is "
        f"{'supported' if match else 'not a primary role'}.",
    )


def _energy(
    version: PerformanceVersion, profile: SongSelectionProfile, weight: Decimal
) -> CriterionScore:
    if profile.desired_energy_level is None:
        return CriterionScore(
            "energy", Decimal("50.0"), weight, False, "Missing desired energy; neutral score used."
        )
    gap = abs(_ENERGY_VALUE[version.energy_level] - _ENERGY_VALUE[profile.desired_energy_level])
    return CriterionScore(
        "energy",
        Decimal(100 - gap * 20),
        weight,
        True,
        f"Energy is {version.energy_level.value}; desired energy is "
        f"{profile.desired_energy_level.value}.",
    )


def _flexibility(
    version: PerformanceVersion, profile: SongSelectionProfile, weight: Decimal
) -> CriterionScore:
    flex = version.arrangement_flexibility
    if flex is None:
        return CriterionScore(
            "flexibility",
            Decimal("50.0"),
            weight,
            False,
            "Missing arrangement flexibility; neutral score used.",
        )
    points = (
        40
        + 15 * int(flex.can_transpose and profile.willingness_to_transpose)
        + 15 * int(flex.can_simplify and profile.willingness_to_simplify)
        + 10 * int(flex.can_shorten)
        + 10 * int(flex.supports_solo)
        + 10 * int(flex.supports_group)
    )
    return CriterionScore(
        "flexibility",
        Decimal(min(100, points)),
        weight,
        True,
        "Arrangement flexibility supports deliberate adaptation experiments.",
    )


def _preference(
    version: PerformanceVersion, profile: SongSelectionProfile, weight: Decimal
) -> CriterionScore:
    score = (
        Decimal("70")
        if profile.preferred_instrument is None
        or version.primary_instrument == profile.preferred_instrument
        else Decimal("45")
    )
    return CriterionScore(
        "preference",
        score,
        weight,
        True,
        f"Primary instrument is {version.primary_instrument.value}.",
    )


def _hard_constraints(
    version: PerformanceVersion, profile: SongSelectionProfile, venue: Venue
) -> tuple[str, ...]:
    hard: list[str] = []
    if not version.is_available:
        hard.append("Performance version is marked unavailable.")
    if (
        profile.available_instruments
        and version.primary_instrument not in profile.available_instruments
    ):
        hard.append(f"Required instrument {version.primary_instrument.value} is unavailable.")
    if version.primary_instrument.name.startswith("PIANO") and not venue.available_piano:
        hard.append("Venue does not provide the required piano.")
    if version.estimated_duration_seconds > profile.slot_duration_minutes * 60:
        hard.append("Song duration exceeds the entire available slot.")
    if (
        profile.strict_vocal_limit
        and version.required_vocal_range
        and not profile.strict_vocal_limit.contains(version.required_vocal_range)
    ):
        hard.append("Required vocal range violates the non-negotiable vocal limit.")
    return tuple(hard)


def _adaptations(
    version: PerformanceVersion,
    profile: SongSelectionProfile,
    hard: tuple[str, ...],
    concerns: tuple[str, ...],
) -> tuple[str, ...]:
    suggestions: list[str] = []
    joined = " ".join(concerns + hard)
    if "semitones outside" in joined and profile.willingness_to_transpose:
        suggestions.append("Experiment with lowering or raising the key before deciding.")
    if "Accompaniment" in joined and profile.willingness_to_simplify:
        suggestions.append("Try a simplified accompaniment pattern and reevaluate stability.")
    if "duration exceeds" in joined:
        suggestions.append("Shorten the introduction or remove an instrumental section.")
    if "instrument" in joined or "piano" in joined:
        suggestions.append("Try a different instrument or save the song for another venue.")
    if version.recovery_confidence < Decimal("7"):
        suggestions.append(
            "Gather more practice evidence for recovery points such as chorus entries."
        )
    return tuple(dict.fromkeys(suggestions))


def _recommendation(score: Decimal, hard: tuple[str, ...], completeness: Decimal) -> str:
    if hard or score < 45:
        return "poor fit for this opportunity"
    if score < 65 or completeness < 70:
        return "possible with adaptation"
    if score < 82:
        return "promising candidate"
    return "strong candidate for this opportunity"


def _observations(
    results: tuple[SuitabilityResult, ...], repertoire: Repertoire
) -> tuple[str, ...]:
    if not results:
        return ("No candidates remain after hard-constraint filtering.",)
    top = results[:3]
    songs = [repertoire.get_song(repertoire.get_version(r.version_id).song_identifier) for r in top]
    notes: list[str] = ["Scores compare fit for this opportunity; they are not artistic truth."]
    if len({s.mood for s in songs}) == 1 and len(songs) > 1:
        notes.append(f"All top candidates share a {songs[0].mood.value} mood; consider contrast.")
    if any(s.genre.value == "original" for s in songs):
        notes.append("An original may trade lower familiarity for stronger personal connection.")
    if results[0].completeness < Decimal("80"):
        notes.append(
            "The highest-rated candidate has incomplete information, so confidence is limited."
        )
    return tuple(notes)
