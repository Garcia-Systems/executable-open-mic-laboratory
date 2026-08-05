from open_mic_lab.cli import main


def test_cli_repertoire_list(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["repertoire", "list"]) == 0
    assert "River Road at Dusk" in capsys.readouterr().out


def test_cli_readiness_show(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["readiness", "show", "train-guitar-closer"]) == 0
    output = capsys.readouterr().out
    assert "Readiness for train-guitar-closer" in output
    assert "performance ready" in output


def test_cli_setlist_analyze(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["setlist", "analyze"]) == 0
    assert "Estimated duration" in capsys.readouterr().out


def test_cli_song_scenarios(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["songs", "scenarios"]) == 0
    assert "coffeehouse" in capsys.readouterr().out


def test_cli_song_evaluate_compare_explain_and_demo(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["songs", "evaluate", "harbor-guitar", "--scenario", "coffeehouse"]) == 0
    assert "Suitability" in capsys.readouterr().out
    assert main(["songs", "compare", "--scenario", "coffeehouse"]) == 0
    assert "Observation" in capsys.readouterr().out
    assert (
        main(
            [
                "songs",
                "explain",
                "window-guitar-original-feature",
                "--scenario",
                "first-performance",
            ]
        )
        == 0
    )
    assert "Explanation" in capsys.readouterr().out
    assert main(["chapter-one-demo"]) == 0
    assert "Chapter 1" in capsys.readouterr().out


def test_cli_song_invalid_inputs() -> None:  # type: ignore[no-untyped-def]
    import pytest

    with pytest.raises(SystemExit):
        main(["songs", "evaluate", "missing", "--scenario", "coffeehouse"])
    with pytest.raises(SystemExit):
        main(["songs", "compare", "--scenario", "missing"])
