import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
	response = client.get("/activities")
	assert response.status_code == 200
	data = response.json()
	assert "Chess Club" in data
	assert "Programming Class" in data


import urllib.parse

def test_signup_for_activity():
	email = "newstudent@mergington.edu"
	activity = "Chess Club"
	encoded_activity = urllib.parse.quote(activity)
	# Ensure not already signed up
	client.post(f"/activities/{encoded_activity}/unregister?email={email}")
	response = client.post(f"/activities/{encoded_activity}/signup?email={email}")
	assert f"Signed up {email} for {activity}" in response.json()["message"]
	# Try signing up again (should fail)
	response2 = client.post(f"/activities/{encoded_activity}/signup?email={email}")
	assert response2.status_code == 400
	assert "already signed up" in response2.json()["detail"]


