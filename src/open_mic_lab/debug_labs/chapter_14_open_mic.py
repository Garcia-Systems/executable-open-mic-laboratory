"""Debug laboratory for Chapter 14: Open Mic Simulator.

Breakpoint markers:
- BREAKPOINT 1: inspect event creation inputs.
- BREAKPOINT 2: step into orchestration and timeline generation.
- BREAKPOINT 3: inspect subsystem-derived report sections.
- BREAKPOINT 4: verify immutable event experiments.
"""

from typing import cast

from open_mic_lab.domain import EventReport, OpenMicEvent
from open_mic_lab.sample_data import build_sample_repertoire
from open_mic_lab.services.event_service import OpenMicEventService


def run_debug_lab() -> dict[str, object]:
    """Run the Chapter 14 debug lab and return inspectable variables."""
    repertoire = build_sample_repertoire()  # BREAKPOINT 1
    service = OpenMicEventService()
    event = service.simulate(repertoire)  # BREAKPOINT 2
    report = service.report(repertoire, event)  # BREAKPOINT 3
    delayed_event = service.experiment(event, "delayed-performance-slot")  # BREAKPOINT 4
    recovery_event = service.experiment(event, "unexpected-recovery-event")
    return {
        "event": event,
        "timeline": service.timeline_text(event),
        "report": report,
        "delayed_event": delayed_event,
        "recovery_event": recovery_event,
        "original_unchanged": event.experiment_history == (),
    }


def main() -> int:
    """Print a concise debug-lab walkthrough."""
    result = run_debug_lab()
    event = cast(OpenMicEvent, result["event"])
    report = cast(EventReport, result["report"])
    print("Chapter 14 debug lab: Open Mic Simulator")
    print(f"Event: {event.identifier}")
    print(result["timeline"])
    print(
        "Report sections: "
        f"preparation={len(report.preparation)}, recovery={len(report.recovery_events)}"
    )
    print(f"Immutable original unchanged: {result['original_unchanged']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
