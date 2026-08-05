"""Educational arrangement experiments that copy performance versions."""

from dataclasses import replace
from decimal import Decimal

from open_mic_lab.domain import Difficulty, EnergyLevel, PerformanceVersion
from open_mic_lab.domain.pitch import VocalNote

_DIFFICULTY_DOWN = {
    Difficulty.CHALLENGING: Difficulty.MODERATE,
    Difficulty.MODERATE: Difficulty.SIMPLE,
    Difficulty.SIMPLE: Difficulty.SIMPLE,
}
_ENERGY_DOWN = {
    EnergyLevel.VERY_HIGH: EnergyLevel.HIGH,
    EnergyLevel.HIGH: EnergyLevel.MEDIUM,
    EnergyLevel.MEDIUM: EnergyLevel.MEDIUM,
    EnergyLevel.LOW: EnergyLevel.LOW,
    EnergyLevel.VERY_LOW: EnergyLevel.VERY_LOW,
}


class PerformanceVersionExperimentService:
    """Create proposed copies for key and arrangement experiments."""

    def transpose(
        self, version: PerformanceVersion, destination_key: str, semitones: int
    ) -> PerformanceVersion:
        """Copy a version into another key and shift required vocal range by semitones.

        This lightweight model validates the destination key as a note name and shifts the
        range only; real arrangements may include instrument-specific or harmonic issues.
        """
        VocalNote.parse(f"{destination_key}4")
        shifted = (
            version.required_vocal_range.transpose(semitones)
            if version.required_vocal_range
            else None
        )
        key_slug = destination_key.lower().replace("#", "sharp").replace("b", "flat")
        return replace(
            version,
            identifier=f"{version.identifier}-transpose-{key_slug}",
            performance_key=destination_key,
            required_vocal_range=shifted,
            adaptation_notes=version.adaptation_notes
            + (
                "Educational transposition experiment: "
                f"{semitones:+} semitones to {destination_key}.",
            ),
        )

    def simplify(self, version: PerformanceVersion) -> PerformanceVersion:
        """Copy a version with bounded educational simplification assumptions."""
        stability = min(Decimal("10"), version.accompaniment_stability + Decimal("1.0"))
        return replace(
            version,
            identifier=f"{version.identifier}-simplified",
            arrangement_difficulty=_DIFFICULTY_DOWN[version.arrangement_difficulty],
            accompaniment_stability=stability,
            energy_level=_ENERGY_DOWN[version.energy_level],
            adaptation_notes=version.adaptation_notes
            + (
                "Educational simplification: easier pattern, projected +1 accompaniment "
                "stability, possible energy reduction.",
            ),
        )
