"""Command-line interface for the executable open mic laboratory."""

import argparse
from collections.abc import Sequence

from open_mic_lab.domain import Repertoire, SetList
from open_mic_lab.sample_data import (
    build_sample_repertoire,
    sample_practice_sessions,
    sample_selection_scenarios,
    sample_selection_venue,
    sample_setlist,
    sample_venue,
)
from open_mic_lab.services.experiment_service import PerformanceVersionExperimentService
from open_mic_lab.services.readiness_service import calculate_readiness
from open_mic_lab.services.repertoire_service import (
    RepertoireEngineeringService,
    describe_repertoire,
)
from open_mic_lab.services.setlist_service import analyze_setlist
from open_mic_lab.services.suitability_service import SongSuitabilityService


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description="Executable Open Mic Laboratory")
    sub = parser.add_subparsers(dest="command", required=True)
    rep = sub.add_parser("repertoire", help="Explore sample repertoire")
    rep_sub = rep.add_subparsers(dest="repertoire_command", required=True)
    rep_sub.add_parser("list", help="List all sample performance versions")
    rep_sub.add_parser("ready", help="List performance-ready versions")
    for name in ("summary", "gaps", "health", "priorities", "neglected", "diversity"):
        rep_sub.add_parser(name, help=f"Show repertoire {name}")
    ready = sub.add_parser("readiness", help="Calculate readiness")
    ready_sub = ready.add_subparsers(dest="readiness_command", required=True)
    show = ready_sub.add_parser("show", help="Show readiness for a version")
    show.add_argument("version_id")
    setlist = sub.add_parser("setlist", help="Work with sample set lists")
    set_sub = setlist.add_subparsers(dest="setlist_command", required=True)
    set_sub.add_parser("sample", help="Print the sample set list")
    set_sub.add_parser("analyze", help="Analyze the sample set list")
    songs = sub.add_parser("songs", help="Run the Song Suitability Laboratory")
    songs_sub = songs.add_subparsers(dest="songs_command", required=True)
    eval_cmd = songs_sub.add_parser("evaluate", help="Evaluate one performance version")
    eval_cmd.add_argument("version_id")
    eval_cmd.add_argument("--scenario", required=True)
    compare = songs_sub.add_parser("compare", help="Compare candidate performance versions")
    compare.add_argument("--scenario", required=True)
    compare.add_argument("version_ids", nargs="*")
    explain = songs_sub.add_parser("explain", help="Explain one suitability result")
    explain.add_argument("version_id")
    explain.add_argument("--scenario", required=True)
    songs_sub.add_parser("scenarios", help="List deterministic Chapter 1 scenarios")
    sub.add_parser("chapter-one-demo", help="Run the Chapter 1 song suitability demo")
    sub.add_parser("chapter-two-demo", help="Run the Chapter 2 repertoire engineering demo")
    sub.add_parser("demo", help="Run a deterministic educational walkthrough")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI."""
    args = build_parser().parse_args(argv)
    rep = build_sample_repertoire()
    if args.command == "repertoire":
        if args.repertoire_command == "list":
            for line in describe_repertoire(rep):
                print(line)
        elif args.repertoire_command == "ready":
            for version in rep.list_ready_versions():
                song = rep.get_song(version.song_identifier)
                print(f"{version.identifier}: {song.title} ({version.primary_instrument.value})")
        else:
            _run_repertoire_engineering(args.repertoire_command, rep)
    elif args.command == "readiness" and args.readiness_command == "show":
        result = calculate_readiness(rep.get_version(args.version_id), sample_practice_sessions())
        print(f"Readiness for {args.version_id}: {result.score}/100 ({result.category})")
        for item in result.breakdown:
            print(f"- {item}")
    elif args.command == "songs":
        return _run_songs(args, rep)
    elif args.command == "chapter-one-demo":
        _run_chapter_one_demo(rep)
    elif args.command == "chapter-two-demo":
        _run_chapter_two_demo(rep)
    elif args.command == "setlist":
        set_list = sample_setlist()
        if args.setlist_command == "sample":
            print(f"{set_list.name} ({set_list.target_duration_minutes} minutes)")
            for index, version_id in enumerate(set_list.ordered_version_identifiers, start=1):
                song = rep.get_song(rep.get_version(version_id).song_identifier)
                print(f"{index}. {version_id}: {song.title}")
        elif args.setlist_command == "analyze":
            _print_analysis(set_list, rep)
    elif args.command == "demo":
        _run_demo(rep)
    return 0


def _print_analysis(set_list: SetList, rep: Repertoire) -> None:
    analysis = analyze_setlist(set_list, rep, sample_venue())
    print(f"Estimated duration: {analysis.estimated_duration_minutes} minutes")
    print(f"Fits venue: {analysis.fits_venue}")
    print(f"Tempo: {analysis.tempo_summary}")
    print(f"Genres: {analysis.genre_distribution}")
    print(f"Moods: {analysis.mood_distribution}")
    for warning in analysis.warnings:
        print(f"Warning: {warning}")


def _run_demo(rep: Repertoire) -> None:
    print("Executable Open Mic Laboratory demo")
    print("\nSample repertoire:")
    for line in describe_repertoire(rep):
        print(f"- {line}")
    print("\nReadiness snapshots:")
    for version_id in ("river-guitar-original", "river-guitar-lowered", "train-guitar-closer"):
        result = calculate_readiness(rep.get_version(version_id), sample_practice_sessions())
        print(f"- {version_id}: {result.score}/100 ({result.category})")
    print("\nSample 15-minute set analysis:")
    _print_analysis(sample_setlist(), rep)
    print("\nObservation: changing key, tempo, order, or recovery skill changes the system.")


def _scenario(name: str):  # type: ignore[no-untyped-def]
    scenarios = sample_selection_scenarios()
    if name not in scenarios:
        raise SystemExit(f"Unknown scenario '{name}'. Try: {', '.join(sorted(scenarios))}.")
    profile = scenarios[name]
    return profile, sample_selection_venue(profile.venue_identifier)


def _run_songs(args, rep: Repertoire) -> int:  # type: ignore[no-untyped-def]
    service = SongSuitabilityService()
    if args.songs_command == "scenarios":
        for key, profile in sample_selection_scenarios().items():
            print(f"{key}: {profile.name} ({profile.slot_duration_minutes} minutes)")
        return 0
    profile, venue = _scenario(args.scenario)
    if args.songs_command in {"evaluate", "explain"}:
        try:
            version = rep.get_version(args.version_id)
        except KeyError as exc:
            raise SystemExit(str(exc)) from exc
        result = service.evaluate(version, rep, profile, venue)
        _print_suitability(result, rep)
        if args.songs_command == "explain":
            print("Explanation:")
            print(result.explanation)
            for criterion in result.criteria:
                print(
                    f"- {criterion.name}: {criterion.score}/100 "
                    f"(weight {criterion.weight:.2f}) — {criterion.explanation}"
                )
        return 0
    if args.songs_command == "compare":
        versions = (
            tuple(rep.get_version(v) for v in args.version_ids)
            if args.version_ids
            else tuple(rep.versions.values())
        )
        comparison = service.compare(versions, rep, profile, venue)
        print(f"Song suitability comparison — {profile.name}")
        print("version | title | key | instrument | score | completeness | recommendation")
        for result in comparison.results:
            version = rep.get_version(result.version_id)
            song = rep.get_song(version.song_identifier)
            print(
                f"{result.version_id} | {song.title} | {version.performance_key} | "
                f"{version.primary_instrument.value} | {result.score} | "
                f"{result.completeness}% | {result.recommendation}"
            )
            print(f"  strongest: {result.strongest_factor}")
            print(f"  concern: {result.largest_concern}")
        for obs in comparison.observations:
            print(f"Observation: {obs}")
        return 0
    return 0


def _print_suitability(result, rep: Repertoire) -> None:  # type: ignore[no-untyped-def]
    version = rep.get_version(result.version_id) if result.version_id in rep.versions else None
    song = rep.get_song(version.song_identifier) if version else None
    if version and song:
        print(f"{song.title} — {song.artist}")
        print(
            f"Version: {version.identifier} | key {version.performance_key} | "
            f"{version.primary_instrument.value}"
        )
    print(f"Suitability: {result.score}/100 | completeness {result.completeness}%")
    print(f"Recommendation: {result.recommendation}")
    for factor in result.positive_factors:
        print(f"Strong factor: {factor}")
    for concern in result.concerns:
        print(f"Concern: {concern}")
    for adaptation in result.adaptations:
        print(f"Suggested experiment: {adaptation}")


def _run_chapter_one_demo(rep: Repertoire) -> None:
    print("Chapter 1 — Choosing Songs")
    profile, venue = _scenario("coffeehouse")
    service = SongSuitabilityService()
    comparison = service.compare(tuple(rep.versions.values()), rep, profile, venue)
    print(f"Scenario: {profile.name}")
    for result in comparison.results[:5]:
        version = rep.get_version(result.version_id)
        song = rep.get_song(version.song_identifier)
        print(f"- {song.title}: {result.score}/100 ({result.recommendation})")
    print("The highest score is not automatically the only reasonable artistic choice.")
    risky = rep.get_version("window-guitar-original-feature")
    before = service.evaluate(risky, rep, profile, venue)
    print(f"Vocal-range concern before experiment: {before.largest_concern}")
    experiment = PerformanceVersionExperimentService().transpose(risky, "F", -2)
    after = service.evaluate(experiment, rep, profile, venue)
    print(
        f"After lowering by two semitones: {after.score}/100, "
        f"range {experiment.required_vocal_range}"
    )
    print("Tradeoff: an original can be unfamiliar yet carry high personal connection.")
    print(
        "Reflection: Would you choose the highest-scoring song, the safest song, "
        "or the song that best introduces you tonight?"
    )


def _run_repertoire_engineering(command: str, rep: Repertoire) -> None:
    service = RepertoireEngineeringService()
    analysis = service.analyze(rep)
    if command == "summary":
        print("Repertoire Engineering Summary")
        for obs in analysis.observations:
            print(f"Observation: {obs}")
        print(service.text_report("Genre Distribution", analysis.genre_distribution))
        print(service.text_report("Readiness", analysis.readiness_distribution))
    elif command == "gaps":
        for gap in service.gaps(rep):
            print(f"Gap: {gap}")
    elif command == "health":
        health = service.health(rep)
        print(f"Repertoire health: {health.score}/100")
        print(
            f"diversity={health.diversity} maintenance={health.maintenance} "
            f"readiness={health.readiness} balance={health.balance} "
            f"role_coverage={health.role_coverage}"
        )
        print(health.explanation)
    elif command == "priorities":
        for item in service.priorities(rep):
            print(f"{item.version_id}: {item.score}")
            for reason in item.reasons:
                print(f"- {reason}")
    elif command == "neglected":
        for version_id in analysis.neglected_version_ids:
            print(version_id)
    elif command == "diversity":
        print(f"Diversity score: {analysis.diversity_score}/100")
        print(service.text_report("Instrument Distribution", analysis.instrument_distribution))


def _run_chapter_two_demo(rep: Repertoire) -> None:
    print("Chapter 2 — Repertoire Engineering")
    service = RepertoireEngineeringService()
    _run_repertoire_engineering("summary", rep)
    print("\nGaps")
    for gap in service.gaps(rep):
        print(f"- {gap}")
    print("\nTop learning priorities")
    for item in service.priorities(rep)[:3]:
        print(f"- {item.version_id}: {item.reasons[0]}")
    health = service.health(rep)
    print(f"\nHealth formula result: {health.score}/100")


if __name__ == "__main__":
    raise SystemExit(main())
