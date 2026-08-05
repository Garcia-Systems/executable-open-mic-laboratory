"""Convenience queries for repertoire displays."""

from open_mic_lab.domain.repertoire import Repertoire


def describe_repertoire(repertoire: Repertoire) -> tuple[str, ...]:
    """Return deterministic one-line descriptions of all performance versions."""
    lines: list[str] = []
    for version in repertoire.versions.values():
        song = repertoire.get_song(version.song_identifier)
        lines.append(
            f"{version.identifier}: {song.title} by {song.artist} | {song.genre.value}, "
            f"{song.mood.value} | {version.primary_instrument.value} | "
            f"{version.performance_status.value}"
        )
    return tuple(lines)
