"""Equipment and signal-flow domain models for Chapter 8."""

from dataclasses import dataclass
from enum import Enum

from open_mic_lab.domain.validation import require_text


class SignalType(Enum):
    """Conceptual signal levels used in live-performance systems."""

    ACOUSTIC = "acoustic"
    MIC_LEVEL = "mic level"
    INSTRUMENT_LEVEL = "instrument level"
    LINE_LEVEL = "line level"
    SPEAKER_LEVEL = "speaker level"
    HEADPHONE_LEVEL = "headphone level"
    DIGITAL = "digital"


class PowerRequirement(Enum):
    """Power needs for equipment nodes."""

    NONE = "none"
    PHANTOM_POWER = "phantom power"
    BATTERY = "battery"
    AC_POWER = "AC power"
    BUS_POWER = "bus power"


class NodeRole(Enum):
    """Educational role of a signal node."""

    AUDIO_SOURCE = "audio source"
    MICROPHONE = "microphone"
    PICKUP = "pickup"
    INSTRUMENT_OUTPUT = "instrument output"
    EFFECTS_PROCESSOR = "effects processor"
    DI_BOX = "DI box"
    MIXER_CHANNEL = "mixer channel"
    MONITOR_MIX = "monitor mix"
    SPEAKER_SYSTEM = "speaker system"
    CABLE = "cable"


class OutputRole(Enum):
    """Destination role for an output heard by a listener."""

    PERFORMER = "performer"
    AUDIENCE = "audience"
    INTERNAL = "internal"


@dataclass(frozen=True, slots=True)
class SignalPort:
    """Input or output jack with a conceptual signal type."""

    identifier: str
    signal_type: SignalType
    note: str = ""

    def __post_init__(self) -> None:
        require_text(self.identifier, "Signal port identifier")


@dataclass(frozen=True, slots=True)
class SignalNode:
    """Reusable equipment node in a signal graph."""

    identifier: str
    label: str
    role: NodeRole
    inputs: tuple[SignalPort, ...]
    outputs: tuple[SignalPort, ...]
    power: PowerRequirement = PowerRequirement.NONE
    educational_notes: tuple[str, ...] = ()
    output_role: OutputRole = OutputRole.INTERNAL

    def __post_init__(self) -> None:
        require_text(self.identifier, "Signal node identifier")
        require_text(self.label, "Signal node label")
        if not self.inputs and not self.outputs:
            raise ValueError("Signal node requires at least one input or output.")


@dataclass(frozen=True, slots=True)
class Cable:
    """A cable concept that joins one output to one input."""

    identifier: str
    label: str
    signal_type: SignalType
    educational_notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require_text(self.identifier, "Cable identifier")
        require_text(self.label, "Cable label")


@dataclass(frozen=True, slots=True)
class Connection:
    """Directed connection from a source node output to a destination node input."""

    identifier: str
    source_node: str
    source_output: str
    destination_node: str
    destination_input: str
    cable: Cable

    def __post_init__(self) -> None:
        require_text(self.identifier, "Connection identifier")
        require_text(self.source_node, "Connection source node")
        require_text(self.source_output, "Connection source output")
        require_text(self.destination_node, "Connection destination node")
        require_text(self.destination_input, "Connection destination input")


@dataclass(frozen=True, slots=True)
class SignalPath:
    """A complete connected equipment configuration."""

    identifier: str
    name: str
    nodes: tuple[SignalNode, ...]
    connections: tuple[Connection, ...]
    educational_notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require_text(self.identifier, "Signal path identifier")
        require_text(self.name, "Signal path name")
        if len({node.identifier for node in self.nodes}) != len(self.nodes):
            raise ValueError("Signal path nodes must have unique identifiers.")
        if len({connection.identifier for connection in self.connections}) != len(self.connections):
            raise ValueError("Signal path connections must have unique identifiers.")


# Concept aliases keep Chapter 8 vocabulary visible without product-specific subclasses.
AudioSource = SignalNode
Microphone = SignalNode
Pickup = SignalNode
InstrumentOutput = SignalNode
MixerChannel = SignalNode
MonitorMix = SignalNode
SpeakerSystem = SignalNode
EffectsProcessor = SignalNode
