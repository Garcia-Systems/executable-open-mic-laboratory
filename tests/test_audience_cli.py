from open_mic_lab.cli import main


def test_audience_profiles_cli(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["audience", "profiles"]) == 0
    assert "supportive-coffeehouse" in capsys.readouterr().out


def test_audience_analyze_cli(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["audience", "analyze"]) == 0
    output = capsys.readouterr().out
    assert "Audience Experience Summary" in output
    assert "Suggested Experiments" in output


def test_audience_experiment_cli(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["audience", "experiment", "participation"]) == 0
    output = capsys.readouterr().out
    assert "Experiment: increase audience interaction" in output
    assert "Original object unchanged: True" in output


def test_chapter_ten_demo_cli(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["chapter-ten-demo"]) == 0
    assert "Chapter 10 — Audience Experience Laboratory" in capsys.readouterr().out
