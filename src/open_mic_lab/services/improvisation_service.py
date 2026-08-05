"""Deterministic improvisation-analysis services for Chapter 12."""

from dataclasses import replace

from open_mic_lab.domain.arrangement import Arrangement
from open_mic_lab.domain.audience import AudienceExpectation, AudienceProfile
from open_mic_lab.domain.improvisation import (
    AdaptivePerformancePlan,
    ImprovisationAnalysis,
    ImprovisationConstraint,
    ImprovisationContext,
    ImprovisationDecision,
    ImprovisationOpportunity,
    ImprovisationOption,
    TimelineComparison,
    TimelineSection,
)


class ImprovisationAnalysisService:
    """Analyze adaptive choices without evaluating artistic originality."""

    def analyze(
        self,
        context: ImprovisationContext,
        arrangement: Arrangement,
        audience: AudienceProfile,
    ) -> ImprovisationAnalysis:
        """Return deterministic opportunities, options, and explanations."""
        options = self.options(context, arrangement, audience)
        observations = [
            "Improvisation is modeled as constrained decision-making, not unrestricted freedom.",
            f"Available time is {context.available_time_seconds} seconds, "
            "so duration choices are visible.",
        ]
        if context.recovery_context.lower() != "stable":
            observations.append(
                "A recovery context can create musical reasons to simplify or finish clearly."
            )
        if audience.participation_comfort >= 6:
            observations.append("This audience profile can support optional participation moments.")
        return ImprovisationAnalysis(
            context,
            tuple(observations),
            options,
            tuple(option.suggestion for option in options),
        )

    def options(
        self,
        context: ImprovisationContext,
        arrangement: Arrangement,
        audience: AudienceProfile,
    ) -> tuple[ImprovisationOption, ...]:
        """List available options in stable educational order."""
        options: list[ImprovisationOption] = []
        if context.available_time_seconds >= 45:
            options.append(
                self._option(
                    ImprovisationOpportunity.REPEAT_CHORUS,
                    ImprovisationDecision.REPEAT_CHORUS,
                    (
                        ImprovisationConstraint.REMAINING_TIME,
                        ImprovisationConstraint.AUDIENCE_PARTICIPATION,
                    ),
                    "Adds familiarity and energy while using more of the slot.",
                    "The remaining time can absorb another chorus without forcing a rushed ending.",
                )
            )
            options.append(
                self._option(
                    ImprovisationOpportunity.EXTEND_ENDING,
                    ImprovisationDecision.EXTEND_ENDING,
                    (
                        ImprovisationConstraint.REMAINING_TIME,
                        ImprovisationConstraint.VENUE_EXPECTATIONS,
                    ),
                    "Creates closure but may reduce time for spoken thanks.",
                    "The slot has room for a deliberate ending variation.",
                )
            )
        if arrangement.solo_sections or context.available_time_seconds >= 30:
            options.append(
                self._option(
                    ImprovisationOpportunity.ADD_INSTRUMENTAL_SPACE,
                    ImprovisationDecision.INSERT_INSTRUMENTAL_BREAK,
                    (
                        ImprovisationConstraint.COORDINATION_DEMANDS,
                        ImprovisationConstraint.PERFORMER_READINESS,
                    ),
                    "Gives the voice space while asking the accompaniment to stay steady.",
                    "Instrumental space can fill silence without adding new lyrics.",
                )
            )
        if (
            audience.participation_comfort >= 6
            or AudienceExpectation.PARTICIPATION in audience.expectations
        ):
            options.append(
                self._option(
                    ImprovisationOpportunity.ENCOURAGE_AUDIENCE_PARTICIPATION,
                    ImprovisationDecision.ADD_AUDIENCE_PARTICIPATION,
                    (
                        ImprovisationConstraint.AUDIENCE_PARTICIPATION,
                        ImprovisationConstraint.VENUE_EXPECTATIONS,
                    ),
                    "Creates shared energy while depending on a simple, optional cue.",
                    "The audience profile suggests participation can be offered without pressure.",
                )
            )
        if context.needs_transition_continuity:
            options.append(
                self._option(
                    ImprovisationOpportunity.CREATE_SMOOTHER_TRANSITION,
                    ImprovisationDecision.EXTEND_TRANSITION,
                    (
                        ImprovisationConstraint.TRANSITION_CONTINUITY,
                        ImprovisationConstraint.REMAINING_TIME,
                    ),
                    "Protects flow between moments while lengthening the handoff.",
                    "The context names continuity as a current constraint.",
                )
            )
        if context.available_time_seconds <= 30:
            options.append(
                self._option(
                    ImprovisationOpportunity.SHORTEN_PERFORMANCE,
                    ImprovisationDecision.REMOVE_VERSE,
                    (
                        ImprovisationConstraint.REMAINING_TIME,
                        ImprovisationConstraint.VENUE_EXPECTATIONS,
                    ),
                    "Protects the schedule while reducing narrative detail.",
                    "Low remaining time makes shortening a visible option.",
                )
            )
            options.append(
                self._option(
                    ImprovisationOpportunity.FINISH_EARLY,
                    ImprovisationDecision.FINISH_IMMEDIATELY,
                    (
                        ImprovisationConstraint.REMAINING_TIME,
                        ImprovisationConstraint.TRANSITION_CONTINUITY,
                    ),
                    "Ends cleanly now but removes planned development.",
                    "Finishing immediately can be musically clearer than rushing several sections.",
                )
            )
        if context.coordination_demand >= 7:
            options.append(
                self._option(
                    ImprovisationOpportunity.ADJUST_DYNAMICS,
                    ImprovisationDecision.SHORTEN_INTRO,
                    (
                        ImprovisationConstraint.COORDINATION_DEMANDS,
                        ImprovisationConstraint.PERFORMER_READINESS,
                    ),
                    "Reduces attention load while changing the opening shape.",
                    "High coordination demand makes simpler dynamic and form choices "
                    "educationally relevant.",
                )
            )
        return tuple(dict.fromkeys(options))

    def planned_timeline(self, arrangement: Arrangement) -> AdaptivePerformancePlan:
        """Build a planned timeline from arrangement structure."""
        sections = [TimelineSection("Intro", 20)]
        for section in arrangement.verse_order:
            sections.append(TimelineSection(section.title(), 35))
            if "verse" in section.lower():
                sections.append(TimelineSection("Chorus", 35))
        if arrangement.uses_bridge:
            sections.append(TimelineSection("Bridge", 30))
        sections.extend(
            TimelineSection("Chorus", 35) for _ in range(arrangement.chorus_repetitions)
        )
        sections.append(TimelineSection("Ending", 20))
        return AdaptivePerformancePlan(
            f"{arrangement.identifier}-planned", arrangement.identifier, tuple(sections)
        )

    def compare(
        self, planned: AdaptivePerformancePlan, adapted: AdaptivePerformancePlan
    ) -> TimelineComparison:
        """Compare timelines without ranking them."""
        differences = [
            f"Planned duration: {planned.total_duration_seconds}s; "
            f"adapted duration: {adapted.total_duration_seconds}s."
        ]
        planned_labels = tuple(s.label for s in planned.sections)
        adapted_labels = tuple(s.label for s in adapted.sections)
        for label in adapted_labels:
            if adapted_labels.count(label) > planned_labels.count(label):
                differences.append(f"Adapted timeline adds or repeats: {label}.")
        for label in planned_labels:
            if label not in adapted_labels:
                differences.append(f"Adapted timeline removes: {label}.")
        return TimelineComparison(
            planned,
            adapted,
            tuple(dict.fromkeys(differences)),
            (
                "Timeline comparison shows flow consequences rather than artistic quality.",
                "A changed plan remains structured when each decision has a musical purpose.",
            ),
        )

    def _option(
        self,
        opportunity: ImprovisationOpportunity,
        decision: ImprovisationDecision,
        constraints: tuple[ImprovisationConstraint, ...],
        tradeoff: str,
        explanation: str,
    ) -> ImprovisationOption:
        return ImprovisationOption(
            opportunity,
            decision,
            constraints,
            (tradeoff, "Constraints influence this choice but do not determine it."),
            f"Consider: {decision.value}.",
            explanation,
        )


