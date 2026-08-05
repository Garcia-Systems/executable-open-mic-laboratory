"""Deterministic Chapter 7 communication analysis services."""

from dataclasses import dataclass, replace

from open_mic_lab.domain.stage import (
    AudienceFamiliarity,
    AudienceInteraction,
    CommunicationPlan,
    IntroductionPurpose,
    PerformerBehavior,
    StageMoment,
    StorySegment,
)


@dataclass(frozen=True, slots=True)
class CommunicationAnalysis:
    """Transparent communication analysis without a single presence score."""

    summary: str
    observations: tuple[str, ...]
    strengths: tuple[str, ...]
    opportunities: tuple[str, ...]
    suggested_experiments: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CommunicationComparison:
    """Before/after comparison for immutable communication experiments."""

    original_summary: str
    changed_summary: str
    differences: tuple[str, ...]


class CommunicationAnalysisService:
    """Analyze stage presence as intentional audience communication."""

    def analyze(self, plan: CommunicationPlan) -> CommunicationAnalysis:
        """Analyze the full plan deterministically."""
        observations = list(self.analyze_introductions(plan)) + list(self.analyze_flow(plan))
        strengths: list[str] = []
        opportunities: list[str] = []
        experiments: list[str] = []
        remaining = plan.available_spoken_seconds - plan.planned_spoken_seconds
        if remaining >= 0:
            strengths.append(
                f"Spoken plan fits with {remaining} seconds available for breathing room."
            )
        else:
            opportunities.append(f"Spoken plan exceeds available time by {abs(remaining)} seconds.")
            experiments.append("shorten introduction")
        if plan.interactions:
            strengths.append("Audience interaction is planned instead of left to chance.")
        else:
            opportunities.append(
                "No audience interaction is planned; connection relies on songs alone."
            )
            experiments.append("invite audience participation")
        if plan.flow.confidence_continuity >= 7:
            strengths.append("Confidence continuity remains steady across transitions.")
        else:
            opportunities.append("Confidence may visibly reset between songs.")
            experiments.append("reduce silence")
        if plan.flow.storytelling_opportunities > len([i for i in plan.introductions if i.story]):
            experiments.append("add personal story")
        summary = (
            f"{plan.identifier}: {len(plan.introductions)} introductions, "
            f"{len(plan.interactions)} interactions, {plan.planned_spoken_seconds}/"
            f"{plan.available_spoken_seconds} spoken seconds planned."
        )
        return CommunicationAnalysis(
            summary,
            tuple(observations),
            tuple(strengths),
            tuple(opportunities),
            tuple(dict.fromkeys(experiments)),
        )

    def analyze_introductions(self, plan: CommunicationPlan) -> tuple[str, ...]:
        """Evaluate structured introductions against time and purpose."""
        observations: list[str] = []
        for index, intro in enumerate(plan.introductions, start=1):
            if intro.total_duration_seconds > 60:
                observations.append(
                    "Introduction before Song "
                    f"{index} may slow pacing at {intro.total_duration_seconds} seconds."
                )
            elif intro.total_duration_seconds <= 20:
                observations.append(
                    f"Brief introduction before Song {index} preserves performance momentum."
                )
            if intro.audience_familiarity is AudienceFamiliarity.LOW and intro.story is None:
                observations.append(
                    f"Song {index} is unfamiliar; a brief context or story may improve connection."
                )
            if intro.purpose is IntroductionPurpose.PARTICIPATION:
                observations.append(
                    f"Introduction before Song {index} prepares audience participation."
                )
        return tuple(observations)

    def analyze_flow(self, plan: CommunicationPlan) -> tuple[str, ...]:
        """Evaluate silence, pacing, confidence, and transitions across the set."""
        observations: list[str] = []
        for index, silence in enumerate(plan.flow.silence_between_songs_seconds, start=1):
            if silence > 25:
                observations.append(
                    f"Long silence between Songs {index} and {index + 1} interrupts momentum."
                )
            elif silence <= 8:
                observations.append(
                    f"Short silence between Songs {index} and {index + 1} keeps pacing active."
                )
        story_count = sum(1 for intro in plan.introductions if intro.story is not None)
        if story_count >= 2:
            observations.append(
                "Two consecutive stories may reduce pacing unless contrast is intentional."
            )
        if plan.flow.eye_contact_opportunities >= len(plan.introductions):
            observations.append("Eye-contact opportunities are available before most songs.")
        if plan.flow.transition_smoothness < 6:
            observations.append("Transitions may feel technically busy instead of communicative.")
        if PerformerBehavior.RECOVERY_BREATH in plan.flow.behaviors:
            observations.append("A recovery breath gives mistakes a visible reset plan.")
        if any(interaction.moment is StageMoment.BEFORE_SONG for interaction in plan.interactions):
            observations.append("Audience participation naturally fits before a song entrance.")
        return tuple(observations)

    def compare(
        self, original: CommunicationPlan, changed: CommunicationPlan
    ) -> CommunicationComparison:
        """Compare communication plans without selecting a winner."""
        original_analysis = self.analyze(original)
        changed_analysis = self.analyze(changed)
        differences = (
            "Spoken time changed from "
            f"{original.planned_spoken_seconds} to {changed.planned_spoken_seconds} seconds.",
            "Interaction count changed from "
            f"{len(original.interactions)} to {len(changed.interactions)}.",
            "Observation count changed from "
            f"{len(original_analysis.observations)} to {len(changed_analysis.observations)}.",
        )
        return CommunicationComparison(
            original_analysis.summary, changed_analysis.summary, differences
        )


