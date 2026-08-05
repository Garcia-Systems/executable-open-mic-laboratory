"""Practice session and deliberate practice planning models."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum

from open_mic_lab.domain.validation import (
    require_non_negative_int,
    require_positive_int,
    require_rating,
    require_text,
)


class SkillArea(Enum):
    """Reusable skill areas that practice can maintain or improve."""

    READINESS = "readiness"
    MEMORY = "memory"
    VOCALS = "vocals"
    ACCOMPANIMENT = "accompaniment"
    RHYTHM = "rhythm"
    COORDINATION = "coordination"
    ARRANGEMENT = "arrangement"
    PERFORMANCE = "performance"
    RECOVERY = "recovery"
    REFLECTION = "reflection"


class PracticePriority(Enum):
    """Educational priority levels for allocating scarce practice time."""

    LOW = "low"
    MAINTAIN = "maintain"
    IMPROVE = "improve"
    URGENT = "urgent"


class PracticeGoal(Enum):
    """High-level goal of a practice plan."""

    BALANCED_IMPROVEMENT = "balanced improvement"
    MAINTENANCE = "maintenance"
    PERFORMANCE_PREPARATION = "performance preparation"
    COORDINATION_FOCUS = "coordination focus"
    MEMORIZATION = "memorization"
    EXPLORATION = "exploration"


class PracticeTask(Enum):
    """Kinds of deliberate practice blocks supported by Chapter 6."""

    WARM_UP = "warm-up"
    RHYTHM_ISOLATION = "rhythm isolation"
    ACCOMPANIMENT_ONLY = "accompaniment only"
    LYRICS_ONLY = "lyrics only"
    COORDINATION = "coordination"
    ARRANGEMENT_REFINEMENT = "arrangement refinement"
    TEMPO_LADDER = "tempo ladder"
    PERFORMANCE_RUN_THROUGH = "performance run-through"
    COOLDOWN = "cooldown"
    REFLECTION = "reflection"


@dataclass(frozen=True, slots=True)
class PracticeSession:
    """One deliberate practice session for a performance version."""

    identifier: str
    performance_version_identifier: str
    date: date
    duration_minutes: int
    practiced_tempo_bpm: int
    mistake_count: int
    memory_confidence: Decimal
    vocal_comfort: Decimal
    accompaniment_stability: Decimal
    recovery_confidence: Decimal
    notes: str = ""

    def __post_init__(self) -> None:
        require_text(self.identifier, "Practice session identifier")
        require_text(self.performance_version_identifier, "Performance version identifier")
        require_positive_int(self.duration_minutes, "Practice duration")
        require_positive_int(self.practiced_tempo_bpm, "Practiced tempo")
        require_non_negative_int(self.mistake_count, "Mistake count")
        require_rating(self.memory_confidence, "Memory confidence")
        require_rating(self.vocal_comfort, "Vocal comfort")
        require_rating(self.accompaniment_stability, "Accompaniment stability")
        require_rating(self.recovery_confidence, "Recovery confidence")


@dataclass(frozen=True, slots=True)
class PracticeBlock:
    """A time-boxed practice investment with an explicit stopping condition."""

    task: PracticeTask
    duration_minutes: int
    objective: str
    focus_area: SkillArea
    success_criteria: str
    notes: str
    version_identifier: str | None = None

    def __post_init__(self) -> None:
        require_positive_int(self.duration_minutes, "Practice block duration")
        require_text(self.objective, "Practice block objective")
        require_text(self.success_criteria, "Practice block success criteria")
        require_text(self.notes, "Practice block notes")


@dataclass(frozen=True, slots=True)
class PracticeOutcome:
    """Observed outcome used by analytics without claiming to predict mastery."""

    version_identifier: str
    skill_area: SkillArea
    minutes: int
    readiness_delta: int
    observation: str


@dataclass(frozen=True, slots=True)
class PracticePlan:
    """Deterministic recommendation for a complete practice session."""

    identifier: str
    goal: PracticeGoal
    available_minutes: int
    blocks: tuple[PracticeBlock, ...]
    rationale: tuple[str, ...]

    @property
    def estimated_duration_minutes(self) -> int:
        """Return the total planned duration."""
        return sum(block.duration_minutes for block in self.blocks)

    def __post_init__(self) -> None:
        require_text(self.identifier, "Practice plan identifier")
        require_positive_int(self.available_minutes, "Available practice time")
        if not self.blocks:
            raise ValueError("Practice plan requires at least one block")
