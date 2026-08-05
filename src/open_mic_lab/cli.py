"""Command-line interface for the executable open mic laboratory."""

import argparse
from collections.abc import Sequence

from open_mic_lab.domain import (
    Arrangement,
    CoordinationExperiment,
    PracticeGoal,
    Repertoire,
    SetList,
)
from open_mic_lab.sample_data import (
    build_sample_repertoire,
    sample_coordination_profile,
    sample_practice_sessions,
    sample_selection_scenarios,
    sample_selection_venue,
    sample_set_scenarios,
    sample_setlist,
    sample_venue,
)
from open_mic_lab.services.arrangement_service import (
    ArrangementAnalysisService,
    ArrangementExperimentService,
    ArrangementTimelineService,
)
from open_mic_lab.services.coordination_service import (
    CoordinationAnalysisService,
    CoordinationExperimentService,
    TempoLadderService,
)
from open_mic_lab.services.experiment_service import PerformanceVersionExperimentService
from open_mic_lab.services.practice_service import (
    PracticeAnalyticsService,
    PracticePlanningInput,
    PracticePlanningService,
)
from open_mic_lab.services.readiness_service import calculate_readiness
from open_mic_lab.services.repertoire_service import (
    RepertoireEngineeringService,
    describe_repertoire,
)
from open_mic_lab.services.set_builder_service import SetBuilderService
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
    set_builder = sub.add_parser("set", help="Engineer complete Chapter 3 sets")
    set_builder_sub = set_builder.add_subparsers(dest="set_command", required=True)
    for name in ("summary", "timeline", "analyze", "compare"):
        set_builder_sub.add_parser(name, help=f"Set {name}")
    exp = set_builder_sub.add_parser("experiment", help="Run immutable set experiments")
    exp_sub = exp.add_subparsers(dest="experiment_command", required=True)
    swap = exp_sub.add_parser("swap", help="Swap two songs")
    swap.add_argument("first")
    swap.add_argument("second")
    opener = exp_sub.add_parser("opener", help="Move a song to opener")
    opener.add_argument("version_id")
    closer = exp_sub.add_parser("closer", help="Move a song to closer")
    closer.add_argument("version_id")
    transition = exp_sub.add_parser("transition", help="Insert a short transition")
    transition.add_argument("after_version_id")
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
    arrangement = sub.add_parser("arrangement", help="Run Chapter 4 arrangement experiments")
    arr_sub = arrangement.add_subparsers(dest="arrangement_command", required=True)
    for name in ("list", "compare", "analyze", "history"):
        arr_sub.add_parser(name, help=f"Arrangement {name}")
    arr_exp = arr_sub.add_parser("experiment", help="Run immutable arrangement experiments")
    arr_exp_sub = arr_exp.add_subparsers(dest="arrangement_experiment_command", required=True)
    tr = arr_exp_sub.add_parser("transpose", help="Transpose an arrangement")
    tr.add_argument("arrangement_id")
    tr.add_argument("destination_key")
    tr.add_argument("semitones", type=int)
    simp = arr_exp_sub.add_parser("simplify", help="Simplify accompaniment")
    simp.add_argument("arrangement_id")
    tempo = arr_exp_sub.add_parser("tempo", help="Alter tempo")
    tempo.add_argument("arrangement_id")
    tempo.add_argument("bpm", type=int)
    groove = arr_exp_sub.add_parser("groove", help="Change groove")
    groove.add_argument("arrangement_id")
    groove.add_argument("groove_style")
    sub.add_parser("chapter-three-demo", help="Run the Chapter 3 set-building demo")
    coord = sub.add_parser("coordination", help="Run Chapter 5 coordination labs")
    coord_sub = coord.add_subparsers(dest="coordination_command", required=True)
    for name in ("analyze", "bottlenecks", "ladder"):
        coord_sub.add_parser(name, help=f"Coordination {name}")
    coord_exp = coord_sub.add_parser("experiment", help="Run immutable coordination experiments")
    coord_exp_sub = coord_exp.add_subparsers(dest="coordination_experiment_command", required=True)
    coord_exp_sub.add_parser("simplify", help="Simplify accompaniment")
    coord_tempo = coord_exp_sub.add_parser("tempo", help="Reduce to a practice tempo")
    coord_tempo.add_argument("bpm", type=int)
    sub.add_parser("chapter-four-demo", help="Run the Chapter 4 arrangement demo")
    sub.add_parser("chapter-five-demo", help="Run the Chapter 5 singing while playing demo")
    practice = sub.add_parser("practice", help="Run Chapter 6 deliberate practice labs")
    practice_sub = practice.add_subparsers(dest="practice_command", required=True)
    for name in ("plan", "analyze", "priorities", "blocks"):
        practice_sub.add_parser(name, help=f"Practice {name}")
    practice_exp = practice_sub.add_parser("experiment", help="Run immutable practice experiments")
    practice_exp_sub = practice_exp.add_subparsers(
        dest="practice_experiment_command", required=True
    )
    for name in (
        "maintenance",
        "performance",
        "shorten",
        "extend",
        "coordination",
        "memorization",
        "exploration",
    ):
        practice_exp_sub.add_parser(name, help=f"Practice experiment {name}")
    sub.add_parser("chapter-six-demo", help="Run the Chapter 6 deliberate practice demo")
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
    elif args.command == "chapter-three-demo":
        _run_chapter_three_demo(rep)
    elif args.command == "chapter-four-demo":
        _run_chapter_four_demo(rep)
    elif args.command == "chapter-five-demo":
        _run_chapter_five_demo(rep)
    elif args.command == "coordination":
        _run_coordination(args)
    elif args.command == "practice":
        _run_practice(args, rep)
    elif args.command == "arrangement":
        _run_arrangement(args, rep)
    elif args.command == "set":
        _run_set_builder(args, rep)
    elif args.command == "setlist":
        set_list = sample_setlist()
        if args.setlist_command == "sample":
            print(f"{set_list.name} ({set_list.target_duration_minutes} minutes)")
            for index, version_id in enumerate(set_list.ordered_version_identifiers, start=1):
                song = rep.get_song(rep.get_version(version_id).song_identifier)
                print(f"{index}. {version_id}: {song.title}")
        elif args.setlist_command == "analyze":
            _print_analysis(set_list, rep)
    elif args.command == "chapter-six-demo":
        _run_chapter_six_demo(rep)
    elif args.command == "demo":
        _run_demo(rep)
    return 0


