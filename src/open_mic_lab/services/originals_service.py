"""Deterministic original-music presentation services for Chapter 13."""

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


# ruff: noqa: E501, D102

from dataclasses import dataclass, replace

from open_mic_lab.domain import Repertoire
from open_mic_lab.domain.enums import Genre
from open_mic_lab.domain.originals import (
    FamiliarityStrategy,
    OriginalPresentationPlan,
)
from open_mic_lab.domain.performance import SetList


@dataclass(frozen=True, slots=True)
class OriginalMusicAnalysis:
    """Educational analysis of original-song presentation without success prediction."""

    summary: str
    observations: tuple[str, ...]
    opportunities: tuple[str, ...]
    tradeoffs: tuple[str, ...]
    adaptation_suggestions: tuple[str, ...]
    educational_explanations: tuple[str, ...]
    mermaid_diagram: str


@dataclass(frozen=True, slots=True)
class OriginalPresentationComparison:
    """Transparent comparison of two original presentation plans."""

    left_identifier: str
    right_identifier: str
    shared_observations: tuple[str, ...]
    differences: tuple[str, ...]
    reflection_prompts: tuple[str, ...]


class OriginalMusicAnalysisService:
    """Analyze original music as presentation choices, not artistic worth."""

    def analyze(
        self, plan: OriginalPresentationPlan, setlist: SetList, repertoire: Repertoire
    ) -> OriginalMusicAnalysis:
        """Return deterministic educational factors for a presentation plan."""
        observations: list[str] = []
        opportunities: list[str] = []
        tradeoffs: list[str] = []
        suggestions: list[str] = []
        originals = list(plan.original_version_identifiers)
        total = len(plan.ordered_version_identifiers)
        original_positions = [plan.ordered_version_identifiers.index(v) + 1 for v in originals]
        familiar_count = 0
        for version_id in plan.ordered_version_identifiers:
            version = repertoire.get_version(version_id)
            song = repertoire.get_song(version.song_identifier)
            if song.genre is not Genre.ORIGINAL and song.estimated_audience_familiarity >= 6:
                familiar_count += 1
        observations.append(
            f"{len(originals)} original(s) appear in a {total}-song plan at positions {original_positions}."
        )
        if original_positions and min(original_positions) == 1:
            tradeoffs.append(
                "Opening with an original foregrounds identity before familiarity is established."
            )
            suggestions.append("Compare an original opener with a familiar-song opener.")
        if original_positions and max(original_positions) == total:
            tradeoffs.append(
                "Closing with unfamiliar material may leave identity-forward final impression."
            )
        for version_id in originals:
            index = plan.ordered_version_identifiers.index(version_id)
            before = index > 0 and self._is_familiar(
                plan.ordered_version_identifiers[index - 1], repertoire
            )
            after = index < total - 1 and self._is_familiar(
                plan.ordered_version_identifiers[index + 1], repertoire
            )
            if before:
                observations.append(
                    f"{version_id} follows familiar material, giving listeners an anchor."
                )
            else:
                opportunities.append(
                    f"{version_id} could use extra orientation before unfamiliar material."
                )
            if after:
                observations.append(
                    f"{version_id} resolves into familiar material after the original."
                )
        intro_seconds = sum(i.duration_seconds for i in plan.introductions)
        if intro_seconds > 90:
            tradeoffs.append("Longer stories can create meaning while slowing set pacing.")
            suggestions.append("Run the shorten-introduction experiment.")
        elif intro_seconds < 25 * max(1, len(originals)):
            opportunities.append(
                "Brief framing preserves momentum but may leave unfamiliar songs under-contextualized."
            )
        if familiar_count < len(originals):
            opportunities.append(
                "The plan contains more originals than familiar anchors for this audience context."
            )
            suggestions.append("Place an original after familiar song.")
        if plan.context.confidence_level < 7:
            opportunities.append(
                "Performance confidence is modeled as needing a simpler transition into the original."
            )
            suggestions.append("Place the original after the most stable familiar song.")
        if any(
            i.strategy is FamiliarityStrategy.AUDIENCE_PARTICIPATION for i in plan.introductions
        ):
            observations.append(
                "Audience participation is offered as optional access to unfamiliar material."
            )
        explanations = (
            "Original music increases uncertainty because listeners cannot rely on memory.",
            "The engine explains communication, sequencing, and pacing choices; it does not predict success.",
            "Artistic identity fields are reflective prompts rather than creativity measurements.",
        )
        summary = (
            f"{plan.identifier}: originals={len(originals)}, familiar anchors={familiar_count}."
        )
        return OriginalMusicAnalysis(
            summary,
            tuple(dict.fromkeys(observations)),
            tuple(dict.fromkeys(opportunities)),
            tuple(dict.fromkeys(tradeoffs)),
            tuple(dict.fromkeys(suggestions)),
            explanations,
            self.performance_flow(plan, repertoire),
        )

    def compare(
        self,
        left: OriginalPresentationPlan,
        right: OriginalPresentationPlan,
        repertoire: Repertoire,
    ) -> OriginalPresentationComparison:
        """Compare two plans transparently without ranking them."""
        dummy_set = SetList(
            left.setlist_identifier, "comparison", left.ordered_version_identifiers, 15, "venue"
        )
        left_analysis = self.analyze(left, dummy_set, repertoire)
        dummy_set_right = replace(
            dummy_set, ordered_version_identifiers=right.ordered_version_identifiers
        )
        right_analysis = self.analyze(right, dummy_set_right, repertoire)
        shared = tuple(o for o in left_analysis.observations if o in right_analysis.observations)
        differences = tuple(
            dict.fromkeys(
                [
                    f"{left.identifier}: {item}"
                    for item in left_analysis.observations + left_analysis.tradeoffs
                ]
                + [
                    f"{right.identifier}: {item}"
                    for item in right_analysis.observations + right_analysis.tradeoffs
                ]
            )
        )
        return OriginalPresentationComparison(
            left.identifier,
            right.identifier,
            shared,
            differences,
            (
                "Which plan gives the audience enough context without explaining the song away?",
                "Where does familiar material help unfamiliar material feel intentional?",
                "What does this sequence reveal about the performer's artistic identity?",
            ),
        )

    def performance_flow(self, plan: OriginalPresentationPlan, repertoire: Repertoire) -> str:
        """Create a deterministic plain-text performance flow summary."""
        labels = ["Performance Flow"]
        for version_id in plan.ordered_version_identifiers:
            version = repertoire.get_version(version_id)
            song = repertoire.get_song(version.song_identifier)
            prefix = (
                "Original Song"
                if version_id in plan.original_version_identifiers
                else "Familiar Song"
            )
            labels.append(f"{prefix}: {song.title}")
        return "\n↓\n".join(labels)

    def mermaid(self, plan: OriginalPresentationPlan, repertoire: Repertoire) -> str:
        """Create a deterministic Mermaid flowchart."""
        lines = ["flowchart TD"]
        for index, version_id in enumerate(plan.ordered_version_identifiers):
            song = repertoire.get_song(repertoire.get_version(version_id).song_identifier)
            label = (
                f"Original: {song.title}"
                if version_id in plan.original_version_identifiers
                else song.title
            )
            lines.append(f"    S{index}[{label}]")
            if index:
                lines.append(f"    S{index - 1} --> S{index}")
        return "\n".join(lines)

    def _is_familiar(self, version_id: str, repertoire: Repertoire) -> bool:
        song = repertoire.get_song(repertoire.get_version(version_id).song_identifier)
        return song.genre is not Genre.ORIGINAL and song.estimated_audience_familiarity >= 6


