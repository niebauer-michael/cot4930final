import pytest
from unittest import mock
from main import access_secret  # Import the function you're testing

# Fixture to mock the access_secret_version method from SecretManagerServiceClient
@pytest.fixture
def mock_access_secret_version_success():
    with mock.patch('google.cloud.secretmanager.SecretManagerServiceClient.access_secret_version') as mock_access_secret_version:
        # Simulate a successful response from Secret Manager with a mock secret value
        mock_access_secret_version.return_value.payload.data = b'mocked_secret_value'
        yield mock_access_secret_version

def test_access_secret_success(mock_access_secret_version_success):
    # Call the access_secret function directly
    secret = access_secret("API_KEY")
    
    # Assert that the secret returned matches the mocked value
    assert secret == 'mocked_secret_value'
    mock_access_secret_version_success.assert_called_once()  # Ensure the mock was called


# Test case for retry error (e.g., timeout while accessing Secret Manager)
@pytest.fixture
def mock_access_secret_version_retry_error():
    with mock.patch('google.cloud.secretmanager.SecretManagerServiceClient.access_secret_version') as mock_access_secret_version:
        # Simulate a retry error or timeout
        mock_access_secret_version.side_effect = Exception("RetryError: Timeout exceeded")
        yield mock_access_secret_version

def test_access_secret_retry_error(mock_access_secret_version_retry_error):
    # Call the function and expect an exception
    with pytest.raises(Exception, match="RetryError: Timeout exceeded"):
        access_secret("API_KEY")

# Test case for metadata service error (e.g., service unavailable)
@pytest.fixture

def mock_access_secret_version_metadata_error():
    with mock.patch('google.cloud.secretmanager.SecretManagerServiceClient.access_secret_version') as mock_access_secret_version:
        # Simulate an error when accessing metadata service
        mock_access_secret_version.side_effect = Exception("Metadata service unavailable")
        yield mock_access_secret_version


def test_access_secret_metadata_error(mock_access_secret_version_metadata_error):
    # Call the function and expect an exception
    with pytest.raises(Exception, match="Metadata service unavailable"):
        access_secret("API_KEY")