def _run_set_builder(args, rep: Repertoire) -> None:  # type: ignore[no-untyped-def]
    service = SetBuilderService()
    set_list = sample_setlist()
    venue = sample_venue()
    if args.set_command == "summary":
        print(f"{set_list.name} ({set_list.target_duration_minutes} minutes)")
        for index, version_id in enumerate(set_list.ordered_version_identifiers, start=1):
            song = rep.get_song(rep.get_version(version_id).song_identifier)
            print(f"{index}. {song.title} — {version_id}")
    elif args.set_command == "timeline":
        for entry in service.timeline(set_list, rep):
            print(f"{entry.start_time}  {entry.label}")
    elif args.set_command == "analyze":
        analysis = service.analyze(set_list, rep, venue)
        print(analysis.overall_assessment)
        print(f"Total duration: {service.format_seconds(analysis.total_duration_seconds)}")
        for strength in analysis.strengths:
            print(f"Strength: {strength}")
        for warning in analysis.warnings:
            print(f"Warning: {warning}")
        for experiment in analysis.suggested_experiments:
            print(f"Suggested experiment: {experiment}")
    elif args.set_command == "compare":
        scenarios = sample_set_scenarios()
        comparison = service.compare(
            scenarios["coffeehouse-15"], scenarios["listening-room"], rep, venue
        )
        _print_set_comparison(comparison)
    elif args.set_command == "experiment":
        if args.experiment_command == "swap":
            changed = service.swap_songs(set_list, args.first, args.second)
        elif args.experiment_command == "opener":
            changed = service.change_opener(set_list, args.version_id)
        elif args.experiment_command == "closer":
            changed = service.change_closer(set_list, args.version_id)
        else:
            from open_mic_lab.domain import SetTransition, TransitionEnergyEffect, TransitionKind

            changed = service.insert_transition(
                set_list,
                SetTransition(
                    "learner-transition",
                    TransitionKind.QUICK_SEGUE,
                    15,
                    TransitionEnergyEffect.LIFT,
                    "Learner-added quick segue",
                    args.after_version_id,
                ),
            )
        print("Original order:", ", ".join(set_list.ordered_version_identifiers))
        print("Experiment order:", ", ".join(changed.ordered_version_identifiers))
        unchanged = (
            set_list.ordered_version_identifiers != changed.ordered_version_identifiers
            or set_list.transitions != changed.transitions
        )
        print(f"Original object unchanged: {unchanged}")


