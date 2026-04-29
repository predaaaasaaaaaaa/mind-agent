import pytest
from src.goal_mapping import map_goal_to_regions, available_goals

def test_available_goals():
    goals = available_goals()
    assert isinstance(goals, list)
    assert len(goals) > 0
    assert "excitement" in goals

def test_map_goal_to_regions_success():
    regions = map_goal_to_regions("I want them to feel excitement")
    assert isinstance(regions, list)
    assert len(regions) > 0
    assert "amygdala" in regions

def test_map_goal_to_regions_failure():
    regions = map_goal_to_regions("This is a completely unknown and random goal")
    assert isinstance(regions, list)
    assert len(regions) == 0
