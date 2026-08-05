"""Deterministic audience-experience services for Chapter 10."""

# Evidence basis for scoring and recommendation services.
#
# Purpose: provide deterministic educational comparisons for repertoire,
# practice, stagecraft, audio workflow, audience scenarios, recovery,
# improvisation, and reflection.
# Inputs: typed domain objects and bounded scenario data in the repository.
# Outputs: scores, categories, warnings, recommendations, and explanation text.
# Evidence Basis: music education, performance psychology, feedback research,
# self-regulated learning, cognitive-load theory, live-sound practice, and
# simulation-based learning motivate the concepts represented here.
# Repository Contribution: exact weights, thresholds, and formula structures are
# original educational heuristics designed for transparent experimentation.
# Limitations: outputs are non-predictive learning aids. They are not validated
# measurements of artistic worth, audience response, technical safety, or future
# performance success.

from dataclasses import dataclass, replace

from open_mic_lab.domain.audience import (
    AudienceFeedbackSummary,
    AudiencePerformance,
    AudiencePerformanceMoment,
    AudienceProfile,
    AudienceResponse,
    EngagementObservation,
    ParticipationOpportunity,
    PerformanceMoment,
)


@dataclass(frozen=True, slots=True)
class AudienceExperimentResult:
    """Immutable experiment output with before and after analyses."""

    experiment_name: str
    original_performance: AudiencePerformance
    changed_performance: AudiencePerformance
    original_response: AudienceResponse
    changed_response: AudienceResponse


