import numpy as np
import pytest
from unittest.mock import patch

from src.region_mapping import voxels_to_regions, top_k_regions

@patch('src.region_mapping.load_atlas')
def test_voxels_to_regions(mock_load_atlas):
    # Mock the atlas
    mock_left = np.zeros(10242, dtype=int)
    mock_left[:5000] = 1 # Region 1
    mock_right = np.zeros(10242, dtype=int)
    mock_right[:5000] = 2 # Region 2
    
    mock_load_atlas.return_value = {
        'map_left': mock_left,
        'map_right': mock_right,
        'labels': [b'Unknown', b'Region1', b'Region2']
    }
    
    fake_preds = np.random.randn(20, 20484)
    activations = voxels_to_regions(fake_preds)
    
    assert isinstance(activations, dict)
    assert len(activations) > 0
    assert 'Region1' in activations
    assert 'Region2' in activations
    assert 'Unknown' not in activations
    
def test_top_k_regions():
    activations = {'A': 1.0, 'B': 2.0, 'C': 0.5, 'D': 3.0}
    top = top_k_regions(activations, k=2)
    assert len(top) == 2
    assert top[0][0] == 'D'
    assert top[1][0] == 'B'
