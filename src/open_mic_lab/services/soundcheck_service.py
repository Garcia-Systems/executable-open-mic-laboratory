"""Deterministic Chapter 9 sound-check services."""

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


# ruff: noqa: D101, D102, E501

from collections.abc import Callable
from dataclasses import dataclass, replace

from open_mic_lab.domain.equipment import NodeRole, OutputRole, SignalPath
from open_mic_lab.domain.soundcheck import (
    BalanceAssessment,
    ChannelSettings,
    EQProfile,
    FeedbackRisk,
    MonitorMix,
    SoundCheck,
)


@dataclass(frozen=True, slots=True)
class SoundCheckAnalysis:
    """Structured result from a deterministic sound-check analysis."""

    soundcheck_id: str
    vocal_balance: BalanceAssessment
    accompaniment_balance: BalanceAssessment
    monitor_balance: BalanceAssessment
    feedback_risk: FeedbackRisk
    clipping_risk: bool
    insufficient_gain: tuple[str, ...]
    unused_channels: tuple[str, ...]
    observations: tuple[str, ...]
    suggested_adjustments: tuple[str, ...]
    warnings: tuple[str, ...]
    strengths: tuple[str, ...]
    educational_explanation: str


@dataclass(frozen=True, slots=True)
class WorkflowStep:
    """One step in a repeatable sound-check workflow."""

    number: int
    name: str
    observation: str
    action: str


@dataclass(frozen=True, slots=True)
class SoundCheckComparison:
    """Before/after comparison between two mixer configurations."""

    original_id: str
    changed_id: str
    differences: tuple[str, ...]


