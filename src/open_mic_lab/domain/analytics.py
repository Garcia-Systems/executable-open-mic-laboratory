"""Performance analytics and continuous-improvement domain models."""

from dataclasses import dataclass
from datetime import date

from open_mic_lab.domain.validation import require_non_negative_int, require_text


@dataclass(frozen=True, slots=True)
class PerformanceSnapshot:
    """A summarized observation from one performance, not an artistic grade."""

    identifier: str
    performed_on: date
    version_identifiers: tuple[str, ...]
    readiness_score: int
    repertoire_size: int
    genre_count: int
    practice_minutes: int
    coordination_score: int
    communication_score: int
    equipment_issues: int
    soundcheck_warnings: int
    audience_observations: tuple[str, ...]
    recovery_events: int
    improvisation_used: bool
    original_songs: int
    event_summary: str

    def __post_init__(self) -> None:
        require_text(self.identifier, "Performance snapshot identifier")
        require_non_negative_int(self.readiness_score, "Readiness score")
        require_non_negative_int(self.repertoire_size, "Repertoire size")
        require_non_negative_int(self.genre_count, "Genre count")
        require_non_negative_int(self.practice_minutes, "Practice minutes")
        require_non_negative_int(self.coordination_score, "Coordination score")
        require_non_negative_int(self.communication_score, "Communication score")
        require_non_negative_int(self.equipment_issues, "Equipment issues")
        require_non_negative_int(self.soundcheck_warnings, "Sound-check warnings")
        require_non_negative_int(self.recovery_events, "Recovery events")
        require_non_negative_int(self.original_songs, "Original songs")
        require_text(self.event_summary, "Event summary")
        if not self.version_identifiers:
            raise ValueError("Performance snapshots need at least one performed version.")
        for version_id in self.version_identifiers:
            require_text(version_id, "Snapshot version identifier")
        for observation in self.audience_observations:
            require_text(observation, "Audience observation")


@dataclass(frozen=True, slots=True)
class PerformanceHistory:
    """Chronological performance snapshots for long-term learning."""

    snapshots: tuple[PerformanceSnapshot, ...]

    def __post_init__(self) -> None:
        if not self.snapshots:
            raise ValueError("Performance history needs at least one snapshot.")
        dates = tuple(snapshot.performed_on for snapshot in self.snapshots)
        if dates != tuple(sorted(dates)):
            raise ValueError("Performance history must be chronological.")


@dataclass(frozen=True, slots=True)
class TrendObservation:
    """A transparent trend statement with supporting evidence."""

    name: str
    direction: str
    evidence: str


@dataclass(frozen=True, slots=True)
class PracticeTrend:
    """Practice consistency summarized across performances."""

    average_minutes: int
    consistency_score: int
    observation: str


@dataclass(frozen=True, slots=True)
class RepertoireTrend:
    """Repertoire growth and balance summarized across performances."""

    starting_size: int
    ending_size: int
    genre_count: int
    observation: str


@dataclass(frozen=True, slots=True)
class ImprovementRecommendation:
    """An educational next action with a visible reason."""

    action: str
    reason: str
    related_chapters: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PerformanceDashboard:
    """Deterministic text dashboard values and rendered report."""

    readiness: int
    repertoire_diversity: int
    practice_consistency: int
    communication: int
    technical_preparation: int
    recovery_confidence: int
    text: str
    mermaid: str


@dataclass(frozen=True, slots=True)
class ImprovementPlan:
    """Immutable continuous-improvement plan."""

    identifier: str
    focus: str
    actions: tuple[str, ...]
    rationale: tuple[str, ...]
    experiment_history: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AnalyticsReport:
    """Complete Volume I analytics report."""

    history: PerformanceHistory
    practice_trend: PracticeTrend
    repertoire_trend: RepertoireTrend
    trends: tuple[TrendObservation, ...]
    dashboard: PerformanceDashboard
    recommendations: tuple[ImprovementRecommendation, ...]
    improvement_plan: ImprovementPlan
    volume_summary: tuple[str, ...]
