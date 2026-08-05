"""Small pitch and vocal-range value objects for Chapter 1."""

import re
from dataclasses import dataclass

_NOTE_RE = re.compile(r"^([A-Ga-g])([#b]?)(-?\d+)$")
_SEMITONES = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
_SHARP_NAMES = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")


@dataclass(frozen=True, order=True, slots=True)
class VocalNote:
    """A deterministic note spelling mapped to MIDI-like pitch order.

    Enharmonic spellings compare by pitch number, so ``Bb4`` and ``A#4`` are equal for
    suitability calculations even though the original spelling is preserved for display.
    """

    pitch_number: int
    spelling: str

    @classmethod
    def parse(cls, value: str) -> "VocalNote":
        """Parse notes such as C3, F#3, or Bb4."""
        match = _NOTE_RE.match(value.strip())
        if not match:
            raise ValueError(f"Invalid note '{value}'. Use forms such as C3, F#3, or Bb4.")
        letter, accidental, octave_text = match.groups()
        octave = int(octave_text)
        if octave < 0 or octave > 8:
            raise ValueError("Octave must be between 0 and 8 for this lightweight model.")
        semitone = _SEMITONES[letter.upper()]
        if accidental == "#":
            semitone += 1
        elif accidental == "b":
            semitone -= 1
        pitch_number = (octave + 1) * 12 + semitone
        return cls(pitch_number=pitch_number, spelling=f"{letter.upper()}{accidental}{octave}")

    def transpose(self, semitones: int) -> "VocalNote":
        """Return this note shifted by semitones, displayed with sharp spellings."""
        new_pitch = self.pitch_number + semitones
        if new_pitch < 12 or new_pitch > 119:
            raise ValueError("Transposed note is outside the supported octave range 0-8.")
        octave = (new_pitch // 12) - 1
        name = _SHARP_NAMES[new_pitch % 12]
        return VocalNote(new_pitch, f"{name}{octave}")

    def __str__(self) -> str:
        return self.spelling


@dataclass(frozen=True, slots=True)
class VocalRange:
    """Lowest and highest notes required or comfortably available."""

    low: VocalNote
    high: VocalNote

    @classmethod
    def from_strings(cls, low: str, high: str) -> "VocalRange":
        """Build a range from note strings."""
        return cls(VocalNote.parse(low), VocalNote.parse(high))

    def __post_init__(self) -> None:
        if self.low.pitch_number > self.high.pitch_number:
            raise ValueError("Vocal range low note must not be higher than high note.")

    def contains(self, other: "VocalRange") -> bool:
        """Return whether this range fully contains another range."""
        return (
            self.low.pitch_number <= other.low.pitch_number
            and other.high.pitch_number <= self.high.pitch_number
        )

    def outside_distance(self, other: "VocalRange") -> int:
        """Return total semitones by which another range extends outside this range."""
        below = max(0, self.low.pitch_number - other.low.pitch_number)
        above = max(0, other.high.pitch_number - self.high.pitch_number)
        return below + above

    def transpose(self, semitones: int) -> "VocalRange":
        """Return a shifted copy of this range."""
        return VocalRange(self.low.transpose(semitones), self.high.transpose(semitones))

    def __str__(self) -> str:
        return f"{self.low}-{self.high}"
