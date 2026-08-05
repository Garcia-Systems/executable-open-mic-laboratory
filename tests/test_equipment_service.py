"""Tests for Chapter 8 equipment laboratory."""

from open_mic_lab.domain.equipment import Cable, Connection, SignalPath, SignalType
from open_mic_lab.equipment_templates import equipment_templates, piano_and_vocal_setup
from open_mic_lab.services.equipment_service import EquipmentExperimentService, SignalFlowService


def test_piano_and_vocal_routes_to_audience_and_performer() -> None:
    analysis = SignalFlowService().analyze(piano_and_vocal_setup())

    assert analysis.audience_outputs == ("Main Speakers",)
    assert analysis.performer_outputs == ("Performer Monitor",)
    assert analysis.incompatible_connections == ()


def test_visualization_is_deterministic_and_branching() -> None:
    diagram = SignalFlowService().visualize(piano_and_vocal_setup())

    assert diagram == SignalFlowService().visualize(piano_and_vocal_setup())
    assert "Small Mixer" in diagram
    assert "├──►" in diagram
    assert "Main Speakers" in diagram


def test_disconnect_cable_is_immutable_and_reports_no_audience_output() -> None:
    original = piano_and_vocal_setup()
    changed = EquipmentExperimentService().disconnect_cable(original, "mixer-to-mains")
    analysis = SignalFlowService().analyze(changed)

    assert original is not changed
    assert len(original.connections) == 4
    assert len(changed.connections) == 3
    assert any(observation.code == "no-audience-output" for observation in analysis.observations)


def test_incompatible_signal_types_are_reported() -> None:
    setup = piano_and_vocal_setup()
    bad = Connection(
        "bad",
        "vocal-mic",
        "out-1",
        "mixer",
        "in-2",
        Cable("bad-cable", "Wrong cable", SignalType.MIC_LEVEL),
    )
    changed = SignalPath("bad-path", "Bad Path", setup.nodes, (bad,))

    analysis = SignalFlowService().analyze(changed)

    assert analysis.incompatible_connections == ("bad",)
    assert any(observation.code == "incompatible-signal" for observation in analysis.observations)


def test_templates_include_required_educational_scenarios() -> None:
    templates = equipment_templates()

    assert set(templates) >= {
        "solo-acoustic-guitar",
        "solo-digital-piano",
        "piano-and-vocal",
        "guitar-and-vocal",
        "small-duo",
        "church-service",
        "coffeehouse",
        "open-mic",
        "simple-band",
    }
