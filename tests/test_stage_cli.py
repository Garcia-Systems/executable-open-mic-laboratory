from open_mic_lab.cli import main


def test_stage_cli_commands(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["stage", "analyze"]) == 0
    assert "chapter-seven-baseline" in capsys.readouterr().out
    assert main(["stage", "flow"]) == 0
    assert "Flow:" in capsys.readouterr().out
    assert main(["stage", "introductions"]) == 0
    assert "Introduction:" in capsys.readouterr().out
    assert main(["stage", "experiment", "shorten"]) == 0
    assert "Original object unchanged: True" in capsys.readouterr().out
    assert main(["stage", "experiment", "story"]) == 0
    assert "Experiment:" in capsys.readouterr().out
    assert main(["stage", "compare"]) == 0
    assert "Difference:" in capsys.readouterr().out


def test_chapter_seven_demo(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["chapter-seven-demo"]) == 0
    output = capsys.readouterr().out
    assert "Chapter 7" in output
    assert "Reflection:" in output
