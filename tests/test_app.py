import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

class TestActivitiesAPI:
    """Test suite for the Mergington High School Activities API"""

    def test_get_activities_success(self):
        """Test retrieving all activities successfully"""
        # Arrange - No special setup needed
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data
        # Verify structure of one activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)

    def test_signup_success(self):
        """Test successful signup for an activity"""
        # Arrange
        activity_name = "Basketball Team"  # Empty activity
        email = "test_signup@example.com"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Signed up {email} for {activity_name}" in data["message"]
        
        # Verify the participant was added
        get_response = client.get("/activities")
        activities = get_response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_duplicate_email(self):
        """Test signup fails when student is already signed up"""
        # Arrange
        activity_name = "Chess Club"  # Has existing participants
        email = "michael@mergington.edu"  # Already signed up
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Student already signed up" in data["detail"]

    def test_signup_invalid_activity(self):
        """Test signup fails for non-existent activity"""
        # Arrange
        invalid_activity = "NonExistent Club"
        email = "test@example.com"
        
        # Act
        response = client.post(f"/activities/{invalid_activity}/signup?email={email}")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_success(self):
        """Test successful unregistration from an activity"""
        # Arrange
        activity_name = "Programming Class"  # Has participants
        email = "emma@mergington.edu"  # Already signed up
        
        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Unregistered {email} from {activity_name}" in data["message"]
        
        # Verify the participant was removed
        get_response = client.get("/activities")
        activities = get_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_not_signed_up(self):
        """Test unregistration fails when student is not signed up"""
        # Arrange
        activity_name = "Basketball Team"  # Empty activity
        email = "not_signed_up@example.com"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Student not signed up" in data["detail"]

    def test_unregister_invalid_activity(self):
        """Test unregistration fails for non-existent activity"""
        # Arrange
        invalid_activity = "Fake Club"
        email = "test@example.com"
        
        # Act
        response = client.delete(f"/activities/{invalid_activity}/signup?email={email}")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_root_redirect(self):
        """Test root endpoint redirects to static index"""
        # Arrange - No special setup
        
        # Act
        response = client.get("/", follow_redirects=False)  # Don't follow redirects
        
        # Assert
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"
