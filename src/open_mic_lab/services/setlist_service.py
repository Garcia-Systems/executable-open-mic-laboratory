"""Deterministic set-list analysis helpers."""

from collections import Counter
from dataclasses import dataclass

from open_mic_lab.domain.enums import Mood
from open_mic_lab.domain.performance import SetList
from open_mic_lab.domain.repertoire import Repertoire
from open_mic_lab.domain.venue import Venue
from open_mic_lab.services.readiness_service import calculate_readiness

SECONDS_PER_SONG_BUFFER = 20


@dataclass(frozen=True, slots=True)
class SetListAnalysis:
    """Friendly set-list analysis without claiming objective correctness."""

    estimated_duration_minutes: int
    fits_venue: bool
    genre_distribution: dict[str, int]
    mood_distribution: dict[str, int]
    tempo_summary: str
    warnings: tuple[str, ...]


def estimated_duration_minutes(set_list: SetList, repertoire: Repertoire) -> int:
    """Estimate duration from tempo, intro length, and a fixed transition buffer."""
    total_seconds = 0
    for version_id in set_list.ordered_version_identifiers:
        version = repertoire.get_version(version_id)
        song_seconds = 180 + max(0, 120 - version.target_tempo_bpm) // 2
        total_seconds += (
            song_seconds + version.introduction_length_seconds + SECONDS_PER_SONG_BUFFER
        )
    return round(total_seconds / 60)


def analyze_setlist(set_list: SetList, repertoire: Repertoire, venue: Venue) -> SetListAnalysis:
    """Analyze contrast, duration fit, and closer placement."""
    versions = [
        repertoire.get_version(version_id) for version_id in set_list.ordered_version_identifiers
    ]
    songs = [repertoire.get_song(version.song_identifier) for version in versions]
    duration = estimated_duration_minutes(set_list, repertoire)
    warnings: list[str] = []
    limit = min(set_list.target_duration_minutes, venue.typical_set_duration_minutes)
    if duration > limit:
        warnings.append(f"Estimated {duration} minutes exceeds the {limit}-minute planning limit.")
    if len({song.genre for song in songs}) == 1 and len(songs) > 1:
        warnings.append("All songs share one genre; consider whether the set needs more contrast.")
    if len({song.mood for song in songs}) == 1 and len(songs) > 1:
        warnings.append("All songs share one mood; the emotional arc may feel flat.")
    if songs and all(song.mood is not Mood.ENERGETIC for song in songs):
        warnings.append(
            "No energetic song appears in this set; that can be intimate, but note the choice."
        )
    if versions:
        strongest = max(
            versions,
            key=lambda version: (
                calculate_readiness(version).score,
                repertoire.get_song(version.song_identifier).audience_participation_potential,
                repertoire.get_song(version.song_identifier).estimated_audience_familiarity,
            ),
        )
        if versions[-1].identifier != strongest.identifier:
            warnings.append(
                f"The strongest available closer appears to be {strongest.identifier}; "
                "it is not last."
            )
    tempos = [version.target_tempo_bpm for version in versions]
    tempo_summary = "no songs" if not tempos else f"min {min(tempos)} bpm, max {max(tempos)} bpm"
    return SetListAnalysis(
        estimated_duration_minutes=duration,
        fits_venue=duration <= limit,
        genre_distribution=dict(Counter(song.genre.value for song in songs)),
        mood_distribution=dict(Counter(song.mood.value for song in songs)),
        tempo_summary=tempo_summary,
        warnings=tuple(warnings),
    )
