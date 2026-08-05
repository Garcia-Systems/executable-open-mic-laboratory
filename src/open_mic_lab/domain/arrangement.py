"""Arrangement domain model for intentional performance versions."""

from dataclasses import dataclass

from open_mic_lab.domain.enums import Instrument
from open_mic_lab.domain.validation import (
    require_non_negative_int,
    require_positive_int,
    require_text,
)


@dataclass(frozen=True, slots=True)
class ArrangementExperimentRecord:
    """One immutable step in an arrangement's evolution."""

    experiment_name: str
    source_arrangement_identifier: str
    summary: str

    def __post_init__(self) -> None:
        require_text(self.experiment_name, "Arrangement experiment name")
        require_text(self.source_arrangement_identifier, "Source arrangement identifier")
        require_text(self.summary, "Arrangement experiment summary")


@dataclass(frozen=True, slots=True)
class Arrangement:
    """How a performer intentionally shapes one performance version of a song.

    Arrangements are separate from songs because the song is the underlying work,
    while instrumentation, key, tempo, form, and audience cues belong to a
    performer's evolving version. Keeping this object separate lets learners copy
    an arrangement for experiments without rewriting the song or erasing the
    source performance version.
    """

    identifier: str
    name: str
    source_performance_version_identifier: str
    primary_instrument: Instrument
    supporting_instruments: tuple[Instrument, ...]
    performance_key: str
    target_tempo_bpm: int
    groove_style: str
    introduction_structure: str
    ending_structure: str
    verse_order: tuple[str, ...]
    chorus_repetitions: int
    uses_bridge: bool
    solo_sections: tuple[str, ...]
    audience_participation_cues: tuple[str, ...]
    simplification_level: int
    dynamic_profile: str
    notes: str = ""
    history: tuple[ArrangementExperimentRecord, ...] = ()

    def __post_init__(self) -> None:
        require_text(self.identifier, "Arrangement identifier")
        require_text(self.name, "Arrangement name")
        require_text(self.source_performance_version_identifier, "Source performance version")
        require_text(self.performance_key, "Performance key")
        require_positive_int(self.target_tempo_bpm, "Target tempo")
        require_text(self.groove_style, "Groove/style")
        require_text(self.introduction_structure, "Introduction structure")
        require_text(self.ending_structure, "Ending structure")
        require_non_negative_int(self.chorus_repetitions, "Chorus repetitions")
        require_non_negative_int(self.simplification_level, "Simplification level")
        require_text(self.dynamic_profile, "Dynamic profile")
        if not self.verse_order:
            raise ValueError("Arrangement needs at least one structural section.")
        for section in self.verse_order:
            require_text(section, "Verse/section order item")
        for section in self.solo_sections:
            require_text(section, "Solo section")
        for cue in self.audience_participation_cues:
            require_text(cue, "Audience participation cue")
