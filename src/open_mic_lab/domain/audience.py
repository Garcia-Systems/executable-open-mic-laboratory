"""Audience-experience models for Chapter 10."""

from dataclasses import dataclass
from enum import Enum

from open_mic_lab.domain.validation import (
    require_non_negative_int,
    require_positive_int,
    require_text,
)


class AudienceExpectation(Enum):
    """Transparent tendencies a group context may bring to a performance."""

    FAMILIARITY = "familiarity"
    LISTENING_ATTENTION = "listening attention"
    PARTICIPATION = "participation"
    CONCISE_STORYTELLING = "concise storytelling"
    WORSHIP_CONTEXT = "worship context"
    INFORMAL_SUPPORT = "informal support"
    OUTDOOR_ENERGY = "outdoor energy"
    EXPERIMENTAL_PATIENCE = "experimental patience"


class PerformanceMoment(Enum):
    """Meaningful moments in an audience-facing performance sequence."""

    OPENING_GREETING = "opening greeting"
    SONG = "song"
    STORY = "story"
    PARTICIPATION = "audience participation"
    QUIET_REFLECTION = "quiet reflection"
    TRANSITION = "transition"
    CLOSING_REMARKS = "closing remarks"


@dataclass(frozen=True, slots=True)
class AudienceProfile:
    """Educational profile describing audience tendencies, not stereotypes."""

    identifier: str
    name: str
    description: str
    expectations: tuple[AudienceExpectation, ...]
    familiarity_preference: int
    participation_comfort: int
    storytelling_tolerance: int
    pacing_patience: int
    variety_preference: int
    typical_context_notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require_text(self.identifier, "Audience profile identifier")
        require_text(self.name, "Audience profile name")
        require_text(self.description, "Audience profile description")
        if not self.expectations:
            raise ValueError("Audience profile requires at least one expectation.")
        for name, value in (
            ("Familiarity preference", self.familiarity_preference),
            ("Participation comfort", self.participation_comfort),
            ("Storytelling tolerance", self.storytelling_tolerance),
            ("Pacing patience", self.pacing_patience),
            ("Variety preference", self.variety_preference),
        ):
            if not 0 <= value <= 10:
                raise ValueError(f"{name} must be between 0 and 10.")


@dataclass(frozen=True, slots=True)
class ParticipationOpportunity:
    """A planned invitation the audience can accept or ignore."""

    description: str
    moment_identifier: str
    accessibility: int
    optional: bool = True

    def __post_init__(self) -> None:
        require_text(self.description, "Participation description")
        require_text(self.moment_identifier, "Participation moment identifier")
        if not 0 <= self.accessibility <= 10:
            raise ValueError("Participation accessibility must be between 0 and 10.")


@dataclass(frozen=True, slots=True)
class EngagementObservation:
    """One transparent audience-experience observation."""

    factor: str
    explanation: str
    adaptation_idea: str | None = None

    def __post_init__(self) -> None:
        require_text(self.factor, "Observation factor")
        require_text(self.explanation, "Observation explanation")


@dataclass(frozen=True, slots=True)
class AudienceResponse:
    """Structured non-predictive response analysis for one profile."""

    profile_identifier: str
    strengths: tuple[str, ...]
    friction_points: tuple[str, ...]
    adaptation_ideas: tuple[str, ...]
    explanations: tuple[EngagementObservation, ...]
    mermaid_diagram: str

    def __post_init__(self) -> None:
        require_text(self.profile_identifier, "Audience response profile identifier")
        require_text(self.mermaid_diagram, "Audience response Mermaid diagram")


@dataclass(frozen=True, slots=True)
class AudienceFeedbackSummary:
    """Comparison summary across two audience analyses."""

    left_profile: str
    right_profile: str
    shared_strengths: tuple[str, ...]
    different_observations: tuple[str, ...]
    reflection_prompts: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AudiencePerformanceMoment:
    """One moment in the planned audience-facing sequence."""

    identifier: str
    kind: PerformanceMoment
    label: str
    duration_seconds: int
    energy: int
    familiarity: int
    communication_clarity: int
    transition_quality: int
    storytelling: bool = False
    participation: ParticipationOpportunity | None = None

    def __post_init__(self) -> None:
        require_text(self.identifier, "Audience moment identifier")
        require_text(self.label, "Audience moment label")
        require_positive_int(self.duration_seconds, "Audience moment duration")
        for name, value in (
            ("Moment energy", self.energy),
            ("Moment familiarity", self.familiarity),
            ("Moment communication clarity", self.communication_clarity),
            ("Moment transition quality", self.transition_quality),
        ):
            if not 0 <= value <= 10:
                raise ValueError(f"{name} must be between 0 and 10.")


@dataclass(frozen=True, slots=True)
class AudiencePerformance:
    """Sequence analyzed by the Audience Experience Laboratory."""

    identifier: str
    name: str
    moments: tuple[AudiencePerformanceMoment, ...]

    @property
    def duration_seconds(self) -> int:
        """Return total performance duration."""
        return sum(moment.duration_seconds for moment in self.moments)

    def __post_init__(self) -> None:
        require_text(self.identifier, "Audience performance identifier")
        require_text(self.name, "Audience performance name")
        if not self.moments:
            raise ValueError("Audience performance requires at least one moment.")
        require_non_negative_int(self.duration_seconds, "Audience performance duration")
