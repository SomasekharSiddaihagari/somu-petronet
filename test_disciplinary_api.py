import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/disciplinary-master"
TEST_USER_ID = 655  # Replace with a valid user_id from your database
CREATED_BY_ID = 1 # Replace with a valid admin/user_id

def test_disciplinary_apis():
    print("🚀 Starting Disciplinary Incident API Tests...\n")

    # 1. CREATE Incident (POST)
    print("--- 1. Testing Create Incident ---")
    create_url = f"{BASE_URL}/"
    payload = {
        "user_id": TEST_USER_ID,
        "incident_date": datetime.now().isoformat(),
        "severity": "Medium",
        "incident_details": "Test incident for API validation",
        "investigation_finding": "Ongoing investigation",
        "measures_taken": "Warning issued",
        "enable_suspension": "false",
        "enable_termination": "false",
        "outcome": "Pending final review",
        "created_by": CREATED_BY_ID
    }
    
    # Using data= for Form data as per router implementation
    response = requests.post(create_url, data=payload)
    print(f"Status: {response.status_code}")
    
    try:
        res_json = response.json()
        print(f"Response: {res_json}")
    except:
        print(f"Response: {response.text}")

    if response.status_code != 200:
        print("❌ Create failed. Stopping tests.")
        return

    incident_id = response.json().get("id")

    # 2. GET ALL Incidents (GET)
    print("\n--- 2. Testing Get All Incidents ---")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Total Incidents: {response.json().get('total')}")

    # 3. GET Incident BY ID (GET)
    print(f"\n--- 3. Testing Get Incident by ID: {incident_id} ---")
    response = requests.get(f"{BASE_URL}/{incident_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Details: {response.json().get('incident_details')}")

    # 4. GET by User ID (GET)
    print(f"\n--- 4. Testing Get by User ID: {TEST_USER_ID} ---")
    response = requests.get(f"{BASE_URL}/get-by-user-disciplinary/{TEST_USER_ID}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Count for User: {len(response.json())}")

    # 5. ACKNOWLEDGE Incident (PUT)
    print(f"\n--- 5. Testing Acknowledge Incident: {incident_id} ---")
    ack_url = f"{BASE_URL}/acknowledge-disciplinary/{incident_id}/{TEST_USER_ID}"
    ack_payload = {
        "acknowledgement": True,
        "comments": "Acknowledged via API test script"
    }
    response = requests.put(ack_url, json=ack_payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # 6. EMPLOYEE ACTIVITY FILTER (POST)
    print(f"\n--- 6. Testing Employee Activity Filter ---")
    filter_url = f"{BASE_URL}/employee-activity-filter-disciplinary/{TEST_USER_ID}"
    filter_payload = {
        "search": "",
        "skip": 0,
        "limit": 10
    }
    response = requests.post(filter_url, json=filter_payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Filter Results Found: {len(response.json())}")

    # 7. DELETE Incident (DELETE)
    print(f"\n--- 7. Testing Delete Incident: {incident_id} ---")
    response = requests.delete(f"{BASE_URL}/{incident_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    print("\n✅ API Testing Completed.")

if __name__ == "__main__":
    test_disciplinary_apis()