class SoundCheckService:
    """Analyze live-mix decisions without pretending to find a perfect mix."""

    def analyze(self, soundcheck: SoundCheck, signal_path: SignalPath) -> SoundCheckAnalysis:
        """Return observations, warnings, strengths, and suggested adjustments."""
        channels = soundcheck.mixer_settings.channels
        vocal = self._channel(channels, "vocal")
        accomp = tuple(c for c in channels if "vocal" not in c.label.lower())
        vocal_score = self._house_score(vocal, soundcheck.mixer_settings.master_level)
        accomp_score = max(
            (self._house_score(c, soundcheck.mixer_settings.master_level) for c in accomp),
            default=0,
        )
        vocal_balance = self._balance(vocal_score, 4, 7)
        accomp_balance = self._balance(accomp_score, 3, 6)
        monitor_score = soundcheck.mixer_settings.monitor_mix.overall_level
        monitor_balance = self._balance(monitor_score, 4, 7)
        feedback_points = (
            soundcheck.venue.reflectivity
            + soundcheck.venue.monitor_sensitivity
            + monitor_score
            + (vocal.gain if vocal else 0)
            - soundcheck.venue.audience_absorption
        )
        feedback = (
            FeedbackRisk.HIGH
            if feedback_points >= 24
            else FeedbackRisk.MODERATE
            if feedback_points >= 18
            else FeedbackRisk.LOW
        )
        clipping = (
            any(not c.muted and c.gain + c.fader >= 17 for c in channels)
            or soundcheck.mixer_settings.master_level >= 9
        )
        insufficient = tuple(
            c.channel_id for c in channels if not c.muted and c.gain + c.fader <= 5
        )
        source_ids = {
            n.identifier
            for n in signal_path.nodes
            if n.role in {NodeRole.MICROPHONE, NodeRole.PICKUP, NodeRole.INSTRUMENT_OUTPUT}
        }
        unused = tuple(c.channel_id for c in channels if c.source_node not in source_ids or c.muted)
        observations = [
            f"Venue profile: {soundcheck.venue.name} ({soundcheck.venue.room_size}); values are educational approximations.",
            f"Vocal balance is {vocal_balance.value}.",
            f"Accompaniment balance is {accomp_balance.value}.",
            f"Monitor balance is {monitor_balance.value}.",
        ]
        suggestions: list[str] = []
        warnings: list[str] = []
        strengths: list[str] = []
        if vocal_balance in {BalanceAssessment.TOO_QUIET, BalanceAssessment.SLIGHTLY_QUIET}:
            suggestions.append("Raise vocal gain or fader one small step, then listen again.")
        if accomp_balance in {BalanceAssessment.SLIGHTLY_LOUD, BalanceAssessment.TOO_LOUD}:
            suggestions.append("Reduce accompaniment before pushing the vocal louder.")
        if monitor_balance in {BalanceAssessment.TOO_QUIET, BalanceAssessment.SLIGHTLY_QUIET}:
            suggestions.append("Raise monitor level enough for comfort, not for audience volume.")
        if feedback is FeedbackRisk.HIGH:
            warnings.append(
                "Feedback risk is high; lower monitor level, reduce vocal gain, or increase mic distance."
            )
        if clipping:
            warnings.append("Clipping risk detected from high gain, fader, or master level.")
        if insufficient:
            warnings.append("Some active channels may not have enough gain to be useful.")
        if unused:
            warnings.append(
                "Unused or muted channels should be named intentionally so routing mistakes stand out."
            )
        if vocal_balance is BalanceAssessment.BALANCED:
            strengths.append("Lyrics have a workable place in the house mix.")
        if monitor_balance is BalanceAssessment.BALANCED:
            strengths.append(
                "Performer monitoring is likely comfortable enough for a short passage."
            )
        if any(n.output_role is OutputRole.AUDIENCE for n in signal_path.nodes):
            strengths.append(
                "The sound check builds on a signal path with an audience destination."
            )
        return SoundCheckAnalysis(
            soundcheck.identifier,
            vocal_balance,
            accomp_balance,
            monitor_balance,
            feedback,
            clipping,
            insufficient,
            unused,
            tuple(observations),
            tuple(suggestions),
            tuple(warnings),
            tuple(strengths),
            "A sound check is a sequence of listening decisions: confirm routing, set usable gain, balance sources, then adjust monitors for performer comfort in this room.",
        )

    def workflow(self, soundcheck: SoundCheck, signal_path: SignalPath) -> tuple[WorkflowStep, ...]:
        """Return a structured seven-step sound-check workflow."""
        analysis = self.analyze(soundcheck, signal_path)
        return (
            WorkflowStep(
                1,
                "verify signal path",
                "Audience and performer destinations are checked before tone decisions.",
                "Confirm every cable and powered speaker.",
            ),
            WorkflowStep(
                2,
                "check vocal microphone",
                f"Vocal is {analysis.vocal_balance.value}.",
                "Speak and sing at performance distance.",
            ),
            WorkflowStep(
                3,
                "check accompaniment",
                f"Accompaniment is {analysis.accompaniment_balance.value}.",
                "Play the loudest expected passage.",
            ),
            WorkflowStep(
                4,
                "balance house mix",
                "The house mix is judged by relative clarity, not maximum volume.",
                "Make one fader change at a time.",
            ),
            WorkflowStep(
                5,
                "balance monitors",
                f"Monitor is {analysis.monitor_balance.value}.",
                "Ask whether the performer can hear pitch and timing.",
            ),
            WorkflowStep(
                6,
                "perform short musical passage",
                f"Feedback risk is {analysis.feedback_risk.value}.",
                "Test the real chorus, not only isolated notes.",
            ),
            WorkflowStep(
                7,
                "confirm performer comfort",
                "Comfort matters because tension changes performance quality.",
                "Name the final tradeoff before starting the set.",
            ),
        )

    def compare(
        self, original: SoundCheck, changed: SoundCheck, signal_path: SignalPath
    ) -> SoundCheckComparison:
        """Compare two mixes without declaring either universally perfect."""
        left = self.analyze(original, signal_path)
        right = self.analyze(changed, signal_path)
        return SoundCheckComparison(
            original.identifier,
            changed.identifier,
            (
                f"Vocal balance changed from {left.vocal_balance.value} to {right.vocal_balance.value}.",
                f"Accompaniment balance changed from {left.accompaniment_balance.value} to {right.accompaniment_balance.value}.",
                f"Monitor balance changed from {left.monitor_balance.value} to {right.monitor_balance.value}.",
                f"Feedback risk changed from {left.feedback_risk.value} to {right.feedback_risk.value}.",
                f"Warnings changed from {len(left.warnings)} to {len(right.warnings)}.",
            ),
        )

    def text_report(self, analysis: SoundCheckAnalysis) -> str:
        """Format a deterministic learner-facing report."""
        lines = ["House Mix"]
        lines.append(f"Vocals .......... {analysis.vocal_balance.value.title()}")
        lines.append(f"Piano ........... {analysis.accompaniment_balance.value.title()}")
        lines.append(f"Monitor ......... {analysis.monitor_balance.value.title()}")
        lines.append("Observations")
        lines.extend(f"✓ {s}" for s in analysis.strengths)
        lines.extend(f"⚠ {w}" for w in analysis.warnings)
        lines.extend(f"→ {s}" for s in analysis.suggested_adjustments)
        return "\n".join(lines)

    def mermaid(self, soundcheck: SoundCheck) -> str:
        """Return a small Mermaid diagram for documentation and notebooks."""
        return "\n".join(
            (
                "flowchart LR",
                "    Venue --> Mixer",
                "    Mixer --> House[House mix]",
                "    Mixer --> Monitor[Monitor mix]",
                f'    Venue["{soundcheck.venue.name}"]',
            )
        )

    def _channel(self, channels: tuple[ChannelSettings, ...], text: str) -> ChannelSettings | None:
        return next((c for c in channels if text in c.label.lower() and not c.muted), None)

    def _house_score(self, channel: ChannelSettings | None, master: int) -> int:
        if channel is None or channel.muted:
            return 0
        distance_penalty = (
            0
            if channel.microphone_distance_cm is None
            else max(0, (channel.microphone_distance_cm - 15) // 15)
        )
        eq_bonus = 1 if channel.eq.mid > 1 else 0
        return max(
            0, min(10, (channel.gain + channel.fader + master) // 3 + eq_bonus - distance_penalty)
        )

    def _balance(self, score: int, low: int, high: int) -> BalanceAssessment:
        if score == 0:
            return BalanceAssessment.MUTED
        if score < low - 1:
            return BalanceAssessment.TOO_QUIET
        if score < low:
            return BalanceAssessment.SLIGHTLY_QUIET
        if score <= high:
            return BalanceAssessment.BALANCED
        if score == high + 1:
            return BalanceAssessment.SLIGHTLY_LOUD
        return BalanceAssessment.TOO_LOUD


class SoundCheckExperimentService:
    """Immutable mixer experiments for Chapter 9."""

    def change_gain(self, soundcheck: SoundCheck, channel_id: str, delta: int) -> SoundCheck:
        """Return a copy with one channel gain changed."""
        return self._replace_channel(
            soundcheck,
            channel_id,
            lambda c: replace(c, gain=max(0, min(10, c.gain + delta))),
            f"gain-{channel_id}-{delta:+d}",
        )

    def reduce_accompaniment(self, soundcheck: SoundCheck, delta: int = 1) -> SoundCheck:
        """Return a copy with non-vocal faders reduced."""
        channels = tuple(
            replace(c, fader=max(0, c.fader - delta)) if "vocal" not in c.label.lower() else c
            for c in soundcheck.mixer_settings.channels
        )
        return self._replace_settings(
            soundcheck, channels, soundcheck.mixer_settings.monitor_mix, "reduce-accompaniment"
        )

    def change_monitor(self, soundcheck: SoundCheck, delta: int) -> SoundCheck:
        """Return a copy with monitor overall level changed."""
        monitor = soundcheck.mixer_settings.monitor_mix
        changed = replace(monitor, overall_level=max(0, min(10, monitor.overall_level + delta)))
        return self._replace_settings(
            soundcheck, soundcheck.mixer_settings.channels, changed, f"monitor-{delta:+d}"
        )

    def adjust_eq(self, soundcheck: SoundCheck, channel_id: str, eq: EQProfile) -> SoundCheck:
        """Return a copy with one channel EQ profile replaced."""
        return self._replace_channel(
            soundcheck, channel_id, lambda c: replace(c, eq=eq), f"eq-{channel_id}"
        )

    def move_microphone(
        self, soundcheck: SoundCheck, channel_id: str, centimeters_delta: int
    ) -> SoundCheck:
        return self._replace_channel(
            soundcheck,
            channel_id,
            lambda c: replace(
                c,
                microphone_distance_cm=max(1, (c.microphone_distance_cm or 15) + centimeters_delta),
            ),
            f"mic-distance-{channel_id}-{centimeters_delta:+d}",
        )

    def mute_channel(self, soundcheck: SoundCheck, channel_id: str) -> SoundCheck:
        """Return a copy with one channel muted."""
        return self._replace_channel(
            soundcheck, channel_id, lambda c: replace(c, muted=True), f"mute-{channel_id}"
        )

    def _replace_channel(
        self,
        soundcheck: SoundCheck,
        channel_id: str,
        fn: Callable[[ChannelSettings], ChannelSettings],
        suffix: str,
    ) -> SoundCheck:
        channels = tuple(
            fn(c) if c.channel_id == channel_id else c for c in soundcheck.mixer_settings.channels
        )
        return self._replace_settings(
            soundcheck, channels, soundcheck.mixer_settings.monitor_mix, suffix
        )

    def _replace_settings(
        self,
        soundcheck: SoundCheck,
        channels: tuple[ChannelSettings, ...],
        monitor: MonitorMix,
        suffix: str,
    ) -> SoundCheck:
        return replace(
            soundcheck,
            identifier=f"{soundcheck.identifier}-{suffix}",
            mixer_settings=replace(
                soundcheck.mixer_settings, channels=channels, monitor_mix=monitor
            ),
        )
