"""Open mic event models for Chapter 14."""

from dataclasses import dataclass
from enum import Enum

from open_mic_lab.domain.validation import require_non_negative_int, require_text


class EventScenario(Enum):
    """Deterministic educational event scenarios, not predictions."""

    FIRST_OPEN_MIC = "first open mic"
    RETURNING_PERFORMER = "returning performer"
    COFFEEHOUSE = "coffeehouse"
    CHURCH_MUSIC_NIGHT = "church music night"
    SONGWRITER_SHOWCASE = "songwriter showcase"


@dataclass(frozen=True, slots=True)
class EventTimelineEntry:
    """One timestamped step in an open mic evening."""

    time: str
    label: str
    educational_note: str

    def __post_init__(self) -> None:
        require_text(self.time, "Timeline time")
        require_text(self.label, "Timeline label")
        require_text(self.educational_note, "Timeline note")


@dataclass(frozen=True, slots=True)
class PerformerArrival:
    """Arrival decision point."""

    arrival_time: str
    check_in_note: str
    setup_observation: str


@dataclass(frozen=True, slots=True)
class SignUpOrder:
    """Deterministic sign-up placement."""

    position: int
    estimated_call_time: str
    rationale: str

    def __post_init__(self) -> None:
        require_non_negative_int(self.position, "Sign-up position")
        require_text(self.estimated_call_time, "Estimated call time")
        require_text(self.rationale, "Sign-up rationale")


@dataclass(frozen=True, slots=True)
class WaitingPeriod:
    """How the learner uses the time before performing."""

    duration_minutes: int
    observations: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PerformanceSlot:
    """Scheduled open mic slot."""

    call_time: str
    duration_minutes: int
    version_identifiers: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PerformanceExecution:
    """Summary of the performed set."""

    started_at: str
    ended_at: str
    recovery_event: str
    improvisation_choice: str


@dataclass(frozen=True, slots=True)
class NetworkingOpportunity:
    """Post-performance social learning opportunity."""

    time: str
    prompt: str
    follow_up: str


@dataclass(frozen=True, slots=True)
class PostPerformanceReflection:
    """Reflection prompts produced by the event."""

    time: str
    prompts: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EventTimeline:
    """Complete deterministic timeline."""

    entries: tuple[EventTimelineEntry, ...]


@dataclass(frozen=True, slots=True)
class OpenMicEvent:
    """Complete immutable open mic simulation input/output envelope."""

    identifier: str
    scenario: EventScenario
    venue_template: str
    arrival: PerformerArrival
    signup: SignUpOrder
    waiting: WaitingPeriod
    slot: PerformanceSlot
    execution: PerformanceExecution
    networking: NetworkingOpportunity
    reflection: PostPerformanceReflection
    timeline: EventTimeline
    experiment_history: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class EventReport:
    """Deterministic report that references subsystem outputs."""

    event: OpenMicEvent
    preparation: tuple[str, ...]
    repertoire_used: tuple[str, ...]
    arrangement_choices: tuple[str, ...]
    communication_plan: tuple[str, ...]
    equipment_setup: tuple[str, ...]
    soundcheck_observations: tuple[str, ...]
    audience_observations: tuple[str, ...]
    recovery_events: tuple[str, ...]
    improvisation_opportunities: tuple[str, ...]
    original_music_notes: tuple[str, ...]
    reflection_prompts: tuple[str, ...]
