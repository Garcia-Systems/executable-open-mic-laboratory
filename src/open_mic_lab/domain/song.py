"""Song domain model."""

from dataclasses import dataclass
from decimal import Decimal

from open_mic_lab.domain.enums import Genre, Mood
from open_mic_lab.domain.validation import require_positive_int, require_rating, require_text


@dataclass(frozen=True, slots=True)
class Song:
    """The underlying musical work, independent of a performer's arrangement."""

    identifier: str
    title: str
    artist: str
    genre: Genre
    original_key: str
    original_tempo_bpm: int
    time_signature: str
    mood: Mood
    estimated_audience_familiarity: Decimal
    story_opportunity: Decimal
    audience_participation_potential: Decimal

    def __post_init__(self) -> None:
        require_text(self.identifier, "Song identifier")
        require_text(self.title, "Song title")
        require_text(self.artist, "Song artist")
        require_text(self.original_key, "Original key")
        require_positive_int(self.original_tempo_bpm, "Original tempo")
        require_text(self.time_signature, "Time signature")
        require_rating(self.estimated_audience_familiarity, "Audience familiarity")
        require_rating(self.story_opportunity, "Story opportunity")
        require_rating(self.audience_participation_potential, "Participation potential")
