"""Smoke tests for ClariPulse™ foundation imports."""


def test_core_imports():
    from components.ui import hero
    from src.data.sample_data import model_leaderboard
    assert callable(hero)
    assert not model_leaderboard().empty
