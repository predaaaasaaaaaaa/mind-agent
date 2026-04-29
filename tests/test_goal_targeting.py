import numpy as np
from unittest.mock import patch
from src.goal_targeting import compute_gap, build_targeting_report

@patch('src.goal_targeting.voxels_to_regions')
def test_compute_gap(mock_voxels_to_regions):
    mock_voxels_to_regions.return_value = {
        "amygdala": 1.0,
        "hippocampus": 0.5,
        "visual_cortex": 2.0
    }
    
    fake_preds = np.random.randn(20, 20484)
    target_regions = ["amygdala", "hippocampus"]
    
    gap = compute_gap(fake_preds, target_regions)
    
    assert isinstance(gap, dict)
    assert "amygdala" in gap
    assert "hippocampus" in gap
    
    # max activation is 2.0
    assert gap["amygdala"]["actual"] == 1.0
    assert gap["amygdala"]["delta_from_max"] == 1.0 # 2.0 - 1.0
    
    assert gap["hippocampus"]["actual"] == 0.5
    assert gap["hippocampus"]["delta_from_max"] == 1.5 # 2.0 - 0.5

@patch('src.goal_targeting.voxels_to_regions')
def test_build_targeting_report(mock_voxels_to_regions):
    mock_voxels_to_regions.return_value = {
        "amygdala": 1.0,
        "visual_cortex": 2.0
    }
    
    fake_preds = np.random.randn(20, 20484)
    target_regions = ["amygdala"]
    gap = compute_gap(fake_preds, target_regions)
    
    report = build_targeting_report(gap, "excitement")
    
    assert isinstance(report, str)
    assert "GOAL TARGETING ANALYSIS: EXCITEMENT" in report
    assert "amygdala" in report
    assert "VIDEO EDITING SUGGESTIONS:" in report