def _print_set_comparison(comparison) -> None:  # type: ignore[no-untyped-def]
    print(f"Comparing {comparison.left_name} vs {comparison.right_name}")
    for difference in comparison.differences:
        print(f"Difference: {difference}")
    for strength in comparison.left_strengths:
        print(f"Left strength: {strength}")
    for strength in comparison.right_strengths:
        print(f"Right strength: {strength}")
    for weakness in comparison.left_weaknesses:
        print(f"Left tradeoff: {weakness}")
    for weakness in comparison.right_weaknesses:
        print(f"Right tradeoff: {weakness}")
    for tradeoff in comparison.audience_tradeoffs:
        print(f"Audience tradeoff: {tradeoff}")


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


def _run_chapter_three_demo(rep: Repertoire) -> None:
    print("Chapter 3 — Building a Set")
    service = SetBuilderService()
    original = sample_setlist()
    print("\nTimeline")
    for entry in service.timeline(original, rep):
        print(f"{entry.start_time}  {entry.label}")
    print("\nAnalysis")
    analysis = service.analyze(original, rep, sample_venue())
    print(analysis.overall_assessment)
    for strength in analysis.strengths:
        print(f"Strength: {strength}")
    for warning in analysis.warnings:
        print(f"Weakness: {warning}")
    changed = service.swap_songs(original, "harbor-guitar", "window-piano")
    print("\nImmutable experiment: swap two songs")
    print(f"Before: {original.ordered_version_identifiers}")
    print(f"After:  {changed.ordered_version_identifiers}")
    print("\nComparison")
    _print_set_comparison(service.compare(original, changed, rep, sample_venue()))
    print("\nReflection: What happens if I change the order?")
    print("Reflection: Which transition protects momentum, and which one costs time?")


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


def _run_arrangement(args, rep: Repertoire) -> None:  # type: ignore[no-untyped-def]
    experiment_service = ArrangementExperimentService()
    analysis_service = ArrangementAnalysisService()
    timeline_service = ArrangementTimelineService()
    original = rep.get_arrangement("window-piano-arrangement")
    alternate = rep.get_arrangement("window-guitar-original-feature-arrangement")
    if args.arrangement_command == "list":
        for arrangement in rep.arrangements.values():
            print(
                f"{arrangement.identifier}: {arrangement.name} | "
                f"{arrangement.primary_instrument.value} | "
                f"key {arrangement.performance_key} | {arrangement.target_tempo_bpm} bpm"
            )
    elif args.arrangement_command == "compare":
        _print_arrangement_comparison(analysis_service.compare(original, alternate))
    elif args.arrangement_command == "analyze":
        for entry in timeline_service.timeline(original):
            print(
                f"{entry.start_time}  {entry.section} ({entry.duration_seconds}s) — {entry.notes}"
            )
    elif args.arrangement_command == "history":
        changed = _chapter_four_chain(original)
        for record in changed.history:
            print(
                f"{record.experiment_name}: {record.summary} "
                f"from {record.source_arrangement_identifier}"
            )
    elif args.arrangement_command == "experiment":
        arrangement = rep.get_arrangement(args.arrangement_id)
        cmd = args.arrangement_experiment_command
        if cmd == "transpose":
            changed = experiment_service.transpose(
                arrangement, args.destination_key, args.semitones
            )
        elif cmd == "simplify":
            changed = experiment_service.simplify_accompaniment(arrangement)
        elif cmd == "tempo":
            changed = experiment_service.alter_tempo(arrangement, args.bpm)
        else:
            changed = experiment_service.change_groove(arrangement, args.groove_style)
        print(
            f"Original: {arrangement.identifier} | key {arrangement.performance_key} | "
            f"{arrangement.target_tempo_bpm} bpm | {arrangement.groove_style}"
        )
        print(
            f"Experiment: {changed.identifier} | key {changed.performance_key} | "
            f"{changed.target_tempo_bpm} bpm | {changed.groove_style}"
        )
        unchanged = arrangement != changed and arrangement.identifier in rep.arrangements
        print(f"Original object unchanged: {unchanged}")


def _chapter_four_chain(original: Arrangement) -> Arrangement:
    service = ArrangementExperimentService()
    transposed = service.transpose(original, "G", -2)
    simplified = service.simplify_accompaniment(transposed)
    short_intro = service.shorten_introduction(simplified)
    return service.alter_tempo(short_intro, 64)


