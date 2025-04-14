import pytest
#import random
#import string
#from main import randomNameGenerator  # Import the function from main.py
from unittest import mock
from google.cloud import storage
from main import getBucket

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