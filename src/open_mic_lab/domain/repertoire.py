"""Repertoire aggregate."""

from dataclasses import dataclass, field

from open_mic_lab.domain.arrangement import Arrangement
from open_mic_lab.domain.enums import Genre, Instrument, Mood, PerformanceStatus
from open_mic_lab.domain.performance import PerformanceVersion
from open_mic_lab.domain.song import Song


@dataclass(slots=True)
class Repertoire:
    """A collection of songs and safely copied performance versions."""

    songs: dict[str, Song] = field(default_factory=dict)
    versions: dict[str, PerformanceVersion] = field(default_factory=dict)
    arrangements: dict[str, Arrangement] = field(default_factory=dict)

    def add_song(self, song: Song) -> None:
        """Add a song, rejecting duplicate identifiers."""
        if song.identifier in self.songs:
            raise ValueError(f"Song identifier '{song.identifier}' already exists.")
        self.songs[song.identifier] = song

    def add_arrangement(self, arrangement: Arrangement) -> None:
        """Add an arrangement, rejecting duplicates and unknown version references."""
        if arrangement.identifier in self.arrangements:
            raise ValueError(f"Arrangement identifier '{arrangement.identifier}' already exists.")
        if arrangement.source_performance_version_identifier not in self.versions:
            raise ValueError(
                f"Arrangement '{arrangement.identifier}' references unknown performance version "
                f"'{arrangement.source_performance_version_identifier}'."
            )
        self.arrangements[arrangement.identifier] = arrangement

    def add_performance_version(self, version: PerformanceVersion) -> None:
        """Add a version, rejecting duplicates and unknown song references."""
        if version.identifier in self.versions:
            raise ValueError(
                f"Performance version identifier '{version.identifier}' already exists."
            )
        if version.song_identifier not in self.songs:
            raise ValueError(
                f"Performance version '{version.identifier}' references unknown song "
                f"'{version.song_identifier}'."
            )
        self.versions[version.identifier] = version

    def get_arrangement(self, identifier: str) -> Arrangement:
        """Return an arrangement by identifier."""
        try:
            return self.arrangements[identifier]
        except KeyError as exc:
            raise KeyError(f"No arrangement found for identifier '{identifier}'.") from exc

    def get_song(self, identifier: str) -> Song:
        """Return a song by identifier."""
        try:
            return self.songs[identifier]
        except KeyError as exc:
            raise KeyError(f"No song found for identifier '{identifier}'.") from exc

    def get_version(self, identifier: str) -> PerformanceVersion:
        """Return a performance version by identifier."""
        try:
            return self.versions[identifier]
        except KeyError as exc:
            raise KeyError(f"No performance version found for identifier '{identifier}'.") from exc

    def list_ready_versions(self) -> tuple[PerformanceVersion, ...]:
        """List versions marked performance ready."""
        return self.filter_by_status(PerformanceStatus.PERFORMANCE_READY)

    def filter_by_genre(self, genre: Genre) -> tuple[PerformanceVersion, ...]:
        """List versions whose songs match a genre."""
        return tuple(
            v for v in self.versions.values() if self.songs[v.song_identifier].genre == genre
        )

    def filter_by_instrument(self, instrument: Instrument) -> tuple[PerformanceVersion, ...]:
        """List versions using a primary instrument."""
        return tuple(v for v in self.versions.values() if v.primary_instrument == instrument)

    def filter_by_mood(self, mood: Mood) -> tuple[PerformanceVersion, ...]:
        """List versions whose songs match a mood."""
        return tuple(
            v for v in self.versions.values() if self.songs[v.song_identifier].mood == mood
        )

    def filter_by_status(self, status: PerformanceStatus) -> tuple[PerformanceVersion, ...]:
        """List versions with the requested workflow status."""
        return tuple(v for v in self.versions.values() if v.performance_status == status)
