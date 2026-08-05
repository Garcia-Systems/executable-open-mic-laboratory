from open_mic_lab.cli import main
from open_mic_lab.debug_labs.chapter_02_repertoire_engineering import main as debug_main
from open_mic_lab.sample_data import build_sample_repertoire
from open_mic_lab.services.repertoire_service import RepertoireEngineeringService


def test_repertoire_analysis_observations_and_distributions() -> None:
    rep = build_sample_repertoire()
    analysis = RepertoireEngineeringService().analyze(rep)
    assert analysis.genre_distribution["pop"] == 2
    assert analysis.key_distribution["E"] == 3
    assert analysis.diversity_score > 50
    assert any("Diversity score" in obs for obs in analysis.observations)


def test_gap_priority_health_and_report_are_deterministic() -> None:
    rep = build_sample_repertoire()
    service = RepertoireEngineeringService()
    assert service.gaps(rep) == service.gaps(rep)
    priorities = service.priorities(rep)
    assert priorities[0].score >= priorities[-1].score
    assert priorities[0].reasons
    health = service.health(rep)
    assert 0 <= health.score <= 100
    assert "Educational comparison" in health.explanation
    report = service.text_report("Genre Distribution", service.analyze(rep).genre_distribution)
    assert "Genre Distribution" in report
    assert "##" in report


def test_repertoire_cli_commands_and_chapter_two_demo(capsys) -> None:  # type: ignore[no-untyped-def]
    for command in ("summary", "gaps", "health", "priorities", "neglected", "diversity"):
        assert main(["repertoire", command]) == 0
        assert capsys.readouterr().out
    assert main(["chapter-two-demo"]) == 0
    assert "Chapter 2" in capsys.readouterr().out


def test_chapter_two_debug_helper(capsys) -> None:  # type: ignore[no-untyped-def]
    assert debug_main() == 0
    assert "debug lab" in capsys.readouterr().out
