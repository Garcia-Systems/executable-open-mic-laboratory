from open_mic_lab.cli import main


def test_arrangement_cli_commands_and_demo(capsys) -> None:  # type: ignore[no-untyped-def]
    commands = [
        ["arrangement", "list"],
        ["arrangement", "compare"],
        ["arrangement", "analyze"],
        ["arrangement", "history"],
        ["arrangement", "experiment", "transpose", "window-piano-arrangement", "G", "-2"],
        ["arrangement", "experiment", "simplify", "window-piano-arrangement"],
        ["arrangement", "experiment", "tempo", "window-piano-arrangement", "64"],
        ["arrangement", "experiment", "groove", "window-piano-arrangement", "coffeehouse"],
        ["chapter-four-demo"],
    ]
    for command in commands:
        assert main(command) == 0
    output = capsys.readouterr().out
    assert "Chapter 4" in output
    assert "Original object unchanged: True" in output
