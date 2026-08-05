"""Debug laboratory for Chapter 2 repertoire engineering."""

from open_mic_lab.sample_data import build_sample_repertoire
from open_mic_lab.services.repertoire_service import RepertoireEngineeringService


def main() -> int:
    """Run a small deterministic repertoire-engineering scenario."""
    repertoire = build_sample_repertoire()
    service = RepertoireEngineeringService()

    # BREAKPOINT: Inspect repertoire loading, version metadata, and lifecycle status.
    version_count = len(repertoire.versions)
    song_count = len(repertoire.songs)

    # BREAKPOINT: Step Into analysis and inspect distributions plus observations.
    analysis = service.analyze(repertoire)
    genre_distribution = analysis.genre_distribution
    key_distribution = analysis.key_distribution
    neglected_version_ids = analysis.neglected_version_ids

    # BREAKPOINT: Step Into deterministic gap detection and inspect category recommendations.
    gaps = service.gaps(repertoire)

    # BREAKPOINT: Step Into priority generation and inspect scores and reasons.
    priorities = service.priorities(repertoire)
    top_priority = priorities[0]

    # BREAKPOINT: Step Into health scoring and inspect each component of the formula.
    health = service.health(repertoire)

    print("Chapter 2 repertoire engineering debug lab")
    print(f"Loaded {song_count} songs and {version_count} performance versions.")
    print(f"Genres: {genre_distribution}")
    print(f"Keys: {key_distribution}")
    print(f"Neglected: {neglected_version_ids}")
    print(f"Gaps: {gaps}")
    print(f"Top priority: {top_priority.version_id} ({top_priority.score})")
    print(f"Health: {health.score}/100")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
