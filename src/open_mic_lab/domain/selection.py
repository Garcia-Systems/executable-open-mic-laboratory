"""Song-selection profile for a particular performance opportunity."""

from dataclasses import dataclass, field
from decimal import Decimal

from open_mic_lab.domain.enums import Difficulty, EnergyLevel, Instrument, Mood, PerformanceRole
from open_mic_lab.domain.pitch import VocalRange
from open_mic_lab.domain.validation import require_positive_int, require_rating, require_text


@dataclass(frozen=True, slots=True)
class SongSelectionProfile:
    """What matters for one transparent song-selection decision."""

    identifier: str
    name: str
    performer_experience_level: str
    preferred_instrument: Instrument | None
    comfortable_vocal_range: VocalRange | None
    maximum_arrangement_difficulty: Difficulty
    desired_mood: Mood | None
    desired_energy_level: EnergyLevel | None
    target_audience_familiarity: tuple[Decimal, Decimal]
    prefer_familiar_songs: bool
    desire_audience_participation: Decimal
    desire_storytelling: Decimal
    willingness_to_transpose: bool
    willingness_to_simplify: bool
    desired_performance_role: PerformanceRole
    venue_identifier: str
    slot_duration_minutes: int
    strict_vocal_limit: VocalRange | None = None
    available_instruments: tuple[Instrument, ...] = field(default_factory=tuple)
    weights: dict[str, Decimal] = field(default_factory=dict)

    def __post_init__(self) -> None:
        require_text(self.identifier, "Selection profile identifier")
        require_text(self.name, "Selection profile name")
        require_text(self.performer_experience_level, "Performer experience level")
        require_text(self.venue_identifier, "Venue identifier")
        require_positive_int(self.slot_duration_minutes, "Slot duration")
        low, high = self.target_audience_familiarity
        require_rating(low, "Target audience familiarity low")
        require_rating(high, "Target audience familiarity high")
        if low > high:
            raise ValueError("Target audience familiarity low cannot exceed high.")
        require_rating(self.desire_audience_participation, "Audience participation desire")
        require_rating(self.desire_storytelling, "Storytelling desire")
        for name, weight in self.weights.items():
            require_text(name, "Criterion name")
            if weight < 0:
                raise ValueError("Criterion weights cannot be negative.")
