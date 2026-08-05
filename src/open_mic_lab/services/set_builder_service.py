"""Chapter 3 deterministic set-building services."""

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


# ruff: noqa: E501
# ruff: noqa: D102

from collections import Counter
from dataclasses import dataclass, replace

from open_mic_lab.domain import (
    EnergyLevel,
    Genre,
    PerformanceRole,
    Repertoire,
    SetList,
    SetTransition,
    Venue,
)
from open_mic_lab.domain.enums import TransitionKind
from open_mic_lab.domain.performance import PerformanceVersion
from open_mic_lab.services.readiness_service import calculate_readiness

ENERGY_POINTS = {
    EnergyLevel.VERY_LOW: 1,
    EnergyLevel.LOW: 2,
    EnergyLevel.MEDIUM: 3,
    EnergyLevel.HIGH: 4,
    EnergyLevel.VERY_HIGH: 5,
}


@dataclass(frozen=True, slots=True)
class TimelineEntry:
    """One deterministic item in a performance timeline."""

    start_seconds: int
    label: str
    duration_seconds: int
    kind: str

    @property
    def start_time(self) -> str:
        minutes, seconds = divmod(self.start_seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"


@dataclass(frozen=True, slots=True)
class SetFlowAnalysis:
    """Structured set analysis that explains tradeoffs instead of one perfect score."""

    overall_assessment: str
    total_duration_seconds: int
    fits_venue: bool
    observations: tuple[str, ...]
    warnings: tuple[str, ...]
    strengths: tuple[str, ...]
    suggested_experiments: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SetComparison:
    """Neutral comparison of two candidate sets."""

    left_name: str
    right_name: str
    differences: tuple[str, ...]
    left_strengths: tuple[str, ...]
    right_strengths: tuple[str, ...]
    left_weaknesses: tuple[str, ...]
    right_weaknesses: tuple[str, ...]
    audience_tradeoffs: tuple[str, ...]


class SetBuilderService:
    """Analyze timelines, flow, experiments, and comparisons for complete sets."""

    def timeline(self, set_list: SetList, repertoire: Repertoire) -> tuple[TimelineEntry, ...]:
        entries: list[TimelineEntry] = []
        elapsed = 0
        for transition in self._transitions_after(set_list, None):
            entries.append(self._transition_entry(transition, elapsed))
            elapsed += transition.estimated_duration_seconds
        for version_id in set_list.ordered_version_identifiers:
            version = repertoire.get_version(version_id)
            song = repertoire.get_song(version.song_identifier)
            entries.append(
                TimelineEntry(elapsed, song.title, version.estimated_duration_seconds, "song")
            )
            elapsed += version.estimated_duration_seconds
            for transition in self._transitions_after(set_list, version_id):
                entries.append(self._transition_entry(transition, elapsed))
                elapsed += transition.estimated_duration_seconds
        return tuple(entries)

    def analyze(self, set_list: SetList, repertoire: Repertoire, venue: Venue) -> SetFlowAnalysis:
        versions = self._versions(set_list, repertoire)
        songs = [repertoire.get_song(version.song_identifier) for version in versions]
        total = sum(entry.duration_seconds for entry in self.timeline(set_list, repertoire))
        limit = min(set_list.target_duration_minutes, venue.typical_set_duration_minutes) * 60
        warnings: list[str] = []
        strengths: list[str] = []
        observations: list[str] = []
        experiments: list[str] = []
        if total > limit:
            warnings.append(
                f"Total running time {self.format_seconds(total)} exceeds the planning limit."
            )
            experiments.append("Shorten a transition or remove the lowest-purpose song.")
        else:
            strengths.append("Total running time fits the venue constraint.")
        if versions:
            opener = versions[0]
            closer = versions[-1]
            if self._role_or_energy(opener, PerformanceRole.OPENER, 3):
                strengths.append(
                    "The opener has a clear opening role or enough energy to focus attention."
                )
            else:
                warnings.append("The opener may not establish attention quickly.")
                experiments.append("Try moving a clearer opener into the first position.")
            if self._role_or_energy(closer, PerformanceRole.CLOSER, 4):
                strengths.append("The closer is positioned to end with confidence or energy.")
            else:
                warnings.append("The closer may not create a strong final impression.")
                experiments.append(
                    "Replace the closer with a higher-readiness or higher-energy song."
                )
        energies = [ENERGY_POINTS[v.energy_level] for v in versions]
        observations.append(
            f"Energy curve: {' -> '.join(str(e) for e in energies) if energies else 'empty set'}."
        )
        if len(set(energies)) > 1:
            strengths.append("Energy contrast gives the audience changes of attention.")
        else:
            warnings.append("Energy stays flat across the set.")
        observations.append(f"Mood balance: {dict(Counter(song.mood.value for song in songs))}.")
        observations.append(
            f"Genre diversity: {dict(Counter(song.genre.value for song in songs))}."
        )
        key_counts = Counter(version.performance_key for version in versions)
        repeated_keys = [key for key, count in key_counts.items() if count > 1]
        if repeated_keys:
            warnings.append(f"Repeated performance key(s): {', '.join(repeated_keys)}.")
        instruments = [v.primary_instrument for v in versions]
        changes = sum(
            1
            for before, after in zip(instruments, instruments[1:], strict=False)
            if before != after
        )
        observations.append(f"Instrument changes: {changes}.")
        if changes and not any(
            t.transition_type is TransitionKind.INSTRUMENT_CHANGE for t in set_list.transitions
        ):
            warnings.append("An instrument change appears without a planned transition.")
        familiar = sum(1 for song in songs if song.estimated_audience_familiarity >= 5)
        originals = sum(1 for song in songs if song.genre is Genre.ORIGINAL)
        observations.append(
            f"Audience familiarity: {familiar}/{len(songs)} songs are likely familiar."
        )
        observations.append(
            f"Original versus cover balance: {originals} original(s), {len(songs) - originals} cover/traditional-style song(s)."
        )
        transition_total = sum(t.estimated_duration_seconds for t in set_list.transitions)
        observations.append(f"Transition timing: {self.format_seconds(transition_total)} total.")
        if not set_list.transitions:
            warnings.append("No transitions are planned; momentum is left to chance.")
            experiments.append("Insert a story, quick segue, or instrument-change transition.")
        assessment = (
            "Engineered set with visible tradeoffs"
            if strengths
            else "Set needs clearer sequencing choices"
        )
        return SetFlowAnalysis(
            assessment,
            total,
            total <= limit,
            tuple(observations),
            tuple(warnings),
            tuple(strengths),
            tuple(dict.fromkeys(experiments)),
        )

    def compare(
        self, left: SetList, right: SetList, repertoire: Repertoire, venue: Venue
    ) -> SetComparison:
        la = self.analyze(left, repertoire, venue)
        ra = self.analyze(right, repertoire, venue)
        differences = (
            f"Duration: {self.format_seconds(la.total_duration_seconds)} vs {self.format_seconds(ra.total_duration_seconds)}.",
            f"Order: {', '.join(left.ordered_version_identifiers)} vs {', '.join(right.ordered_version_identifiers)}.",
        )
        tradeoffs = (
            "A familiar audience may value quick recognition and participation; a listening room may accept slower story pacing.",
            "Instrument changes add color but require transition time and setup attention.",
        )
        return SetComparison(
            left.name,
            right.name,
            differences,
            la.strengths,
            ra.strengths,
            la.warnings,
            ra.warnings,
            tradeoffs,
        )

    def swap_songs(self, set_list: SetList, first: str, second: str) -> SetList:
        ids = list(set_list.ordered_version_identifiers)
        a, b = ids.index(first), ids.index(second)
        ids[a], ids[b] = ids[b], ids[a]
        return replace(
            set_list,
            identifier=f"{set_list.identifier}-swap",
            ordered_version_identifiers=tuple(ids),
        )

    def remove_song(self, set_list: SetList, version_id: str) -> SetList:
        return replace(
            set_list,
            identifier=f"{set_list.identifier}-remove",
            ordered_version_identifiers=tuple(
                v for v in set_list.ordered_version_identifiers if v != version_id
            ),
            transitions=tuple(
                t for t in set_list.transitions if t.after_version_identifier != version_id
            ),
        )

    def replace_song(self, set_list: SetList, old_id: str, new_id: str) -> SetList:
        ids = tuple(new_id if v == old_id else v for v in set_list.ordered_version_identifiers)
        transitions = tuple(
            replace(t, after_version_identifier=new_id)
            if t.after_version_identifier == old_id
            else t
            for t in set_list.transitions
        )
        return replace(
            set_list,
            identifier=f"{set_list.identifier}-replace",
            ordered_version_identifiers=ids,
            transitions=transitions,
        )

    def insert_transition(self, set_list: SetList, transition: SetTransition) -> SetList:
        return replace(
            set_list,
            identifier=f"{set_list.identifier}-transition",
            transitions=(*set_list.transitions, transition),
        )

    def shorten_transition(self, set_list: SetList, transition_id: str, seconds: int) -> SetList:
        transitions = tuple(
            replace(t, estimated_duration_seconds=max(0, t.estimated_duration_seconds - seconds))
            if t.identifier == transition_id
            else t
            for t in set_list.transitions
        )
        return replace(
            set_list, identifier=f"{set_list.identifier}-shorter", transitions=transitions
        )

    def change_opener(self, set_list: SetList, version_id: str) -> SetList:
        ids = [version_id, *(v for v in set_list.ordered_version_identifiers if v != version_id)]
        return replace(
            set_list,
            identifier=f"{set_list.identifier}-opener",
            ordered_version_identifiers=tuple(ids),
        )

    def change_closer(self, set_list: SetList, version_id: str) -> SetList:
        ids = [v for v in set_list.ordered_version_identifiers if v != version_id] + [version_id]
        return replace(
            set_list,
            identifier=f"{set_list.identifier}-closer",
            ordered_version_identifiers=tuple(ids),
        )

    def reorder_by_energy(self, set_list: SetList, repertoire: Repertoire) -> SetList:
        ordered = tuple(
            sorted(
                set_list.ordered_version_identifiers,
                key=lambda v: ENERGY_POINTS[repertoire.get_version(v).energy_level],
            )
        )
        return replace(
            set_list,
            identifier=f"{set_list.identifier}-energy",
            ordered_version_identifiers=ordered,
        )

    def reorder_manually(self, set_list: SetList, ordered_ids: tuple[str, ...]) -> SetList:
        if set(ordered_ids) != set(set_list.ordered_version_identifiers):
            raise ValueError("Manual reorder must contain exactly the existing songs.")
        return replace(
            set_list,
            identifier=f"{set_list.identifier}-manual",
            ordered_version_identifiers=ordered_ids,
        )

    @staticmethod
    def format_seconds(seconds: int) -> str:
        minutes, remainder = divmod(seconds, 60)
        return f"{minutes:02d}:{remainder:02d}"

    @staticmethod
    def _transition_entry(transition: SetTransition, elapsed: int) -> TimelineEntry:
        return TimelineEntry(
            elapsed, transition.notes, transition.estimated_duration_seconds, "transition"
        )

    @staticmethod
    def _transitions_after(set_list: SetList, version_id: str | None) -> tuple[SetTransition, ...]:
        return tuple(t for t in set_list.transitions if t.after_version_identifier == version_id)

    @staticmethod
    def _versions(set_list: SetList, repertoire: Repertoire) -> tuple[PerformanceVersion, ...]:
        return tuple(repertoire.get_version(v) for v in set_list.ordered_version_identifiers)

    @staticmethod
    def _role_or_energy(
        version: PerformanceVersion, role: PerformanceRole, minimum_energy: int
    ) -> bool:
        return (
            role in version.supported_roles
            or ENERGY_POINTS[version.energy_level] >= minimum_energy
            or calculate_readiness(version).score >= 85
        )
