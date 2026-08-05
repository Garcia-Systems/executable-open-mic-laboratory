from open_mic_lab.cli import main


def test_analytics_dashboard_cli(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["analytics", "dashboard"]) == 0
    output = capsys.readouterr().out
    assert "Performance Dashboard" in output
    assert "Readiness" in output


def test_chapter_fifteen_demo_cli(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["chapter-fifteen-demo"]) == 0
    output = capsys.readouterr().out
    assert "Volume I summary" in output
    assert "Immutable planning experiments" in output
