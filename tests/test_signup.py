"""Backend tests for activity signup (AAA pattern)."""
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_duplicate_signup_rejected():
    # Arrange: use the Chess Club roster
    email = activities["Chess Club"]["participants"][0]
    # Act: sign up the same student again
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    # Assert: rejected as a conflict
    assert response.status_code == 409


def test_unregister_and_resignup():
    # Arrange
    email = "newstudent@mergington.edu"
    # Act: sign up, unregister, sign up again
    assert client.post(f"/activities/Drama Club/signup?email={email}").status_code == 200
    assert client.delete(f"/activities/Drama Club/signup?email={email}").status_code == 200
    response = client.post(f"/activities/Drama Club/signup?email={email}")
    # Assert
    assert response.status_code == 200
