"""Practice session model."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from open_mic_lab.domain.validation import (
    require_non_negative_int,
    require_positive_int,
    require_rating,
    require_text,
)


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