class CommunicationExperimentService:
    """Immutable experiments for communication choices."""

    def shorten_introduction(
        self, plan: CommunicationPlan, introduction_identifier: str, seconds: int = 15
    ) -> CommunicationPlan:
        """Return a plan with one introduction shortened."""
        introductions = tuple(
            replace(
                intro,
                estimated_duration_seconds=max(10, intro.estimated_duration_seconds - seconds),
            )
            if intro.identifier == introduction_identifier
            else intro
            for intro in plan.introductions
        )
        return replace(plan, identifier=f"{plan.identifier}-shortened", introductions=introductions)

    def remove_introduction(
        self, plan: CommunicationPlan, introduction_identifier: str
    ) -> CommunicationPlan:
        """Return a plan with one introduction removed."""
        return replace(
            plan,
            identifier=f"{plan.identifier}-removed-intro",
            introductions=tuple(
                i for i in plan.introductions if i.identifier != introduction_identifier
            ),
        )

    def add_personal_story(
        self,
        plan: CommunicationPlan,
        introduction_identifier: str,
        theme: str = "why this song matters",
    ) -> CommunicationPlan:
        """Return a plan with a concise personal story attached."""
        introductions = tuple(
            replace(
                intro,
                story=StorySegment(theme, 25, personal=True, connects_to_song=True),
            )
            if intro.identifier == introduction_identifier
            else intro
            for intro in plan.introductions
        )
        return replace(plan, identifier=f"{plan.identifier}-story", introductions=introductions)

    def invite_audience_participation(self, plan: CommunicationPlan) -> CommunicationPlan:
        """Return a plan with a simple audience invitation before the closing song."""
        interaction = AudienceInteraction(
            "closing-participation",
            StageMoment.BEFORE_SONG,
            "Invite the audience to sing the final repeated line if they want to.",
            15,
            6,
        )
        return replace(
            plan,
            identifier=f"{plan.identifier}-participation",
            interactions=plan.interactions + (interaction,),
        )

    def reduce_silence(
        self, plan: CommunicationPlan, maximum_seconds: int = 12
    ) -> CommunicationPlan:
        """Return a plan with long silences capped."""
        flow = replace(
            plan.flow,
            silence_between_songs_seconds=tuple(
                min(silence, maximum_seconds) for silence in plan.flow.silence_between_songs_seconds
            ),
        )
        return replace(plan, identifier=f"{plan.identifier}-less-silence", flow=flow)

    def extend_transition(
        self, plan: CommunicationPlan, index: int, seconds: int = 10
    ) -> CommunicationPlan:
        """Return a plan with one transition silence intentionally extended."""
        silences = list(plan.flow.silence_between_songs_seconds)
        silences[index] += seconds
        return replace(
            plan,
            identifier=f"{plan.identifier}-extended-transition",
            flow=replace(plan.flow, silence_between_songs_seconds=tuple(silences)),
        )

    def increase_audience_interaction(self, plan: CommunicationPlan) -> CommunicationPlan:
        """Return a plan with a lightweight check-in interaction."""
        interaction = AudienceInteraction(
            "warm-check-in",
            StageMoment.BEFORE_SET,
            "Smile, thank the room, and acknowledge the host.",
            10,
            3,
        )
        return replace(
            plan,
            identifier=f"{plan.identifier}-more-interaction",
            interactions=(interaction,) + plan.interactions,
        )

    def simplify_spoken_segments(self, plan: CommunicationPlan) -> CommunicationPlan:
        """Return a plan with stories removed and introductions made concise."""
        introductions = tuple(
            replace(
                intro,
                estimated_duration_seconds=min(intro.estimated_duration_seconds, 20),
                story=None,
            )
            for intro in plan.introductions
        )
        return replace(
            plan, identifier=f"{plan.identifier}-simplified", introductions=introductions
        )
