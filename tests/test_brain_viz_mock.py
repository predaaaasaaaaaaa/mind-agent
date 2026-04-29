import os
import numpy as np
import pytest
from unittest.mock import patch, MagicMock

from src.brain_viz import render_brain_heatmap, render_comparison

@patch('src.brain_viz.datasets.fetch_surf_fsaverage')
@patch('src.brain_viz.plotting.plot_surf_stat_map')
@patch('src.brain_viz.plt.subplots')
@patch('src.brain_viz.plt.close')
def test_render_brain_heatmap(mock_close, mock_subplots, mock_plot_surf, mock_fetch):
    mock_fsaverage = MagicMock()
    mock_fetch.return_value = mock_fsaverage
    
    mock_fig = MagicMock()
    mock_axes = [MagicMock(), MagicMock()]
    mock_subplots.return_value = (mock_fig, mock_axes)
    
    # Let's mock savefig to actually create an empty file so the file exists check passes
    def fake_savefig(path, **kwargs):
        with open(path, 'w') as f:
            f.write("mock png")
            
    mock_fig.savefig.side_effect = fake_savefig
    
    fake_preds = np.random.randn(20, 20484)
    output_path = "mock_heatmap.png"
    
    try:
        res_path = render_brain_heatmap(fake_preds, output_path, "Test")
        assert res_path == output_path
        assert os.path.exists(output_path)
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)

@patch('src.brain_viz.datasets.fetch_surf_fsaverage')
@patch('src.brain_viz.plotting.plot_surf_stat_map')
@patch('src.brain_viz.plt.subplots')
@patch('src.brain_viz.plt.close')
def test_render_comparison(mock_close, mock_subplots, mock_plot_surf, mock_fetch):
    mock_fsaverage = MagicMock()
    mock_fetch.return_value = mock_fsaverage
    
    mock_fig = MagicMock()
    # 2x2 grid of axes
    mock_axes = np.array([[MagicMock(), MagicMock()], [MagicMock(), MagicMock()]])
    mock_subplots.return_value = (mock_fig, mock_axes)
    
    def fake_savefig(path, **kwargs):
        with open(path, 'w') as f:
            f.write("mock png")
            
    mock_fig.savefig.side_effect = fake_savefig
    
    fake_actual = np.random.randn(20, 20484)
    fake_target = np.random.randn(20, 20484)
    output_path = "mock_comparison.png"
    
    try:
        res_path = render_comparison(fake_actual, fake_target, output_path)
        assert res_path == output_path
        assert os.path.exists(output_path)
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)
