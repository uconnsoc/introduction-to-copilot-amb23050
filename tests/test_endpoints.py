"""
Test suite for the Activities API using AAA (Arrange-Act-Assert) pattern.
Tests cover all endpoints: GET /activities, POST /signup, DELETE /unregister, and GET /
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that the endpoint returns all 9 activities"""
        # Arrange - no additional setup needed, using fixture
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        
    def test_get_activities_returns_correct_structure(self, client, reset_activities):
        """Test that each activity has the required fields"""
        # Arrange - no additional setup needed
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        activity = data["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)
        
    def test_get_activities_has_correct_participant_count(self, client, reset_activities):
        """Test that participant lists contain correct data"""
        # Arrange - no additional setup needed
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert len(data["Chess Club"]["participants"]) == 2
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in data["Chess Club"]["participants"]


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_successful(self, client, reset_activities):
        """Test successful signup of a new student for an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]
        
        # Verify participant was added
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert email in participants
        
    def test_signup_duplicate_returns_400(self, client, reset_activities):
        """Test that signing up an already registered student returns 400"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
        
    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities):
        """Test that signing up for non-existent activity returns 404"""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
        
    def test_signup_with_special_characters_in_email(self, client, reset_activities):
        """Test that emails with special characters are handled correctly"""
        # Arrange
        activity_name = "Chess Club"
        email = "test+tag@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert email in participants
        
    def test_signup_updates_participant_count(self, client, reset_activities):
        """Test that participant count increases after signup"""
        # Arrange
        activity_name = "Programming Class"
        email = "newstudent@mergington.edu"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity_name]["participants"])
        assert updated_count == initial_count + 1
        
    def test_signup_multiple_different_students(self, client, reset_activities):
        """Test that multiple different students can sign up for same activity"""
        # Arrange
        activity_name = "Yoga Club"
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        # Act
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert email1 in participants
        assert email2 in participants


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/signup endpoint"""
    
    def test_unregister_successful(self, client, reset_activities):
        """Test successful unregistration of a student from an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email in response.json()["message"]
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert email not in participants
        
    def test_unregister_nonparticipant_returns_400(self, client, reset_activities):
        """Test that unregistering a non-participant returns 400"""
        # Arrange
        activity_name = "Chess Club"
        email = "notstudent@mergington.edu"  # Not registered
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]
        
    def test_unregister_from_nonexistent_activity_returns_404(self, client, reset_activities):
        """Test that unregistering from non-existent activity returns 404"""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
        
    def test_unregister_updates_participant_count(self, client, reset_activities):
        """Test that participant count decreases after unregistration"""
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity_name]["participants"])
        assert updated_count == initial_count - 1
        
    def test_unregister_then_signup_again(self, client, reset_activities):
        """Test that a student can sign up again after unregistering"""
        # Arrange
        activity_name = "Soccer Team"
        email = "liam@mergington.edu"
        
        # Act
        unregister_response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert unregister_response.status_code == 200
        assert signup_response.status_code == 200
        activities_response = client.get("/activities")
        participants = activities_response.json()[activity_name]["participants"]
        assert email in participants


class TestRootRedirect:
    """Tests for GET / endpoint"""
    
    def test_root_redirects_to_index(self, client):
        """Test that root path redirects to static index"""
        # Arrange - no setup needed
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]


class TestFutureProofing:
    """Tests for validations that should be added in future (currently skipped)"""
    
    @pytest.mark.skip(reason="Max participant limit not yet implemented")
    def test_signup_fails_when_activity_full(self, client, reset_activities):
        """Test that signup fails when activity reaches max participants"""
        # Arrange - fill up an activity
        activity_name = "Chess Club"
        max_participants = 12
        current_participants = 2
        
        # Sign up additional students to reach max
        for i in range(max_participants - current_participants):
            email = f"student{i}@mergington.edu"
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
        
        # Act - try to add one more when full
        final_email = "overfull@mergington.edu"
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": final_email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "full" in response.json()["detail"].lower()
        
    @pytest.mark.skip(reason="Spots calculation not yet validated")
    def test_available_spots_never_negative(self, client, reset_activities):
        """Test that available spots calculation never goes negative"""
        # Arrange - get all activities
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity in data.items():
            available_spots = activity["max_participants"] - len(activity["participants"])
            assert available_spots >= 0, f"{activity_name} has negative spots ({available_spots})"
