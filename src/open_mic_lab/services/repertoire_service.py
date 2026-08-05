"""Repertoire engineering analysis for Chapter 2."""

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

from collections import Counter
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from open_mic_lab.domain import (
    Difficulty,
    EnergyLevel,
    Instrument,
    PerformanceRole,
    PerformanceStatus,
    Repertoire,
    VenueType,
)
from open_mic_lab.domain.performance import PerformanceVersion
from open_mic_lab.services.readiness_service import calculate_readiness

TODAY = date(2026, 8, 5)


@dataclass(frozen=True, slots=True)
class LearningPriority:
    """A structured answer to: what should I learn next?"""

    version_id: str
    score: int
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RepertoireHealth:
    """Educational health score with transparent components."""

    score: int
    diversity: int
    maintenance: int
    readiness: int
    balance: int
    role_coverage: int
    explanation: str


@dataclass(frozen=True, slots=True)
class RepertoireAnalysis:
    """Deterministic repertoire analysis snapshot."""

    observations: tuple[str, ...]
    genre_distribution: dict[str, int]
    key_distribution: dict[str, int]
    tempo_distribution: dict[str, int]
    mood_distribution: dict[str, int]
    instrument_distribution: dict[str, int]
    role_distribution: dict[str, int]
    readiness_distribution: dict[str, int]
    neglected_version_ids: tuple[str, ...]
    improved_version_ids: tuple[str, ...]
    diversity_score: int


