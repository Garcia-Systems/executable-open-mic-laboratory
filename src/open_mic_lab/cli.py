"""Command-line interface for the executable open mic laboratory."""

import argparse
from collections.abc import Sequence

from open_mic_lab.domain import Repertoire, SetList
from open_mic_lab.sample_data import (
    build_sample_repertoire,
    sample_practice_sessions,
    sample_setlist,
    sample_venue,
)
from open_mic_lab.services.readiness_service import calculate_readiness
from open_mic_lab.services.repertoire_service import describe_repertoire
from open_mic_lab.services.setlist_service import analyze_setlist


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description="Executable Open Mic Laboratory")
    sub = parser.add_subparsers(dest="command", required=True)
    rep = sub.add_parser("repertoire", help="Explore sample repertoire")
    rep_sub = rep.add_subparsers(dest="repertoire_command", required=True)
    rep_sub.add_parser("list", help="List all sample performance versions")
    rep_sub.add_parser("ready", help="List performance-ready versions")
    ready = sub.add_parser("readiness", help="Calculate readiness")
    ready_sub = ready.add_subparsers(dest="readiness_command", required=True)
    show = ready_sub.add_parser("show", help="Show readiness for a version")
    show.add_argument("version_id")
    setlist = sub.add_parser("setlist", help="Work with sample set lists")
    set_sub = setlist.add_subparsers(dest="setlist_command", required=True)
    set_sub.add_parser("sample", help="Print the sample set list")
    set_sub.add_parser("analyze", help="Analyze the sample set list")
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
    elif args.command == "readiness" and args.readiness_command == "show":
        result = calculate_readiness(rep.get_version(args.version_id), sample_practice_sessions())
        print(f"Readiness for {args.version_id}: {result.score}/100 ({result.category})")
        for item in result.breakdown:
            print(f"- {item}")
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


if __name__ == "__main__":
    raise SystemExit(main())
