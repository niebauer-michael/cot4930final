import pytest
import random
import string
from main import randomNameGenerator  # Import the function from main.py
from unittest import mock
from google.cloud import storage
from main import getBucket

# Test function
def test_randomNameGenerator(monkeypatch):
    # Mocking random.choices to return a controlled result
    mock_random_choices = ['a', 'B', '3', '9', 'z', 'X']  # Example controlled output
    monkeypatch.setattr(random, 'choices', lambda *args, **kwargs: mock_random_choices)

    result = randomNameGenerator()
    
    # Assert that the result is a string of length 6
    assert len(result) == 6
    # Assert that the result matches the mocked output
    assert result == 'aB39zX'


#from main import app

#def test_value_is_one():
#    value = 1
#    assert value == 1  # This will pass if value is 1, and fail otherwise

def test_getBucket():
    # Mock the storage.Client
    mock_storage_client = mock.Mock()
    
    # Mock the bucket method of the storage client
    mock_bucket = mock.Mock()
    mock_storage_client.bucket.return_value = mock_bucket
    
    # Replace storage.Client with our mock
    with mock.patch.object(storage, 'Client', return_value=mock_storage_client):
        result = getBucket()
        
        # Assert that the return value is the mocked bucket
        assert result == mock_bucket
        
        # Assert that storage.Client was called once
        mock_storage_client.bucket.assert_called_once_with('cot4930private')