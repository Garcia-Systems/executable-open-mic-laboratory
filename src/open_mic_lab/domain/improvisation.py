"""Improvisation models for adaptive musical decision-making."""

from dataclasses import dataclass
from enum import Enum

from open_mic_lab.domain.validation import require_non_negative_int, require_text


class ImprovisationOpportunity(Enum):
    """Places where a performer can adapt without abandoning structure."""

    EXTEND_ENDING = "extend the ending"
    SHORTEN_PERFORMANCE = "shorten the performance"
    REPEAT_CHORUS = "repeat a chorus"
    ADD_INSTRUMENTAL_SPACE = "add instrumental space"
    ENCOURAGE_AUDIENCE_PARTICIPATION = "encourage audience participation"
    CREATE_SMOOTHER_TRANSITION = "create a smoother transition"
    ADJUST_DYNAMICS = "adjust dynamics"
    FINISH_EARLY = "finish early"


class ImprovisationDecision(Enum):
    """Immutable experiments learners can compare."""

    REPEAT_CHORUS = "repeat chorus"
    EXTEND_ENDING = "extend ending"
    SHORTEN_INTRO = "shorten intro"
    REMOVE_VERSE = "remove verse"
    ADD_AUDIENCE_PARTICIPATION = "add audience participation"
    INSERT_INSTRUMENTAL_BREAK = "insert instrumental break"
    EXTEND_TRANSITION = "extend transition"
    FINISH_IMMEDIATELY = "finish immediately"


class ImprovisationConstraint(Enum):
    """Educational constraints that influence, but do not determine, choices."""

    REMAINING_TIME = "remaining time"
    PERFORMER_READINESS = "performer readiness"
    COORDINATION_DEMANDS = "coordination demands"
    VENUE_EXPECTATIONS = "venue expectations"
    AUDIENCE_PARTICIPATION = "audience participation"
    TRANSITION_CONTINUITY = "transition continuity"


@dataclass(frozen=True, slots=True)
class ImprovisationContext:
    """Context for deterministic improvisation analysis."""

    performance_identifier: str
    arrangement_identifier: str
    audience_profile_identifier: str
    recovery_context: str
    available_time_seconds: int
    performer_readiness: int
    coordination_demand: int
    venue_expectation: str
    needs_transition_continuity: bool = True

    def __post_init__(self) -> None:
        require_text(self.performance_identifier, "Performance identifier")
        require_text(self.arrangement_identifier, "Arrangement identifier")
        require_text(self.audience_profile_identifier, "Audience profile identifier")
        require_text(self.recovery_context, "Recovery context")
        require_non_negative_int(self.available_time_seconds, "Available time")
        require_text(self.venue_expectation, "Venue expectation")
        for name, value in (
            ("Performer readiness", self.performer_readiness),
            ("Coordination demand", self.coordination_demand),
        ):
            if not 0 <= value <= 10:
                raise ValueError(f"{name} must be between 0 and 10.")


@dataclass(frozen=True, slots=True)
class TimelineSection:
    """One planned or adapted timeline section."""

    label: str
    duration_seconds: int
    source: str = "planned"

    def __post_init__(self) -> None:
        require_text(self.label, "Timeline label")
        require_non_negative_int(self.duration_seconds, "Timeline duration")
        require_text(self.source, "Timeline source")


@dataclass(frozen=True, slots=True)
class TransitionExtension:
    """A named transition extension separate from arrangement structure."""

    label: str
    added_seconds: int
    purpose: str

    def __post_init__(self) -> None:
        require_text(self.label, "Transition extension label")
        require_non_negative_int(self.added_seconds, "Transition extension seconds")
        require_text(self.purpose, "Transition extension purpose")


@dataclass(frozen=True, slots=True)
class EndingVariation:
    """A deterministic ending variation."""

    label: str
    added_seconds: int
    energy_shape: str

    def __post_init__(self) -> None:
        require_text(self.label, "Ending variation label")
        require_non_negative_int(self.added_seconds, "Ending variation seconds")
        require_text(self.energy_shape, "Ending variation energy shape")


@dataclass(frozen=True, slots=True)
class IntroVariation:
    """A deterministic introduction variation."""

    label: str
    duration_seconds: int
    purpose: str

    def __post_init__(self) -> None:
        require_text(self.label, "Intro variation label")
        require_non_negative_int(self.duration_seconds, "Intro variation seconds")
        require_text(self.purpose, "Intro variation purpose")


@dataclass(frozen=True, slots=True)
class AdaptivePerformancePlan:
    """Immutable planned or adapted performance timeline."""

    identifier: str
    source_plan_identifier: str
    sections: tuple[TimelineSection, ...]
    decisions: tuple[ImprovisationDecision, ...] = ()
    rationale: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require_text(self.identifier, "Adaptive plan identifier")
        require_text(self.source_plan_identifier, "Source plan identifier")
        if not self.sections:
            raise ValueError("Adaptive performance plan requires sections.")

    @property
    def total_duration_seconds(self) -> int:
        """Return deterministic total duration."""
        return sum(section.duration_seconds for section in self.sections)


@dataclass(frozen=True, slots=True)
class ImprovisationOption:
    """One available adaptation with tradeoffs and fit explanation."""

    opportunity: ImprovisationOpportunity
    decision: ImprovisationDecision
    constraints: tuple[ImprovisationConstraint, ...]
    tradeoffs: tuple[str, ...]
    suggestion: str
    explanation: str


@dataclass(frozen=True, slots=True)
class ImprovisationAnalysis:
    """Structured analysis that avoids choosing one best improvisation."""

    context: ImprovisationContext
    observations: tuple[str, ...]
    options: tuple[ImprovisationOption, ...]
    adaptation_suggestions: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TimelineComparison:
    """Educational comparison between planned and adapted timelines."""

    planned: AdaptivePerformancePlan
    adapted: AdaptivePerformancePlan
    differences: tuple[str, ...]
    educational_observations: tuple[str, ...]
