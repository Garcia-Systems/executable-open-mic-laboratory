"""Recovery models for Chapter 11."""

from dataclasses import dataclass
from enum import Enum

from open_mic_lab.domain.validation import require_non_negative_int, require_text


class IncidentType(Enum):
    """Educational incident scenarios, not predictions."""

    FORGOTTEN_LYRICS = "forgotten lyrics"
    WRONG_CHORD = "wrong chord"
    MISSED_ENTRANCE = "missed entrance"
    TEMPO_DRIFT = "tempo drift"
    SKIPPED_VERSE = "skipped verse"
    MICROPHONE_FAILURE = "microphone failure"
    CABLE_DISCONNECTED = "cable disconnected"
    BROKEN_STRING = "broken string"
    MONITOR_PROBLEM = "monitor problem"
    PAGE_TURN_ISSUE = "page turn issue"
    AUDIENCE_INTERRUPTION = "audience interruption"


class RecoveryStrategy(Enum):
    """Deterministic recovery choices available for experiments."""

    CONTINUE_IMMEDIATELY = "continue immediately"
    RESTART_SECTION = "restart section"
    SIMPLIFY_ACCOMPANIMENT = "simplify accompaniment"
    INVITE_AUDIENCE_PARTICIPATION = "invite audience participation"
    SKIP_VERSE = "skip verse"
    STOP_AND_EXPLAIN = "stop and explain"
    INSTRUMENTAL_RECOVERY = "instrumental recovery"
    TEMPO_RESET = "tempo reset"


class RecoveryStage(Enum):
    """Stages in a recoverable performance event."""

    MISTAKE_OCCURS = "Mistake Occurs"
    PERFORMER_RECOGNIZES = "Performer Recognizes Issue"
    RECOVERY_DECISION = "Recovery Decision"
    AUDIENCE_PERCEPTION = "Audience Perception"
    PERFORMANCE_CONTINUES = "Performance Continues"
    REFLECTION = "Reflection"


@dataclass(frozen=True, slots=True)
class PerformanceIncident:
    """One educational performance incident independent of repertoire."""

    identifier: str
    incident_type: IncidentType
    moment: str
    description: str
    performer_noticeability: int
    audience_noticeability: int
    technical: bool = False

    def __post_init__(self) -> None:
        require_text(self.identifier, "Incident identifier")
        require_text(self.moment, "Incident moment")
        require_text(self.description, "Incident description")
        for name, value in (
            ("Performer noticeability", self.performer_noticeability),
            ("Audience noticeability", self.audience_noticeability),
        ):
            if not 0 <= value <= 10:
                raise ValueError(f"{name} must be between 0 and 10.")


@dataclass(frozen=True, slots=True)
class RecoveryAction:
    """A suggested performer action with educational rationale."""

    strategy: RecoveryStrategy
    description: str
    rationale: str

    def __post_init__(self) -> None:
        require_text(self.description, "Recovery action description")
        require_text(self.rationale, "Recovery action rationale")


@dataclass(frozen=True, slots=True)
class RecoveryOutcome:
    """Non-scored recovery outcome dimensions."""

    strategy: RecoveryStrategy
    continuity: str
    audience_impact: str
    technical_considerations: tuple[str, ...]
    educational_response: str

    def __post_init__(self) -> None:
        require_text(self.continuity, "Recovery continuity")
        require_text(self.audience_impact, "Recovery audience impact")
        require_text(self.educational_response, "Recovery educational response")


@dataclass(frozen=True, slots=True)
class RecoveryTimelineEvent:
    """One event in a recovery timeline."""

    stage: RecoveryStage
    label: str
    elapsed_seconds: int
    note: str

    def __post_init__(self) -> None:
        require_text(self.label, "Recovery timeline label")
        require_non_negative_int(self.elapsed_seconds, "Recovery elapsed seconds")
        require_text(self.note, "Recovery timeline note")


@dataclass(frozen=True, slots=True)
class RecoveryTimeline:
    """Deterministic sequence from incident through reflection."""

    incident_identifier: str
    strategy: RecoveryStrategy
    events: tuple[RecoveryTimelineEvent, ...]

    def __post_init__(self) -> None:
        require_text(self.incident_identifier, "Recovery timeline incident identifier")
        if not self.events:
            raise ValueError("Recovery timeline requires events.")


@dataclass(frozen=True, slots=True)
class IncidentReport:
    """Structured recovery analysis for education and reflection."""

    incident: PerformanceIncident
    context: str
    preparation: str
    communication_plan: str
    observations: tuple[str, ...]
    strengths: tuple[str, ...]
    recovery_timeline: RecoveryTimeline
    suggested_actions: tuple[RecoveryAction, ...]
    reflection_prompts: tuple[str, ...]
    outcomes: tuple[RecoveryOutcome, ...]


INCIDENT_CATALOG: tuple[PerformanceIncident, ...] = (
    PerformanceIncident(
        "forgotten-lyrics",
        IncidentType.FORGOTTEN_LYRICS,
        "second verse",
        "The performer loses the next lyric phrase.",
        9,
        6,
    ),
    PerformanceIncident(
        "wrong-chord",
        IncidentType.WRONG_CHORD,
        "chorus entrance",
        "The accompaniment lands on an unintended chord.",
        8,
        5,
    ),
    PerformanceIncident(
        "missed-entrance",
        IncidentType.MISSED_ENTRANCE,
        "after intro",
        "The vocal entrance arrives one measure late.",
        7,
        5,
    ),
    PerformanceIncident(
        "tempo-drift",
        IncidentType.TEMPO_DRIFT,
        "middle section",
        "Tempo gradually pushes faster than planned.",
        6,
        4,
    ),
    PerformanceIncident(
        "skipped-verse",
        IncidentType.SKIPPED_VERSE,
        "form navigation",
        "A verse is skipped during the song form.",
        7,
        4,
    ),
    PerformanceIncident(
        "microphone-failure",
        IncidentType.MICROPHONE_FAILURE,
        "first chorus",
        "The vocal microphone stops reaching the room.",
        8,
        8,
        True,
    ),
    PerformanceIncident(
        "cable-disconnected",
        IncidentType.CABLE_DISCONNECTED,
        "setup transition",
        "A cable disconnects and interrupts the signal path.",
        9,
        8,
        True,
    ),
    PerformanceIncident(
        "broken-string",
        IncidentType.BROKEN_STRING,
        "strummed passage",
        "A guitar string breaks during performance.",
        9,
        7,
        True,
    ),
    PerformanceIncident(
        "monitor-problem",
        IncidentType.MONITOR_PROBLEM,
        "opening song",
        "The performer cannot hear enough monitor mix.",
        8,
        3,
        True,
    ),
    PerformanceIncident(
        "page-turn-issue",
        IncidentType.PAGE_TURN_ISSUE,
        "bridge",
        "A chart page is not available at the needed moment.",
        8,
        4,
    ),
    PerformanceIncident(
        "audience-interruption",
        IncidentType.AUDIENCE_INTERRUPTION,
        "quiet introduction",
        "An audience sound interrupts a focused moment.",
        6,
        6,
    ),
)
