import pytest
import requests

def test_get_locations_for_us_90210_check_status_code_equals_200():
     response = requests.get("http://127.0.0.1:5000/api")
     assert response.status_code == 200