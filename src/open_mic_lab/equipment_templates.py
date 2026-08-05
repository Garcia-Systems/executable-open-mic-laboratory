"""Deterministic educational equipment templates for Chapter 8."""

from open_mic_lab.domain.equipment import (
    Cable,
    Connection,
    NodeRole,
    OutputRole,
    PowerRequirement,
    SignalNode,
    SignalPath,
    SignalPort,
    SignalType,
)


def _port(name: str, signal: SignalType) -> SignalPort:
    return SignalPort(name, signal)


def _node(
    identifier: str,
    label: str,
    role: NodeRole,
    ins: tuple[SignalType, ...],
    outs: tuple[SignalType, ...],
    output_role: OutputRole = OutputRole.INTERNAL,
    power: PowerRequirement = PowerRequirement.NONE,
) -> SignalNode:
    return SignalNode(
        identifier,
        label,
        role,
        tuple(_port(f"in-{i + 1}", s) for i, s in enumerate(ins)),
        tuple(_port(f"out-{i + 1}", s) for i, s in enumerate(outs)),
        power,
        (f"{label} teaches the role of {role.value}.",),
        output_role,
    )


def piano_and_vocal_setup() -> SignalPath:
    """Return the Chapter 8 demonstration setup."""
    vocal = _node("vocal-mic", "Vocal Microphone", NodeRole.MICROPHONE, (), (SignalType.MIC_LEVEL,))
    piano = _node(
        "digital-piano",
        "Digital Piano Outputs",
        NodeRole.INSTRUMENT_OUTPUT,
        (),
        (SignalType.LINE_LEVEL,),
    )
    mixer = _node(
        "mixer",
        "Small Mixer",
        NodeRole.MIXER_CHANNEL,
        (SignalType.MIC_LEVEL, SignalType.LINE_LEVEL),
        (SignalType.LINE_LEVEL, SignalType.LINE_LEVEL),
        power=PowerRequirement.AC_POWER,
    )
    monitor = _node(
        "monitor",
        "Performer Monitor",
        NodeRole.MONITOR_MIX,
        (SignalType.LINE_LEVEL,),
        (),
        OutputRole.PERFORMER,
        PowerRequirement.AC_POWER,
    )
    mains = _node(
        "mains",
        "Main Speakers",
        NodeRole.SPEAKER_SYSTEM,
        (SignalType.LINE_LEVEL,),
        (),
        OutputRole.AUDIENCE,
        PowerRequirement.AC_POWER,
    )
    mic_cable = Cable("xlr", "XLR cable", SignalType.MIC_LEVEL)
    line_cable = Cable("trs", "Balanced line cable", SignalType.LINE_LEVEL)
    return SignalPath(
        "piano-and-vocal",
        "Piano and Vocal",
        (vocal, piano, mixer, monitor, mains),
        (
            Connection("vocal-to-mixer", "vocal-mic", "out-1", "mixer", "in-1", mic_cable),
            Connection("piano-to-mixer", "digital-piano", "out-1", "mixer", "in-2", line_cable),
            Connection("mixer-to-monitor", "mixer", "out-1", "monitor", "in-1", line_cable),
            Connection("mixer-to-mains", "mixer", "out-2", "mains", "in-1", line_cable),
        ),
        ("A mixer creates separate audience and performer destinations.",),
    )


def solo_acoustic_guitar_setup() -> SignalPath:
    guitar = _node(
        "guitar",
        "Acoustic Guitar Pickup",
        NodeRole.PICKUP,
        (),
        (SignalType.INSTRUMENT_LEVEL,),
        power=PowerRequirement.BATTERY,
    )
    di = _node(
        "di", "DI Box", NodeRole.DI_BOX, (SignalType.INSTRUMENT_LEVEL,), (SignalType.MIC_LEVEL,)
    )
    mixer = _node(
        "mixer",
        "Mixer Channel",
        NodeRole.MIXER_CHANNEL,
        (SignalType.MIC_LEVEL,),
        (SignalType.LINE_LEVEL,),
        power=PowerRequirement.AC_POWER,
    )
    mains = _node(
        "mains",
        "Powered Speaker",
        NodeRole.SPEAKER_SYSTEM,
        (SignalType.LINE_LEVEL,),
        (),
        OutputRole.AUDIENCE,
        PowerRequirement.AC_POWER,
    )
    return SignalPath(
        "solo-acoustic-guitar",
        "Solo Acoustic Guitar",
        (guitar, di, mixer, mains),
        (
            Connection(
                "guitar-to-di",
                "guitar",
                "out-1",
                "di",
                "in-1",
                Cable("instrument", "Instrument cable", SignalType.INSTRUMENT_LEVEL),
            ),
            Connection(
                "di-to-mixer",
                "di",
                "out-1",
                "mixer",
                "in-1",
                Cable("xlr", "XLR cable", SignalType.MIC_LEVEL),
            ),
            Connection(
                "mixer-to-mains",
                "mixer",
                "out-1",
                "mains",
                "in-1",
                Cable("line", "Line cable", SignalType.LINE_LEVEL),
            ),
        ),
        (),
    )


def equipment_templates() -> dict[str, SignalPath]:
    """Return reusable educational templates."""
    base = piano_and_vocal_setup()
    return {
        "solo-acoustic-guitar": solo_acoustic_guitar_setup(),
        "solo-digital-piano": SignalPath(
            "solo-digital-piano",
            "Solo Digital Piano",
            base.nodes[1:],
            base.connections[1:],
            ("Digital piano begins at line level.",),
        ),
        "piano-and-vocal": base,
        "guitar-and-vocal": SignalPath(
            "guitar-and-vocal",
            "Guitar and Vocal",
            solo_acoustic_guitar_setup().nodes + (base.nodes[0],),
            solo_acoustic_guitar_setup().connections,
            ("Add a microphone as a second source.",),
        ),
        "small-duo": base,
        "church-service": base,
        "coffeehouse": solo_acoustic_guitar_setup(),
        "open-mic": base,
        "simple-band": base,
    }