def _print_arrangement_comparison(comparison) -> None:  # type: ignore[no-untyped-def]
    print(f"Comparing {comparison.left_identifier} vs {comparison.right_identifier}")
    for difference in comparison.differences:
        print(f"Difference: {difference}")
    for tradeoff in comparison.left_tradeoffs:
        print(f"Left tradeoff: {tradeoff}")
    for tradeoff in comparison.right_tradeoffs:
        print(f"Right tradeoff: {tradeoff}")
    print(f"Reflection: {comparison.reflection}")


def _run_chapter_four_demo(rep: Repertoire) -> None:
    print("Chapter 4 — Making Songs Your Own")
    original = rep.get_arrangement("window-piano-arrangement")
    service = ArrangementExperimentService()
    analysis = ArrangementAnalysisService()
    timeline = ArrangementTimelineService()
    stages = [original]
    stages.append(service.transpose(stages[-1], "G", -2))
    stages.append(service.simplify_accompaniment(stages[-1]))
    stages.append(service.alter_tempo(stages[-1], 64))
    for before, after in zip(stages, stages[1:], strict=False):
        _print_arrangement_comparison(analysis.compare(before, after))
    print("\nExperiment history")
    for record in stages[-1].history:
        print(f"- {record.experiment_name}: {record.summary}")
    print("\nStructural timeline")
    for entry in timeline.timeline(stages[-1]):
        print(f"{entry.start_time}  {entry.section} ({entry.duration_seconds}s)")
    print("\nReflection: What did this arrangement make easier, and what did it cost?")
    print("Reflection: Does this version serve tonight's room better than the baseline?")


def _run_coordination(args) -> None:  # type: ignore[no-untyped-def]
    profile = sample_coordination_profile()
    service = CoordinationAnalysisService()
    experiment = CoordinationExperimentService()
    if args.coordination_command == "analyze":
        _print_coordination_analysis(service.analyze(profile))
    elif args.coordination_command == "bottlenecks":
        for item in service.bottlenecks(profile):
            print(f"Bottleneck: {item}")
            print(f"Suggested experiment: {service._focus_for(item)}")
    elif args.coordination_command == "ladder":
        ladder = TempoLadderService().generate(60, profile.target_tempo_bpm, 6)
        print("Tempo ladder:", ", ".join(f"{bpm} BPM" for bpm in ladder.tempos))
        print(ladder.explanation)
    elif args.coordination_command == "experiment":
        original = CoordinationExperiment(profile)
        if args.coordination_experiment_command == "simplify":
            changed = experiment.simplify_accompaniment(original)
        else:
            changed = experiment.reduce_tempo(original, args.bpm)
        before = service.analyze(original.profile)
        after = service.analyze(changed.profile)
        print(f"Before: {before.coordination_score}/100 load {before.cognitive_load.score}")
        print(f"After: {after.coordination_score}/100 load {after.cognitive_load.score}")
        print(f"Original object unchanged: {original.profile.identifier == profile.identifier}")


def _print_coordination_analysis(result) -> None:  # type: ignore[no-untyped-def]
    print(f"Coordination score: {result.coordination_score}/100")
    print(f"Cognitive load: {result.cognitive_load.score}/100 ({result.cognitive_load.category})")
    for bottleneck in result.primary_bottlenecks:
        print(f"Bottleneck: {bottleneck}")
    for focus in result.suggested_practice_focus:
        print(f"Practice focus: {focus}")
    for factor in result.contributing_factors:
        print(f"Factor: {factor}")
    print(result.model_note)


def _run_chapter_five_demo(rep: Repertoire) -> None:
    print("Chapter 5 — Singing While Playing")
    arrangement = rep.get_arrangement("window-piano-arrangement")
    print(f"Performance version: {arrangement.source_performance_version_identifier}")
    profile = sample_coordination_profile()
    analysis = CoordinationAnalysisService()
    experiments = CoordinationExperimentService()
    baseline = CoordinationExperiment(profile)
    print("\nBaseline analysis")
    _print_coordination_analysis(analysis.analyze(baseline.profile))
    print("\nBottlenecks")
    for item in analysis.bottlenecks(baseline.profile):
        print(f"- {item}")
    simplified = experiments.simplify_accompaniment(baseline)
    print("\nSimplify accompaniment experiment")
    print(f"Before load: {analysis.analyze(baseline.profile).cognitive_load.score}")
    print(f"After load: {analysis.analyze(simplified.profile).cognitive_load.score}")
    ladder = TempoLadderService().generate(60, profile.target_tempo_bpm, 6)
    print("\nTempo ladder")
    for bpm in ladder.tempos:
        print(f"- {bpm} BPM")
    print(ladder.explanation)
    print(
        "Automaticity reduces cognitive load because a stable accompaniment "
        "consumes less attention."
    )
    print("Reflection: Which task fails first when attention is crowded?")
    print("Reflection: What could become automatic before the next full-speed run?")


