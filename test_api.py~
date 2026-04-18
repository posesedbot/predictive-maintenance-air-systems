# test_api.py
import requests
import pytest
import subprocess
import time

# Define the server URL and the prediction endpoint
BASE_URL = "http://127.0.0.1:8000"
PREDICT_URL = f"{BASE_URL}/predict"

# Sample payload that should trigger a FAILURE (Heuristic: Run Hours > 1500 AND Vibration > 2.0)
FAILURE_PAYLOAD = {
  "run_hours": 2000,
  "temp_avg": 90.0,
  "pressure_avg": 6.0,
  "vibration": 2.5
}

# Sample payload that should trigger a SUCCESS (No Failure)
SUCCESS_PAYLOAD = {
  "run_hours": 800,
  "temp_avg": 85.0,
  "pressure_avg": 5.0,
  "vibration": 1.5
}

# --- Fixture to Manage the Server Lifecycle ---
@pytest.fixture(scope="module")
def api_server():
    """Starts the FastAPI server as a background process for testing."""
    # Command to run your FastAPI app using uvicorn
    cmd = ["uvicorn", "api.fastapi_app:app", "--host", "127.0.0.1", "--port", "8000"]
    
    # Start the server in a new process
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait a few seconds for the server to start up
    time.sleep(5)
    
    # Yield the process object to the test function
    yield proc
    
    # --- Teardown: Stop the server after tests are done ---
    proc.terminate()
    proc.wait()


# --- Test Functions ---

def test_api_is_running(api_server):
    """Tests if the root endpoint returns a status code 200."""
    response = requests.get(BASE_URL + "/")
    assert response.status_code == 200
    assert response.json()["status"] == "Boiler Maintenance API is running."

def test_prediction_failure_scenario(api_server):
    """Tests the critical FAILURE path using the heuristic rule."""
    response = requests.post(PREDICT_URL, json=FAILURE_PAYLOAD)
    data = response.json()
    
    assert response.status_code == 200
    assert data["prediction"] == 1
    assert "SHUTDOWN & INSPECTION" in data["action_required"]

def test_prediction_success_scenario(api_server):
    """Tests the SUCCESS path using the heuristic rule."""
    response = requests.post(PREDICT_URL, json=SUCCESS_PAYLOAD)
    data = response.json()
    
    assert response.status_code == 200
    assert data["prediction"] == 0
    assert "STATUS OK" in data["action_required"]