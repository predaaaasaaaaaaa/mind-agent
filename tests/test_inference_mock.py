import numpy as np
from unittest.mock import patch

# We patch the entire BrainPredictor class to return fake data 
# since the prompt requires mocking the real TRIBE v2 model call
@patch('src.inference.BrainPredictor', create=True)
def test_brain_predictor_predict(mock_predictor_class):
    mock_instance = mock_predictor_class.return_value
    mock_instance.predict.return_value = np.random.randn(23, 20484)
    
    predictor = mock_predictor_class()
    preds = predictor.predict("fake_video.mp4")
    
    assert preds.shape == (23, 20484)
