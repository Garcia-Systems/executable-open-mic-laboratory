from open_mic_lab.cli import main


def test_recovery_incidents_cli(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["recovery", "incidents"]) == 0
    assert "forgotten-lyrics" in capsys.readouterr().out


def test_recovery_analyze_cli(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["recovery", "analyze"]) == 0
    assert "Incident: forgotten lyrics" in capsys.readouterr().out


def test_recovery_experiment_cli(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["recovery", "experiment", "restart"]) == 0
    assert "Experiment strategy: restart section" in capsys.readouterr().out


def test_chapter_eleven_demo_cli(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["chapter-eleven-demo"]) == 0
    assert "Chapter 11" in capsys.readouterr().out