class OriginalPresentationExperimentService:
    """Immutable placement and story experiments for original presentation plans."""

    def move_original_earlier(
        self, plan: OriginalPresentationPlan, version_id: str | None = None
    ) -> OriginalPresentationPlan:
        return self._move(plan, version_id or plan.original_version_identifiers[0], -1, "earlier")

    def move_original_later(
        self, plan: OriginalPresentationPlan, version_id: str | None = None
    ) -> OriginalPresentationPlan:
        return self._move(plan, version_id or plan.original_version_identifiers[0], 1, "later")

    def place_original_after_familiar_song(
        self, plan: OriginalPresentationPlan, familiar_version_id: str
    ) -> OriginalPresentationPlan:
        original = plan.original_version_identifiers[0]
        order = [v for v in plan.ordered_version_identifiers if v != original]
        index = order.index(familiar_version_id) + 1
        order.insert(index, original)
        return replace(
            plan,
            identifier=f"{plan.identifier}-after-familiar",
            ordered_version_identifiers=tuple(order),
        )

    def place_original_before_familiar_closer(
        self, plan: OriginalPresentationPlan
    ) -> OriginalPresentationPlan:
        original = plan.original_version_identifiers[0]
        closer = plan.ordered_version_identifiers[-1]
        order = [v for v in plan.ordered_version_identifiers if v != original]
        order.insert(order.index(closer), original)
        return replace(
            plan,
            identifier=f"{plan.identifier}-before-closer",
            ordered_version_identifiers=tuple(order),
        )

    def shorten_introduction(self, plan: OriginalPresentationPlan) -> OriginalPresentationPlan:
        return replace(
            plan,
            identifier=f"{plan.identifier}-short-story",
            introductions=tuple(
                replace(i, duration_seconds=max(10, i.duration_seconds // 2))
                for i in plan.introductions
            ),
        )

    def lengthen_story(self, plan: OriginalPresentationPlan) -> OriginalPresentationPlan:
        return replace(
            plan,
            identifier=f"{plan.identifier}-longer-story",
            introductions=tuple(
                replace(
                    i,
                    duration_seconds=i.duration_seconds + 20,
                    strategy=FamiliarityStrategy.PERSONAL_STORY,
                )
                for i in plan.introductions
            ),
        )

    def pair_with_audience_participation(
        self, plan: OriginalPresentationPlan
    ) -> OriginalPresentationPlan:
        return replace(
            plan,
            identifier=f"{plan.identifier}-participation",
            introductions=tuple(
                replace(
                    i,
                    strategy=FamiliarityStrategy.AUDIENCE_PARTICIPATION,
                    story_theme=i.story_theme or "shared refrain",
                )
                for i in plan.introductions
            ),
        )

    def replace_familiar_song_with_original(
        self, plan: OriginalPresentationPlan, familiar_version_id: str, original_version_id: str
    ) -> OriginalPresentationPlan:
        order = tuple(
            original_version_id if v == familiar_version_id else v
            for v in plan.ordered_version_identifiers
        )
        originals = tuple(dict.fromkeys(plan.original_version_identifiers + (original_version_id,)))
        return replace(
            plan,
            identifier=f"{plan.identifier}-more-originals",
            ordered_version_identifiers=order,
            original_version_identifiers=originals,
        )

    def _move(
        self, plan: OriginalPresentationPlan, version_id: str, delta: int, suffix: str
    ) -> OriginalPresentationPlan:
        order = list(plan.ordered_version_identifiers)
        index = order.index(version_id)
        destination = min(max(index + delta, 0), len(order) - 1)
        order.pop(index)
        order.insert(destination, version_id)
        return replace(
            plan, identifier=f"{plan.identifier}-{suffix}", ordered_version_identifiers=tuple(order)
        )