class AudienceResponseService:
    """Analyze educational audience factors without predicting emotions."""

    def analyze(
        self, performance: AudiencePerformance, profile: AudienceProfile
    ) -> AudienceResponse:
        """Return structured observations for a performance and audience profile."""
        strengths: list[str] = []
        friction: list[str] = []
        ideas: list[str] = []
        explanations: list[EngagementObservation] = []
        song_moments = [m for m in performance.moments if m.kind is PerformanceMoment.SONG]
        familiar_count = sum(1 for m in song_moments if m.familiarity >= 6)
        unfamiliar_runs = self._longest_unfamiliar_run(song_moments)
        avg_transition = sum(m.transition_quality for m in performance.moments) / len(
            performance.moments
        )
        storytelling_seconds = sum(
            m.duration_seconds for m in performance.moments if m.storytelling
        )
        participation_count = sum(1 for m in performance.moments if m.participation is not None)
        energy_curve = tuple(m.energy for m in song_moments)

        if song_moments and song_moments[0].energy >= 5 and song_moments[0].familiarity >= 5:
            strengths.append("Strong opening song gives listeners early orientation.")
        else:
            friction.append("The opening may ask for attention before orientation is established.")
            ideas.append("Move a clearer or more familiar song earlier.")
        explanations.append(
            EngagementObservation(
                "opening",
                "Openers are modeled as orientation moments, not guarantees of approval.",
                "Test a familiar or higher-clarity opener.",
            )
        )

        if profile.familiarity_preference >= 7 and unfamiliar_runs >= 2:
            friction.append("Multiple unfamiliar songs in succession may reduce accessibility.")
            ideas.append("Replace one unfamiliar song or move a familiar song earlier.")
        elif familiar_count >= max(1, len(song_moments) // 2):
            strengths.append("Familiar material is spaced through the sequence.")
        explanations.append(
            EngagementObservation(
                "familiarity",
                f"This profile has familiarity preference {profile.familiarity_preference}/10; "
                f"the set has {familiar_count}/{len(song_moments)} familiar song moments.",
            )
        )

        if avg_transition >= 7:
            strengths.append("Transitions are clear enough to support pacing.")
        else:
            friction.append("Uneven transitions may make the sequence feel less intentional.")
            ideas.append("Simplify transitions between contrasting moments.")
        explanations.append(
            EngagementObservation(
                "transition quality",
                "Transition quality is an explicit learner-supplied factor "
                "separate from confidence.",
            )
        )

        if storytelling_seconds > profile.storytelling_tolerance * 12:
            friction.append("Storytelling may exceed this profile's modeled patience.")
            ideas.append("Shorten one spoken segment.")
        elif storytelling_seconds and profile.storytelling_tolerance >= 5:
            strengths.append("Storytelling fits this audience profile well.")
        explanations.append(
            EngagementObservation(
                "storytelling",
                "Stories are treated as context and pacing choices, not proof of connection.",
                "Compare reduced and expanded storytelling versions.",
            )
        )

        if participation_count and profile.participation_comfort >= 5:
            strengths.append("Participation opportunities are optional and accessible.")
        elif profile.participation_comfort >= 7:
            friction.append("This profile may benefit from a low-pressure participation option.")
            ideas.append("Add an optional refrain, clap, or call-and-response moment.")
        explanations.append(
            EngagementObservation(
                "participation",
                "Participation is modeled as an opportunity, never an expected audience behavior.",
            )
        )

        if len(set(energy_curve)) >= min(3, len(energy_curve)):
            strengths.append("Energy progression includes useful variety.")
        elif profile.variety_preference >= 6:
            friction.append("Similar energy across songs may reduce contrast for this profile.")
            ideas.append("Change order or arrangement energy to create more contrast.")
        if performance.duration_seconds > 900 and profile.pacing_patience <= 5:
            friction.append("Performance length may be ambitious for this audience context.")
            ideas.append("Shorten the performance.")

        if not ideas:
            ideas.append("Compare the same set against another audience profile.")
        return AudienceResponse(
            profile.identifier,
            tuple(dict.fromkeys(strengths)),
            tuple(dict.fromkeys(friction)),
            tuple(dict.fromkeys(ideas)),
            tuple(explanations),
            self.mermaid(performance),
        )

    def compare(
        self,
        performance: AudiencePerformance,
        left: AudienceProfile,
        right: AudienceProfile,
    ) -> AudienceFeedbackSummary:
        """Compare observations for two audience profiles."""
        left_response = self.analyze(performance, left)
        right_response = self.analyze(performance, right)
        shared = tuple(s for s in left_response.strengths if s in right_response.strengths)
        differences = tuple(
            dict.fromkeys(
                [f"{left.name}: {item}" for item in left_response.friction_points]
                + [f"{right.name}: {item}" for item in right_response.friction_points]
            )
        )
        prompts = (
            "Which adaptation preserves artistic authenticity?",
            "Which difference comes from audience context rather than song quality?",
            "What would you observe after the performance without treating it as prediction?",
        )
        return AudienceFeedbackSummary(left.name, right.name, shared, differences, prompts)

    def mermaid(self, performance: AudiencePerformance) -> str:
        """Create a deterministic Mermaid flow diagram for the moments."""
        lines = ["flowchart LR"]
        for index, moment in enumerate(performance.moments):
            node = f"M{index}"
            lines.append(f"    {node}[{moment.label}]")
            if index:
                lines.append(f"    M{index - 1} --> {node}")
        return "\n".join(lines)

    def _longest_unfamiliar_run(self, moments: list[AudiencePerformanceMoment]) -> int:
        longest = 0
        current = 0
        for moment in moments:
            if moment.familiarity < 5:
                current += 1
                longest = max(longest, current)
            else:
                current = 0
        return longest


class AudienceExperimentService:
    """Immutable adaptation experiments for audience experience."""

    def __init__(self, analyzer: AudienceResponseService | None = None) -> None:
        self._analyzer = analyzer or AudienceResponseService()

    def increase_interaction(
        self, performance: AudiencePerformance, profile: AudienceProfile
    ) -> AudienceExperimentResult:
        """Add a low-pressure participation moment before the closer."""
        opportunity = ParticipationOpportunity(
            "Invite a simple final chorus hum.", "added-participation", 8
        )
        changed = replace(
            performance,
            identifier=f"{performance.identifier}-participation",
            moments=performance.moments[:-1]
            + (
                AudiencePerformanceMoment(
                    "added-participation",
                    PerformanceMoment.PARTICIPATION,
                    "Audience participation",
                    20,
                    6,
                    6,
                    8,
                    8,
                    participation=opportunity,
                ),
            )
            + performance.moments[-1:],
        )
        return self._result("increase audience interaction", performance, changed, profile)

    def reduce_storytelling(
        self, performance: AudiencePerformance, profile: AudienceProfile
    ) -> AudienceExperimentResult:
        """Shorten storytelling moments while preserving the sequence."""
        changed = replace(
            performance,
            identifier=f"{performance.identifier}-less-story",
            moments=tuple(
                replace(moment, duration_seconds=max(20, moment.duration_seconds // 2))
                if moment.storytelling
                else moment
                for moment in performance.moments
            ),
        )
        return self._result("reduce storytelling", performance, changed, profile)

    def replace_one_unfamiliar_song(
        self, performance: AudiencePerformance, profile: AudienceProfile
    ) -> AudienceExperimentResult:
        """Make the first unfamiliar song moment more familiar."""
        changed_moments = []
        replaced = False
        for moment in performance.moments:
            if not replaced and moment.kind is PerformanceMoment.SONG and moment.familiarity < 5:
                changed_moments.append(
                    replace(moment, label=f"{moment.label} (familiar substitute)", familiarity=7)
                )
                replaced = True
            else:
                changed_moments.append(moment)
        changed = replace(
            performance,
            identifier=f"{performance.identifier}-familiarity",
            moments=tuple(changed_moments),
        )
        return self._result("replace one unfamiliar song", performance, changed, profile)

    def add_familiar_closer(
        self, performance: AudiencePerformance, profile: AudienceProfile
    ) -> AudienceExperimentResult:
        """Make the final song moment a familiar closer."""
        moments = list(performance.moments)
        for index in range(len(moments) - 1, -1, -1):
            if moments[index].kind is PerformanceMoment.SONG:
                moments[index] = replace(
                    moments[index], label="Familiar closer", familiarity=8, energy=8
                )
                break
        changed = replace(
            performance, identifier=f"{performance.identifier}-closer", moments=tuple(moments)
        )
        return self._result("add a familiar closer", performance, changed, profile)

    def shorten_performance(
        self, performance: AudiencePerformance, profile: AudienceProfile
    ) -> AudienceExperimentResult:
        """Remove the longest non-opening story or reflection moment."""
        removable = [
            m
            for m in performance.moments
            if m.kind in {PerformanceMoment.STORY, PerformanceMoment.QUIET_REFLECTION}
        ]
        target = max(removable, key=lambda m: m.duration_seconds) if removable else None
        changed = replace(
            performance,
            identifier=f"{performance.identifier}-shorter",
            moments=tuple(m for m in performance.moments if m is not target),
        )
        return self._result("shorten the performance", performance, changed, profile)

    def simplify_transitions(
        self, performance: AudiencePerformance, profile: AudienceProfile
    ) -> AudienceExperimentResult:
        """Raise low transition-quality moments by simplifying them."""
        changed = replace(
            performance,
            identifier=f"{performance.identifier}-simple-transitions",
            moments=tuple(
                replace(moment, transition_quality=max(moment.transition_quality, 7))
                for moment in performance.moments
            ),
        )
        return self._result("simplify transitions", performance, changed, profile)

    def _result(
        self,
        name: str,
        original: AudiencePerformance,
        changed: AudiencePerformance,
        profile: AudienceProfile,
    ) -> AudienceExperimentResult:
        return AudienceExperimentResult(
            name,
            original,
            changed,
            self._analyzer.analyze(original, profile),
            self._analyzer.analyze(changed, profile),
        )