class RepertoireEngineeringService:
    """Analyze repertoire as a changing system rather than a static song list."""

    def analyze(self, repertoire: Repertoire, today: date = TODAY) -> RepertoireAnalysis:
        """Return distributions, activity signals, and educational observations."""
        versions = tuple(repertoire.versions.values())
        genres = Counter(repertoire.get_song(v.song_identifier).genre.value for v in versions)
        keys = Counter(v.performance_key for v in versions)
        tempos = Counter(self._tempo_band(v.target_tempo_bpm) for v in versions)
        moods = Counter(repertoire.get_song(v.song_identifier).mood.value for v in versions)
        instruments = Counter(v.primary_instrument.value for v in versions)
        roles = Counter(role.value for v in versions for role in v.supported_roles)
        readiness = Counter(calculate_readiness(v).category for v in versions)
        neglected = tuple(
            v.identifier
            for v in versions
            if self._days_since(v.last_practiced, today) > v.maintenance_interval_days
        )
        improved = tuple(
            v.identifier
            for v in versions
            if v.performance_status
            in {PerformanceStatus.NEARLY_READY, PerformanceStatus.PERFORMANCE_READY}
            and v.total_practice_sessions >= 3
        )
        diversity = self._diversity_score(genres, keys, moods, instruments, roles)
        observations = self._observations(
            genres, keys, moods, instruments, roles, readiness, neglected, diversity
        )
        return RepertoireAnalysis(
            observations,
            dict(genres),
            dict(keys),
            dict(tempos),
            dict(moods),
            dict(instruments),
            dict(roles),
            dict(readiness),
            neglected,
            improved,
            diversity,
        )

    def gaps(self, repertoire: Repertoire) -> tuple[str, ...]:
        """Return deterministic category-level gap recommendations."""
        versions = tuple(repertoire.versions.values())
        high_confidence = [v for v in versions if self._confidence(v) >= Decimal("8")]
        gaps: list[str] = []
        if not any(
            PerformanceRole.OPENER in v.supported_roles and v in high_confidence for v in versions
        ):
            gaps.append("Your repertoire has no high-confidence opener.")
        if not any(
            PerformanceRole.CLOSER in v.supported_roles and v in high_confidence for v in versions
        ):
            gaps.append("Your repertoire has no high-confidence closer.")
        if not any(v.energy_level in {EnergyLevel.HIGH, EnergyLevel.VERY_HIGH} for v in versions):
            gaps.append("Add an upbeat category so the set can lift the room.")
        if not any(PerformanceRole.AUDIENCE_PARTICIPATION in v.supported_roles for v in versions):
            gaps.append("Add an audience-participation category for interactive venues.")
        if not any(
            repertoire.get_song(v.song_identifier).genre.value == "original" for v in versions
        ):
            gaps.append("Add an original-song category when your writing is ready to test.")
        if not any(
            v.primary_instrument == Instrument.GUITAR_VOCAL
            and PerformanceRole.OPENER in v.supported_roles
            for v in versions
        ):
            gaps.append("You have several strong songs but no guitar-based opener.")
        if not any(v.arrangement_difficulty == Difficulty.SIMPLE for v in versions):
            gaps.append("Keep at least one low-difficulty song for stressful rooms.")
        if not any(v.arrangement_difficulty == Difficulty.CHALLENGING for v in versions):
            gaps.append("Keep one advanced challenge song to grow the repertoire.")
        return tuple(gaps)

    def priorities(
        self, repertoire: Repertoire, desired_venue: VenueType | None = None
    ) -> tuple[LearningPriority, ...]:
        """Rank learning priorities using readiness, neglect, balance, venue, and role gaps."""
        analysis = self.analyze(repertoire)
        missing_roles = {
            "opener": not any("opener" in r for r in analysis.role_distribution),
            "closer": not any("closer" in r for r in analysis.role_distribution),
        }
        priorities: list[LearningPriority] = []
        for v in repertoire.versions.values():
            score = 0
            reasons: list[str] = []
            readiness = calculate_readiness(v).score
            if 65 <= readiness < 85:
                score += 30
                reasons.append("nearly performance-ready and likely to reward focused work")
            if v.identifier in analysis.neglected_version_ids:
                score += 18
                reasons.append("recently neglected compared with its maintenance interval")
            song = repertoire.get_song(v.song_identifier)
            if analysis.genre_distribution[song.genre.value] == 1:
                score += 14
                reasons.append("protects a less-represented genre")
            if analysis.instrument_distribution[v.primary_instrument.value] == 1:
                score += 10
                reasons.append("protects a less-represented instrument")
            if any(
                (role == PerformanceRole.OPENER and missing_roles["opener"])
                or (role == PerformanceRole.CLOSER and missing_roles["closer"])
                for role in v.supported_roles
            ):
                score += 20
                reasons.append("fills a missing set role")
            if desired_venue == VenueType.CAFE and VenueType.CAFE in v.preferred_venue_types:
                score += 8
                reasons.append("fits the requested coffeehouse venue")
            if v.performance_status == PerformanceStatus.RETIRED:
                score -= 20
                reasons.append("retired songs should be revived deliberately, not by habit")
            priorities.append(
                LearningPriority(
                    v.identifier,
                    score,
                    tuple(reasons) or ("useful comparison item with no urgent signal",),
                )
            )
        return tuple(sorted(priorities, key=lambda p: (-p.score, p.version_id)))

    def health(self, repertoire: Repertoire) -> RepertoireHealth:
        """Compute the documented educational repertoire health score."""
        analysis = self.analyze(repertoire)
        count = max(1, len(repertoire.versions))
        maintenance = round(100 * (count - len(analysis.neglected_version_ids)) / count)
        readiness = round(
            sum(calculate_readiness(v).score for v in repertoire.versions.values()) / count
        )
        balance = max(0, 100 - max(analysis.genre_distribution.values(), default=0) * 100 // count)
        required_roles = {
            PerformanceRole.OPENER.value,
            PerformanceRole.CLOSER.value,
            PerformanceRole.AUDIENCE_PARTICIPATION.value,
            PerformanceRole.ORIGINAL_FEATURE.value,
        }
        role_coverage = round(
            100 * len(required_roles & set(analysis.role_distribution)) / len(required_roles)
        )
        score = round(
            analysis.diversity_score * 0.25
            + maintenance * 0.20
            + readiness * 0.25
            + balance * 0.15
            + role_coverage * 0.15
        )
        return RepertoireHealth(
            score,
            analysis.diversity_score,
            maintenance,
            readiness,
            balance,
            role_coverage,
            "Educational comparison only: not an objective measure of musicianship.",
        )

    def text_report(self, title: str, distribution: dict[str, int]) -> str:
        """Render a deterministic text bar report."""
        lines = [title, "=" * len(title)]
        for key, value in sorted(distribution.items()):
            lines.append(f"{key.title():<18} {value:>2} {'#' * value}")
        return "\n".join(lines)

    def _observations(
        self,
        genres: Counter[str],
        keys: Counter[str],
        moods: Counter[str],
        instruments: Counter[str],
        roles: Counter[str],
        readiness: Counter[str],
        neglected: tuple[str, ...],
        diversity: int,
    ) -> tuple[str, ...]:
        obs = []
        if keys:
            common = ", ".join(k for k, _ in keys.most_common(2))
            obs.append(
                f"Most of your songs are in {common}. "
                "Consider additional keys to increase flexibility."
            )
        if moods and instruments:
            obs.append(
                f"Your strongest cluster is {moods.most_common(1)[0][0]} material "
                f"on {instruments.most_common(1)[0][0]}."
            )
        if not any("closer" in r for r in roles):
            obs.append("Your repertoire has no defined closer role.")
        if neglected:
            obs.append(f"{len(neglected)} songs have stalled beyond their maintenance interval.")
        obs.append(
            f"Diversity score is {diversity}/100; use it to compare "
            "repertoire experiments, not artistic worth."
        )
        return tuple(obs)

    def _diversity_score(self, *counters: Counter[str]) -> int:
        scores = []
        for c in counters:
            total = sum(c.values()) or 1
            scores.append(round(100 * (1 - sum((n / total) ** 2 for n in c.values()))))
        return round(sum(scores) / len(scores))

    def _tempo_band(self, bpm: int) -> str:
        if bpm < 90:
            return "slow"
        if bpm <= 120:
            return "medium"
        return "fast"

    def _days_since(self, value: date | None, today: date) -> int:
        return 999 if value is None else (today - value).days

    def _confidence(self, v: PerformanceVersion) -> Decimal:
        return (
            v.vocal_comfort
            + v.accompaniment_stability
            + v.memory_confidence
            + v.recovery_confidence
        ) / Decimal("4")


def describe_repertoire(repertoire: Repertoire) -> tuple[str, ...]:
    """Return deterministic one-line descriptions of all performance versions."""
    lines: list[str] = []
    for version in repertoire.versions.values():
        song = repertoire.get_song(version.song_identifier)
        lines.append(
            f"{version.identifier}: {song.title} by {song.artist} | "
            f"{song.genre.value}, {song.mood.value} | "
            f"{version.primary_instrument.value} | {version.performance_status.value}"
        )
    return tuple(lines)
