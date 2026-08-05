"""Chapter 4 services for arrangement experiments, comparison, and timelines."""

# ruff: noqa: D102

from collections.abc import Callable
from dataclasses import dataclass, replace
from typing import Any

from open_mic_lab.domain import Arrangement, ArrangementExperimentRecord, Instrument
from open_mic_lab.domain.pitch import VocalNote


@dataclass(frozen=True, slots=True)
class ArrangementComparison:
    """Neutral comparison that explains arrangement tradeoffs."""

    left_identifier: str
    right_identifier: str
    differences: tuple[str, ...]
    left_tradeoffs: tuple[str, ...]
    right_tradeoffs: tuple[str, ...]
    reflection: str


@dataclass(frozen=True, slots=True)
class ArrangementTimelineEntry:
    """One deterministic structural arrangement event."""

    start_seconds: int
    section: str
    duration_seconds: int
    notes: str

    @property
    def start_time(self) -> str:
        minutes, seconds = divmod(self.start_seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"


class ArrangementExperimentService:
    """Return copied arrangements for every experiment so originals stay inspectable."""

    def transpose(
        self, arrangement: Arrangement, destination_key: str, semitones: int
    ) -> Arrangement:
        VocalNote.parse(f"{destination_key}4")
        return self._copy(
            arrangement,
            "transpose",
            f"transpose-{destination_key.lower().replace('#', 'sharp').replace('b', 'flat')}",
            f"Transposed {semitones:+} semitones to {destination_key}.",
            performance_key=destination_key,
        )

    def simplify_accompaniment(self, arrangement: Arrangement) -> Arrangement:
        return self._copy(
            arrangement,
            "simplify accompaniment",
            "simplified",
            "Simplified accompaniment texture.",
            simplification_level=arrangement.simplification_level + 1,
            notes=(arrangement.notes + " Simplified accompaniment.").strip(),
        )

    def alter_tempo(self, arrangement: Arrangement, target_tempo_bpm: int) -> Arrangement:
        return self._copy(
            arrangement,
            "alter tempo",
            f"tempo-{target_tempo_bpm}",
            f"Changed target tempo to {target_tempo_bpm} bpm.",
            target_tempo_bpm=target_tempo_bpm,
        )

    def shorten_introduction(self, arrangement: Arrangement) -> Arrangement:
        return self._copy(
            arrangement,
            "shorten introduction",
            "short-intro",
            "Shortened the introduction for a faster audience entry.",
            introduction_structure=f"shortened {arrangement.introduction_structure}",
        )

    def extend_ending(self, arrangement: Arrangement) -> Arrangement:
        return self._copy(
            arrangement,
            "extend ending",
            "extended-ending",
            "Extended the ending to create a clearer final impression.",
            ending_structure=f"extended {arrangement.ending_structure}",
        )

    def remove_section(self, arrangement: Arrangement, section: str) -> Arrangement:
        order = tuple(item for item in arrangement.verse_order if item != section)
        if not order:
            raise ValueError("Cannot remove every arrangement section.")
        return self._copy(
            arrangement,
            "remove section",
            f"remove-{self._slug(section)}",
            f"Removed section: {section}.",
            verse_order=order,
        )

    def duplicate_chorus(self, arrangement: Arrangement) -> Arrangement:
        return self._copy(
            arrangement,
            "duplicate chorus",
            "extra-chorus",
            "Added one chorus repetition.",
            chorus_repetitions=arrangement.chorus_repetitions + 1,
        )

    def change_groove(self, arrangement: Arrangement, groove_style: str) -> Arrangement:
        return self._copy(
            arrangement,
            "change groove",
            f"groove-{self._slug(groove_style)}",
            f"Changed groove/style to {groove_style}.",
            groove_style=groove_style,
        )

    def switch_primary_instrument(
        self, arrangement: Arrangement, instrument: Instrument
    ) -> Arrangement:
        return self._copy(
            arrangement,
            "switch primary instrument",
            f"instrument-{self._slug(instrument.value)}",
            f"Switched primary instrument to {instrument.value}.",
            primary_instrument=instrument,
        )

    def combine(
        self, arrangement: Arrangement, *steps: Callable[[Arrangement], Arrangement]
    ) -> Arrangement:
        current = arrangement
        for step in steps:
            current = step(current)
        return current

    def _copy(
        self,
        arrangement: Arrangement,
        name: str,
        slug: str,
        summary: str,
        **changes: Any,
    ) -> Arrangement:
        record = ArrangementExperimentRecord(name, arrangement.identifier, summary)
        return replace(
            arrangement,
            identifier=f"{arrangement.identifier}-{slug}",
            name=f"{arrangement.name} — {name}",
            history=arrangement.history + (record,),
            **changes,
        )

    @staticmethod
    def _slug(value: str) -> str:
        return value.lower().replace("/", "-").replace(" ", "-")


class ArrangementAnalysisService:
    """Compare arrangements without declaring an artistic winner."""

    def compare(self, left: Arrangement, right: Arrangement) -> ArrangementComparison:
        differences: list[str] = []
        left_tradeoffs: list[str] = []
        right_tradeoffs: list[str] = []
        if left.primary_instrument != right.primary_instrument:
            differences.append(
                f"Instrument: {left.primary_instrument.value} vs {right.primary_instrument.value}."
            )
            left_tradeoffs.append("Keeps the existing instrumental muscle memory.")
            right_tradeoffs.append("May create a new color but adds setup and practice needs.")
        if left.performance_key != right.performance_key:
            differences.append(f"Key: {left.performance_key} vs {right.performance_key}.")
            right_tradeoffs.append("May improve vocal comfort while changing familiar fingerings.")
        if left.target_tempo_bpm != right.target_tempo_bpm:
            differences.append(f"Tempo: {left.target_tempo_bpm} vs {right.target_tempo_bpm} bpm.")
            right_tradeoffs.append("Tempo changes can improve control but alter audience energy.")
        if left.simplification_level != right.simplification_level:
            differences.append(
                "Simplification: level "
                f"{left.simplification_level} vs {right.simplification_level}."
            )
            right_tradeoffs.append("Simplification may free attention for singing and recovery.")
        if left.introduction_structure != right.introduction_structure:
            differences.append("Introduction structure changed.")
        if left.ending_structure != right.ending_structure:
            differences.append("Ending structure changed.")
        if left.audience_participation_cues != right.audience_participation_cues:
            differences.append("Audience participation cues changed.")
        return ArrangementComparison(
            left.identifier,
            right.identifier,
            tuple(differences) or ("No structural differences detected.",),
            tuple(left_tradeoffs) or ("Preserves a known baseline for comparison.",),
            tuple(right_tradeoffs) or ("Offers a different intention to test safely.",),
            "Choose the arrangement that best serves this performer, room, "
            "and moment—not an abstract winner.",
        )


class ArrangementTimelineService:
    """Generate deterministic structural timing estimates from arrangement form."""

    def timeline(self, arrangement: Arrangement) -> tuple[ArrangementTimelineEntry, ...]:
        entries: list[ArrangementTimelineEntry] = []
        elapsed = 0
        seconds_per_beat = 60 / arrangement.target_tempo_bpm
        base = max(18, round(seconds_per_beat * 32))
        for section in arrangement.verse_order:
            multiplier = 1.0
            if "Intro" in section:
                multiplier = 0.5 if "short" in arrangement.introduction_structure else 0.75
            elif "Bridge" in section or "Instrumental" in section or "solo" in section.lower():
                multiplier = 0.8
            elif "Ending" in section or "Refrain" in section:
                multiplier = 1.2 if "extended" in arrangement.ending_structure else 0.75
            duration = max(8, round(base * multiplier))
            entries.append(
                ArrangementTimelineEntry(
                    elapsed, section, duration, self._notes(section, arrangement)
                )
            )
            elapsed += duration
        return tuple(entries)

    def _notes(self, section: str, arrangement: Arrangement) -> str:
        if "Intro" in section:
            return arrangement.introduction_structure
        if "Ending" in section or "Refrain" in section:
            cues = "; ".join(arrangement.audience_participation_cues)
            return f"{arrangement.ending_structure}{f' — {cues}' if cues else ''}"
        if section in arrangement.solo_sections:
            return "solo section"
        return arrangement.dynamic_profile
