import numpy as np
from unittest.mock import patch
from src.report_builder import build_analysis_report

@patch('src.report_builder.voxels_to_regions')
@patch('src.report_builder.top_k_regions')
def test_build_analysis_report(mock_top_k, mock_voxels_to_regions):
    mock_voxels_to_regions.return_value = {"amygdala": 1.5, "hippocampus": 1.2}
    mock_top_k.return_value = [("amygdala", 1.5), ("hippocampus", 1.2)]
    
    fake_preds = np.random.randn(20, 20484)
    report = build_analysis_report(fake_preds, top_k=2)
    
    assert isinstance(report, str)
    assert "BRAIN ACTIVATION ANALYSIS" in report
    assert "amygdala" in report
    assert "hippocampus" in report
    assert "Interpretation:" in report
    assert "High emotional arousal" in report # part of amygdala hint
