from decimal import Decimal
from importlib import import_module

from open_mic_lab.debug_labs.chapter_00_readiness import build_debug_scenario as build_chapter_00
from open_mic_lab.debug_labs.chapter_01_song_suitability import (
    build_debug_scenario as build_chapter_01,
)
from open_mic_lab.domain import PerformanceVersion
from open_mic_lab.services.readiness_service import ReadinessResult
from open_mic_lab.services.suitability_service import CandidateComparison, SuitabilityResult


def test_debug_modules_import_successfully() -> None:
    assert import_module("open_mic_lab.debug_labs.chapter_00_readiness")
    assert import_module("open_mic_lab.debug_labs.chapter_01_song_suitability")


def test_chapter_00_debug_scenario_is_structured_and_deterministic() -> None:
    first = build_chapter_00()
    second = build_chapter_00()
    assert first == second
    assert first.song.identifier == "river-road"
    assert first.original_version.identifier != first.adapted_version.identifier
    assert first.original_version.performance_key != first.adapted_version.performance_key
    assert first.practice_sessions
    assert isinstance(first.original_result, ReadinessResult)
    assert isinstance(first.adapted_result, ReadinessResult)
    assert Decimal("0") <= first.original_result.score <= Decimal("100")
    assert Decimal("0") <= first.adapted_result.score <= Decimal("100")
    assert first.score_difference == first.adapted_result.score - first.original_result.score
    assert first.adapted_result.breakdown


def test_chapter_01_debug_scenario_is_structured_and_deterministic() -> None:
    first = build_chapter_01()
    second = build_chapter_01()
    assert [r.version_id for r in first.comparison.results] == [
        r.version_id for r in second.comparison.results
    ]
    assert first.candidate_a.identifier != first.candidate_b.identifier
    assert isinstance(first.candidate_a, PerformanceVersion)
    assert isinstance(first.candidate_b, PerformanceVersion)
    assert isinstance(first.candidate_a_result, SuitabilityResult)
    assert isinstance(first.candidate_b_result, SuitabilityResult)
    assert isinstance(first.comparison, CandidateComparison)
    assert len(first.comparison.results) >= 2
    assert first.adapted_candidate_b is not first.candidate_b
    assert first.adapted_candidate_b.identifier != first.candidate_b.identifier
    assert first.candidate_b.performance_key == first.candidate_b_original_key
    assert not first.source_candidate_was_mutated
    assert first.adapted_candidate_b.performance_key == "F"
    assert first.adapted_candidate_b_result.version_id == first.adapted_candidate_b.identifier
    assert first.score_change == (
        first.adapted_candidate_b_result.score - first.candidate_b_result.score
    )
    assert [r.version_id for r in first.adapted_comparison.results] == [
        r.version_id for r in second.adapted_comparison.results
    ]


def test_vscode_debug_configurations_reference_valid_modules() -> None:
    import json
    from pathlib import Path

    data = json.loads(Path(".vscode/launch.json").read_text())
    modules = {config["name"]: config["module"] for config in data["configurations"]}
    assert modules == {
        "Debug Chapter 0 Readiness Lab": "open_mic_lab.debug_labs.chapter_00_readiness",
        "Debug Chapter 1 Song Suitability Lab": (
            "open_mic_lab.debug_labs.chapter_01_song_suitability"
        ),
        "Debug Chapter 2 Repertoire Engineering Lab": (
            "open_mic_lab.debug_labs.chapter_02_repertoire_engineering"
        ),
        "Debug Chapter 3 Building a Set Lab": ("open_mic_lab.debug_labs.chapter_03_building_a_set"),
        "Debug Chapter 4 Arrangements Lab": ("open_mic_lab.debug_labs.chapter_04_arrangements"),
        "Debug Chapter 5 Coordination Lab": "open_mic_lab.debug_labs.chapter_05_coordination",
        "Debug Chapter 6 Practice Engineering Lab": (
            "open_mic_lab.debug_labs.chapter_06_practice_engineering"
        ),
        "Debug Chapter 7 Stage Presence Lab": ("open_mic_lab.debug_labs.chapter_07_stage_presence"),
        "Debug Chapter 8 Signal Flow Lab": "open_mic_lab.debug_labs.chapter_08_signal_flow",
        "Debug Chapter 9 Sound Check Lab": "open_mic_lab.debug_labs.chapter_09_sound_check",
        "Debug Chapter 10 Audience Experience Lab": (
            "open_mic_lab.debug_labs.chapter_10_audience_experience"
        ),
        "Debug Chapter 11 Recovery Lab": "open_mic_lab.debug_labs.chapter_11_recovery",
        "Debug Chapter 12 Improvisation Lab": ("open_mic_lab.debug_labs.chapter_12_improvisation"),
        "Debug Chapter 13 Original Music Lab": (
            "open_mic_lab.debug_labs.chapter_13_original_music"
        ),
        "Debug Chapter 14 Open Mic Simulator Lab": ("open_mic_lab.debug_labs.chapter_14_open_mic"),
    }
    for module in modules.values():
        assert import_module(module)
