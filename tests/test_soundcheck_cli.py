from open_mic_lab.cli import main


def test_soundcheck_analyze_cli(capsys):
    assert main(["soundcheck", "analyze"]) == 0
    assert "House Mix" in capsys.readouterr().out


def test_soundcheck_workflow_cli(capsys):
    assert main(["soundcheck", "workflow"]) == 0
    assert "verify signal path" in capsys.readouterr().out


def test_soundcheck_experiment_cli(capsys):
    assert main(["soundcheck", "experiment", "monitor", "2"]) == 0
    assert "Original object unchanged: True" in capsys.readouterr().out


def test_chapter_nine_demo_cli(capsys):
    assert main(["chapter-nine-demo"]) == 0
    out = capsys.readouterr().out
    assert "Chapter 9" in out
    assert "Immutable experiment" in out
