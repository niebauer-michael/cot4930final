import pytest
import random
import string
from main import randomNameGenerator  # Import the function from main.py

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
