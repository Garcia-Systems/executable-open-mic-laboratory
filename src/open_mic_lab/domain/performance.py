"""Performance-version, set-list, and performance event models."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from open_mic_lab.domain.enums import (
    Difficulty,
    EnergyLevel,
    Instrument,
    PerformanceRole,
    PerformanceStatus,
    VenueType,
)
from open_mic_lab.domain.pitch import VocalRange
from open_mic_lab.domain.validation import (
    require_non_negative_int,
    require_positive_int,
    require_rating,
    require_text,
)


@dataclass(frozen=True, slots=True)
class ArrangementFlexibility:
    """How readily an arrangement can be adapted for learning experiments."""

    can_transpose: bool
    can_simplify: bool
    can_shorten: bool
    adaptable_instruments: tuple[Instrument, ...]
    supports_solo: bool
    supports_group: bool

    def __post_init__(self) -> None:
        if not self.adaptable_instruments:
            raise ValueError("Arrangement flexibility needs at least one adaptable instrument.")


@dataclass(frozen=True, slots=True)
class PerformanceVersion:
    """A performer's current arrangement and preparation state for a song."""

    identifier: str
    song_identifier: str
    performance_key: str
    target_tempo_bpm: int
    primary_instrument: Instrument
    arrangement_difficulty: Difficulty
    vocal_comfort: Decimal
    accompaniment_stability: Decimal
    memory_confidence: Decimal
    recovery_confidence: Decimal
    performance_status: PerformanceStatus
    introduction_length_seconds: int
    required_vocal_range: VocalRange | None = None
    energy_level: EnergyLevel = EnergyLevel.MEDIUM
    supported_roles: tuple[PerformanceRole, ...] = (PerformanceRole.FLEXIBLE,)
    performer_connection: Decimal | None = None
    arrangement_flexibility: ArrangementFlexibility | None = None
    estimated_duration_seconds: int = 210
    is_available: bool = True
    adaptation_notes: tuple[str, ...] = ()
    date_added: date | None = None
    last_practiced: date | None = None
    last_performed: date | None = None
    maintenance_interval_days: int = 14
    total_practice_sessions: int = 0
    total_performances: int = 0
    total_audience_responses: int = 0
    target_readiness: int = 85
    preferred_venue_types: tuple[VenueType, ...] = ()
    setup_requirements: tuple[str, ...] = ()
    preferred_performance_role: PerformanceRole | None = None
    average_confidence: Decimal | None = None
    notes: str = ""

    def __post_init__(self) -> None:
        require_text(self.identifier, "Performance version identifier")
        require_text(self.song_identifier, "Song identifier")
        require_text(self.performance_key, "Performance key")
        require_positive_int(self.target_tempo_bpm, "Target tempo")
        require_rating(self.vocal_comfort, "Vocal comfort")
        require_rating(self.accompaniment_stability, "Accompaniment stability")
        require_rating(self.memory_confidence, "Memory confidence")
        require_rating(self.recovery_confidence, "Recovery confidence")
        require_non_negative_int(self.introduction_length_seconds, "Introduction length")
        require_positive_int(self.estimated_duration_seconds, "Estimated duration")
        if self.performer_connection is not None:
            require_rating(self.performer_connection, "Performer connection")
        require_positive_int(self.maintenance_interval_days, "Maintenance interval")
        require_non_negative_int(self.total_practice_sessions, "Total practice sessions")
        require_non_negative_int(self.total_performances, "Total performances")
        require_non_negative_int(self.total_audience_responses, "Total audience responses")
        require_rating(Decimal(self.target_readiness) / Decimal("10"), "Target readiness")
        if self.average_confidence is not None:
            require_rating(self.average_confidence, "Average confidence")
        if not self.supported_roles:
            raise ValueError("Performance versions need at least one supported role.")
        for note in self.adaptation_notes:
            require_text(note, "Adaptation note")


@dataclass(frozen=True, slots=True)
class SetList:
    """An ordered group of performance versions for a venue."""

    identifier: str
    name: str
    ordered_version_identifiers: tuple[str, ...]
    target_duration_minutes: int
    venue_identifier: str
    notes: str = ""

    def __post_init__(self) -> None:
        require_text(self.identifier, "Set-list identifier")
        require_text(self.name, "Set-list name")
        require_text(self.venue_identifier, "Venue identifier")
        require_positive_int(self.target_duration_minutes, "Target duration")
        if len(set(self.ordered_version_identifiers)) != len(self.ordered_version_identifiers):
            raise ValueError("Set lists cannot repeat a performance version in this milestone.")
        for version_id in self.ordered_version_identifiers:
            require_text(version_id, "Set-list performance version identifier")


@dataclass(frozen=True, slots=True)
class Performance:
    """A completed or planned live performance event."""

    identifier: str
    venue_identifier: str
    set_list_identifier: str
    date: date
    actual_duration_minutes: int
    overall_confidence: Decimal
    audience_engagement: Decimal
    mistakes: int
    recovery_quality: Decimal
    notes: str = ""

    def __post_init__(self) -> None:
        require_text(self.identifier, "Performance identifier")
        require_text(self.venue_identifier, "Venue identifier")
        require_text(self.set_list_identifier, "Set-list identifier")
        require_non_negative_int(self.actual_duration_minutes, "Actual duration")
        require_non_negative_int(self.mistakes, "Mistakes")
        require_rating(self.overall_confidence, "Overall confidence")
        require_rating(self.audience_engagement, "Audience engagement")
        require_rating(self.recovery_quality, "Recovery quality")