def _sample_practice_plan(
    minutes: int = 30, goal: PracticeGoal = PracticeGoal.BALANCED_IMPROVEMENT
) -> object:
    service = PracticePlanningService()
    return service.generate_plan(
        build_sample_repertoire(),
        sample_practice_sessions(),
        sample_coordination_profile(),
        PracticePlanningInput(minutes, __import__("datetime").date(2026, 8, 5), goal),
    )


def _print_practice_plan(plan) -> None:  # type: ignore[no-untyped-def]
    print(
        f"Practice plan: {plan.identifier} "
        f"({plan.estimated_duration_minutes}/{plan.available_minutes} minutes)"
    )
    print(f"Goal: {plan.goal.value}")
    for index, block in enumerate(plan.blocks, start=1):
        version = f" [{block.version_identifier}]" if block.version_identifier else ""
        print(
            f"{index}. {block.task.value} — {block.duration_minutes} min — "
            f"{block.focus_area.value}{version}"
        )
        print(f"   Objective: {block.objective}")
        print(f"   Success: {block.success_criteria}")
        print(f"   Why: {block.notes}")
    for reason in plan.rationale:
        print(f"Sequencing: {reason}")


def _run_practice(args, rep: Repertoire) -> None:  # type: ignore[no-untyped-def]
    service = PracticePlanningService()
    planning_input = PracticePlanningInput(30, __import__("datetime").date(2026, 8, 5))
    plan = service.generate_plan(
        rep, sample_practice_sessions(), sample_coordination_profile(), planning_input
    )
    if args.practice_command == "plan":
        _print_practice_plan(plan)
    elif args.practice_command == "priorities":
        for item in service.priorities(
            rep, sample_practice_sessions(), sample_coordination_profile(), planning_input
        ):
            print(
                f"{item.version_identifier}: {item.skill_area.value} "
                f"{item.score} ({item.priority.value})"
            )
            for reason in item.reasons:
                print(f"- {reason}")
    elif args.practice_command == "blocks":
        for block in plan.blocks:
            print(
                f"{block.task.value}: {block.duration_minutes} minutes — {block.success_criteria}"
            )
    elif args.practice_command == "analyze":
        analytics = PracticeAnalyticsService().analyze(plan, sample_practice_sessions())
        for area, minutes in analytics.distribution:
            print(f"{area.value}: {minutes} minutes")
        for observation in analytics.observations:
            print(f"Observation: {observation}")
    elif args.practice_command == "experiment":
        changed = service.experiment(plan, args.practice_experiment_command)
        print(
            f"Original: {plan.identifier} {plan.estimated_duration_minutes} minutes "
            f"{plan.goal.value}"
        )
        print(
            f"Experiment: {changed.identifier} {changed.estimated_duration_minutes} minutes "
            f"{changed.goal.value}"
        )
        print(f"Original object unchanged: {plan.identifier != changed.identifier}")


def _run_chapter_six_demo(rep: Repertoire) -> None:
    print("Chapter 6 — Deliberate Practice Engineering")
    service = PracticePlanningService()
    sessions = sample_practice_sessions()
    profile = sample_coordination_profile()
    print("\nCurrent repertoire priorities")
    base_input = PracticePlanningInput(30, __import__("datetime").date(2026, 8, 5))
    for item in service.priorities(rep, sessions, profile, base_input)[:5]:
        print(
            f"- {item.version_identifier}: {item.skill_area.value} "
            f"({item.priority.value}) because {item.reasons[0]}"
        )
    print("\n30-minute plan")
    plan = service.generate_plan(rep, sessions, profile, base_input)
    _print_practice_plan(plan)
    print("\nRevised 45-minute plan")
    revised = service.generate_plan(
        rep,
        sessions,
        profile,
        PracticePlanningInput(
            45, __import__("datetime").date(2026, 8, 5), PracticeGoal.PERFORMANCE_PREPARATION
        ),
    )
    _print_practice_plan(revised)
    print("\nPractice analytics")
    analytics = PracticeAnalyticsService().analyze(revised, sessions)
    for observation in analytics.observations:
        print(f"Observation: {observation}")
    print("Reflection: Which block produces the greatest improvement per minute?")
    print("Reflection: What should be maintained, and what deserves focused change?")


if __name__ == "__main__":
    raise SystemExit(main())