class ImprovisationExperimentService:
    """Create immutable adaptive performance plans."""

    def experiment(
        self, plan: AdaptivePerformancePlan, decision: ImprovisationDecision
    ) -> AdaptivePerformancePlan:
        """Apply one named improvisation decision without mutating the original."""
        sections = list(plan.sections)
        rationale = list(plan.rationale)
        if decision is ImprovisationDecision.REPEAT_CHORUS:
            index = self._last_index(sections, "Chorus")
            sections.insert(index + 1, TimelineSection("Chorus", 35, "improvised repeat"))
            rationale.append("Repeating the chorus reinforces a familiar anchor.")
        elif decision is ImprovisationDecision.EXTEND_ENDING:
            sections[-1] = replace(
                sections[-1],
                label="Extended Ending",
                duration_seconds=45,
                source="improvised ending",
            )
            rationale.append("Extending the ending creates a clearer landing.")
        elif decision is ImprovisationDecision.SHORTEN_INTRO:
            sections[0] = replace(sections[0], duration_seconds=8, source="shortened intro")
            rationale.append("Shortening the intro reaches the song sooner.")
        elif decision is ImprovisationDecision.REMOVE_VERSE:
            sections = [s for s in sections if s.label != "Verse"]
            rationale.append("Removing a verse protects time while preserving core material.")
        elif decision is ImprovisationDecision.ADD_AUDIENCE_PARTICIPATION:
            index = self._last_index(sections, "Chorus")
            sections.insert(
                index + 1, TimelineSection("Audience Participation", 25, "improvised invitation")
            )
            rationale.append("Participation turns repetition into a shared moment.")
        elif decision is ImprovisationDecision.INSERT_INSTRUMENTAL_BREAK:
            index = self._last_index(sections, "Chorus")
            sections.insert(
                index + 1, TimelineSection("Instrumental Break", 30, "improvised space")
            )
            rationale.append("Instrumental space fills silence while preserving pulse.")
        elif decision is ImprovisationDecision.EXTEND_TRANSITION:
            sections.append(TimelineSection("Extended Transition", 20, "improvised transition"))
            rationale.append("An extended transition protects continuity into the next moment.")
        elif decision is ImprovisationDecision.FINISH_IMMEDIATELY:
            sections = [
                *sections[: max(1, len(sections) // 2)],
                TimelineSection("Immediate Ending", 10, "early finish"),
            ]
            rationale.append("Finishing immediately chooses clarity over rushing the whole plan.")
        return AdaptivePerformancePlan(
            f"{plan.identifier}-{decision.name.lower().replace('_', '-')}",
            plan.source_plan_identifier,
            tuple(sections),
            (*plan.decisions, decision),
            tuple(rationale),
        )

    def _last_index(self, sections: list[TimelineSection], label: str) -> int:
        for index in range(len(sections) - 1, -1, -1):
            if sections[index].label == label:
                return index
        return max(0, len(sections) - 2)
