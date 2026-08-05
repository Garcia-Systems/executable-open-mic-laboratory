"""Debug laboratory for Chapter 8 signal flow."""

from open_mic_lab.equipment_templates import piano_and_vocal_setup
from open_mic_lab.services.equipment_service import EquipmentExperimentService, SignalFlowService


def run_debug_lab() -> None:
    """Run the Chapter 8 debug scenario with breakpoint-friendly variables."""
    # BREAKPOINT 1: equipment-template creation.
    setup = piano_and_vocal_setup()
    flow = SignalFlowService()
    experiments = EquipmentExperimentService()

    # BREAKPOINT 2: graph construction and baseline routing.
    baseline_analysis = flow.analyze(setup)
    baseline_diagram = flow.visualize(setup)

    # BREAKPOINT 3: immutable experiment disconnects a cable.
    disconnected = experiments.disconnect_cable(setup, "mixer-to-mains")

    # BREAKPOINT 4: validation after a routing fault.
    disconnected_analysis = flow.analyze(disconnected)
    disconnected_diagram = flow.visualize(disconnected)

    # BREAKPOINT 5: compare restored and changed signal paths.
    comparison = flow.compare(disconnected, setup)

    print("Chapter 8 Signal Flow Debug Lab")
    print(baseline_diagram)
    print(f"Baseline observations: {len(baseline_analysis.observations)}")
    print(disconnected_diagram)
    print(f"Disconnected observations: {len(disconnected_analysis.observations)}")
    for difference in comparison.differences:
        print(f"Difference: {difference}")


if __name__ == "__main__":
    run_debug_lab()
