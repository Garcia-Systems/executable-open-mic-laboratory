"""Chapter 14 deterministic open mic event orchestration."""

from dataclasses import replace

from open_mic_lab.domain import (
    EventReport,
    EventScenario,
    EventTimeline,
    EventTimelineEntry,
    NetworkingOpportunity,
    OpenMicEvent,
    PerformanceExecution,
    PerformanceSlot,
    PerformerArrival,
    PostPerformanceReflection,
    Repertoire,
    SignUpOrder,
    WaitingPeriod,
)
from open_mic_lab.domain.equipment import SignalPath
from open_mic_lab.equipment_templates import equipment_templates
from open_mic_lab.sample_data import (
    sample_audience_performance,
    sample_audience_profiles,
    sample_communication_plan,
    sample_coordination_profile,
    sample_improvisation_context,
    sample_original_presentation_plan,
    sample_practice_sessions,
    sample_recovery_scenario,
    sample_setlist,
    sample_venue,
)
from open_mic_lab.services.audience_service import AudienceResponseService
from open_mic_lab.services.coordination_service import CoordinationAnalysisService
from open_mic_lab.services.equipment_service import SignalFlowService
from open_mic_lab.services.improvisation_service import ImprovisationAnalysisService
from open_mic_lab.services.originals_service import OriginalMusicAnalysisService
from open_mic_lab.services.readiness_service import calculate_readiness
from open_mic_lab.services.recovery_service import RecoveryAnalysisService
from open_mic_lab.services.set_builder_service import SetBuilderService
from open_mic_lab.services.soundcheck_service import SoundCheckService
from open_mic_lab.services.stage_service import CommunicationAnalysisService
from open_mic_lab.soundcheck_templates import sample_soundcheck


def event_scenarios() -> tuple[EventScenario, ...]:
    """Return stable scenario order for educational examples."""
    return tuple(EventScenario)


