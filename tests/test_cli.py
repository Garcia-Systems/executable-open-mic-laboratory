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
