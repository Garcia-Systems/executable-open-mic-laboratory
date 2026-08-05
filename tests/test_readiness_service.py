from decimal import Decimal

from open_mic_lab.sample_data import build_sample_repertoire, sample_practice_sessions
from open_mic_lab.services.readiness_service import calculate_readiness


def test_readiness_is_deterministic() -> None:
    rep = build_sample_repertoire()
    result = calculate_readiness(
        rep.get_version("river-guitar-lowered"), sample_practice_sessions()
    )
    assert result.score == Decimal("79.9")
    assert result.category == "nearly ready"
    assert result == calculate_readiness(
        rep.get_version("river-guitar-lowered"), sample_practice_sessions()
    )


def test_readiness_categories_and_boundaries() -> None:
    rep = build_sample_repertoire()
    low = calculate_readiness(rep.get_version("lantern-piano"))
    high = calculate_readiness(rep.get_version("train-guitar-closer"), sample_practice_sessions())
    assert Decimal("0") <= low.score <= Decimal("100")
    assert low.category == "developing"
    assert high.category == "performance ready"
    assert high.score <= Decimal("100")