class OpenMicEventService:
    """Coordinate existing subsystem engines into one open mic evening."""

    def simulate(
        self,
        repertoire: Repertoire,
        scenario: EventScenario = EventScenario.FIRST_OPEN_MIC,
        venue_template: str = "coffeehouse",
    ) -> OpenMicEvent:
        """Create a deterministic event without replacing subsystem analysis."""
        set_list = sample_setlist()
        templates = self._templates(venue_template)
        entries = tuple(
            EventTimelineEntry(time, label, note) for time, label, note in templates[scenario]
        )
        return OpenMicEvent(
            f"{scenario.name.lower()}-{venue_template}",
            scenario,
            venue_template,
            PerformerArrival(
                entries[0].time, "Check in with host.", "Notice PA, stage size, and signup flow."
            ),
            SignUpOrder(
                4 if scenario is EventScenario.FIRST_OPEN_MIC else 2,
                entries[4].time,
                "Slot leaves time to observe the room before playing.",
            ),
            WaitingPeriod(
                35, ("Listen for room volume.", "Notice audience attention and host pacing.")
            ),
            PerformanceSlot(
                entries[4].time,
                set_list.target_duration_minutes,
                set_list.ordered_version_identifiers,
            ),
            PerformanceExecution(
                entries[6].time,
                entries[7].time,
                "forgotten-lyrics handled with continue immediately",
                "extend final chorus if audience is engaged",
            ),
            NetworkingOpportunity(
                entries[8].time,
                "Thank one listener or host for a specific observation.",
                "Record one concrete follow-up action.",
            ),
            PostPerformanceReflection(
                entries[9].time,
                (
                    "What preparation changed the evening?",
                    "What should be practiced before the next signup?",
                ),
            ),
            EventTimeline(entries),
        )

    def report(self, repertoire: Repertoire, event: OpenMicEvent) -> EventReport:
        """Generate a report by calling prior chapter services and summarizing their outputs."""
        set_list = sample_setlist()
        venue = sample_venue()
        set_analysis = SetBuilderService().analyze(set_list, repertoire, venue)
        readiness = tuple(
            self._readiness_summary(repertoire, version_id)
            for version_id in event.slot.version_identifiers
        )
        arrangements = tuple(
            self._arrangement_summary(repertoire, version_id)
            for version_id in event.slot.version_identifiers
        )
        coordination = CoordinationAnalysisService().analyze(sample_coordination_profile())
        communication = CommunicationAnalysisService().analyze(sample_communication_plan())
        signal_path = self._signal_path(event.venue_template)
        equipment = SignalFlowService().analyze(signal_path)
        sound = SoundCheckService().analyze(sample_soundcheck(), signal_path)
        audience = AudienceResponseService().analyze(
            sample_audience_performance(), sample_audience_profiles()["supportive-coffeehouse"]
        )
        recovery = RecoveryAnalysisService().analyze(sample_recovery_scenario())
        first_arrangement = repertoire.get_arrangement(
            repertoire.get_version(event.slot.version_identifiers[0]).arrangement_identifier or ""
        )
        audience_profile = sample_audience_profiles()["supportive-coffeehouse"]
        improv = ImprovisationAnalysisService().analyze(
            sample_improvisation_context(), first_arrangement, audience_profile
        )
        originals = OriginalMusicAnalysisService().analyze(
            sample_original_presentation_plan(), set_list, repertoire
        )
        return EventReport(
            event,
            (
                set_analysis.overall_assessment,
                *readiness,
                f"Coordination score: {coordination.coordination_score}",
            ),
            tuple(event.slot.version_identifiers),
            arrangements,
            (communication.summary, *communication.strengths[:2]),
            (
                f"{len(equipment.end_to_end_paths)} end-to-end signal path(s)",
                *[o.message for o in equipment.observations[:2]],
            ),
            tuple(sound.observations[:4]),
            (
                f"Audience profile: {audience.profile_identifier}",
                *audience.strengths[:3],
                *audience.friction_points[:1],
            ),
            tuple(recovery.observations),
            tuple(option.suggestion for option in improv.options[:4]),
            (originals.summary, *originals.observations[:3]),
            event.reflection.prompts + recovery.reflection_prompts,
        )

    def timeline_text(self, event: OpenMicEvent) -> str:
        """Format the event timeline."""
        return "\n".join(
            f"{entry.time} {entry.label} — {entry.educational_note}"
            for entry in event.timeline.entries
        )

    def mermaid(self, event: OpenMicEvent) -> str:
        """Render a deterministic Mermaid flowchart."""
        labels = (
            "Preparation",
            "Arrival",
            "Sound Check",
            "Performance",
            "Networking",
            "Reflection",
        )
        body = "\n".join(
            f"    n{i}[{label}] --> n{i + 1}[{labels[i + 1]}]"
            for i, label in enumerate(labels[:-1])
        )
        return f"flowchart TD\n{body}"

    def compare(self, left: OpenMicEvent, right: OpenMicEvent) -> tuple[str, ...]:
        """Compare two simulated events at the orchestration level."""
        return (
            f"scenario: {left.scenario.value} -> {right.scenario.value}",
            f"venue: {left.venue_template} -> {right.venue_template}",
            f"call time: {left.slot.call_time} -> {right.slot.call_time}",
            f"history: {', '.join(right.experiment_history) or 'none'}",
        )

    def experiment(self, event: OpenMicEvent, name: str) -> OpenMicEvent:
        """Create immutable event variants for Chapter 14 experiments."""
        history = event.experiment_history + (name,)
        if name == "delayed-performance-slot":
            return replace(
                event, slot=replace(event.slot, call_time="19:45"), experiment_history=history
            )
        if name == "different-audience":
            return replace(
                event, scenario=EventScenario.SONGWRITER_SHOWCASE, experiment_history=history
            )
        if name == "equipment-change":
            return replace(event, venue_template="church", experiment_history=history)
        if name == "alternate-arrangement":
            return replace(
                event,
                execution=replace(
                    event.execution, improvisation_choice="shorten intro and simplify ending"
                ),
                experiment_history=history,
            )
        if name == "unexpected-recovery-event":
            return replace(
                event,
                execution=replace(
                    event.execution, recovery_event="cable-disconnected handled by stop and explain"
                ),
                experiment_history=history,
            )
        if name == "original-song-placement":
            versions = tuple(reversed(event.slot.version_identifiers))
            return replace(
                event,
                slot=replace(event.slot, version_identifiers=versions),
                experiment_history=history,
            )
        return replace(event, experiment_history=history)

    def _readiness_summary(self, repertoire: Repertoire, version_id: str) -> str:
        result = calculate_readiness(repertoire.get_version(version_id), sample_practice_sessions())
        return f"{version_id}: {result.category}"

    def _arrangement_summary(self, repertoire: Repertoire, version_id: str) -> str:
        arrangement_id = repertoire.get_version(version_id).arrangement_identifier or ""
        arrangement = repertoire.get_arrangement(arrangement_id)
        return f"{arrangement.name}: {arrangement.groove_style}"

    def _signal_path(self, venue_template: str) -> SignalPath:
        return equipment_templates()["church-service" if venue_template == "church" else "open-mic"]

    def _templates(
        self, venue_template: str
    ) -> dict[EventScenario, tuple[tuple[str, str, str], ...]]:
        base: tuple[tuple[str, str, str], ...] = (
            ("18:30", "Arrive", "Enter early enough to make calm decisions."),
            ("18:35", "Sign Up", "Choose a slot with time to observe."),
            ("18:45", "Observe Other Performers", "Learn the room before performing."),
            ("19:05", "Sound Check", "Confirm signal flow and monitoring."),
            ("19:20", "Called to Stage", "Transition from waiting to execution."),
            ("19:21", "Introduction", "Use the communication plan."),
            ("19:22", "Performance Begins", "Execute the prepared set."),
            ("19:36", "Performance Ends", "Notice recovery and improvisation choices."),
            ("19:38", "Networking", "Convert the event into community learning."),
            ("19:45", "Reflection", "Record preparation data."),
        )
        if venue_template == "church":
            base = tuple(
                (time, label, note.replace("room", "listening space")) for time, label, note in base
            )
        return {scenario: base for scenario in EventScenario}
