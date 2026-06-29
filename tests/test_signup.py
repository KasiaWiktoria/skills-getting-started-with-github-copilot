"""
Tests for signing up students for activities in the Mergington High School API.

These tests verify the POST /activities/{activity_name}/signup endpoint using the 
AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and test client
- Act: Make a POST request to the signup endpoint
- Assert: Verify response status, content, and side effects
"""

import pytest


class TestSignupForActivity:
    """Test suite for the POST /activities/{activity_name}/signup endpoint."""

    def test_successfully_signup_new_student(self, test_client):
        """
        Test that a new student can successfully sign up for an activity.
        
        AAA Pattern:
        - Arrange: Prepare test client and new student email
        - Act: POST signup request for Chess Club
        - Assert: Verify success response and participant is added
        """
        # Arrange
        activity_name = "Chess Club"
        email = "new_student@mergington.edu"

        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert - Status and response message
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]

        # Assert - Verify participant was actually added
        activities_response = test_client.get("/activities").json()
        assert email in activities_response[activity_name]["participants"]


    def test_activity_not_found_returns_404(self, test_client):
        """
        Test that signing up for a non-existent activity returns 404.
        
        AAA Pattern:
        - Arrange: Prepare test client and non-existent activity name
        - Act: POST signup request for fake activity
        - Assert: Verify 404 status and error message
        """
        # Arrange
        nonexistent_activity = "Fake Activity"
        email = "student@mergington.edu"

        # Act
        response = test_client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


    def test_duplicate_signup_returns_400(self, test_client):
        """
        Test that signing up the same student twice returns 400.
        
        AAA Pattern:
        - Arrange: Sign up a student for an activity
        - Act: Attempt to sign up the same student again
        - Assert: Verify 400 status and "already signed up" error message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in initial participants

        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]


    def test_multiple_students_can_signup(self, test_client):
        """
        Test that multiple different students can sign up for the same activity.
        
        AAA Pattern:
        - Arrange: Prepare multiple unique student emails
        - Act: Sign up each student sequentially
        - Assert: Verify all are added and no conflicts occur
        """
        # Arrange
        activity_name = "Programming Class"
        new_students = [
            "student1@mergington.edu",
            "student2@mergington.edu",
            "student3@mergington.edu"
        ]

        # Act & Assert
        for email in new_students:
            response = test_client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # Assert - Verify all students were added
        activities = test_client.get("/activities").json()
        for email in new_students:
            assert email in activities[activity_name]["participants"]


    def test_signup_increments_participant_count(self, test_client):
        """
        Test that signing up a student increments the participant count.
        
        AAA Pattern:
        - Arrange: Get initial participant count for an activity
        - Act: Sign up a new student
        - Assert: Verify participant count increased by 1
        """
        # Arrange
        activity_name = "Gym Class"
        initial_activities = test_client.get("/activities").json()
        initial_count = len(initial_activities[activity_name]["participants"])
        email = "new_participant@mergington.edu"

        # Act
        test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        updated_activities = test_client.get("/activities").json()
        updated_count = len(updated_activities[activity_name]["participants"])
        assert updated_count == initial_count + 1


    def test_signup_preserves_existing_participants(self, test_client):
        """
        Test that adding a new participant doesn't remove existing ones.
        
        AAA Pattern:
        - Arrange: Get initial participant list
        - Act: Sign up a new student
        - Assert: Verify existing participants are still there and new one is added
        """
        # Arrange
        activity_name = "Soccer Team"
        initial_activities = test_client.get("/activities").json()
        initial_participants = set(initial_activities[activity_name]["participants"])
        new_email = "new_soccer_player@mergington.edu"

        # Act
        test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )

        # Assert
        updated_activities = test_client.get("/activities").json()
        updated_participants = set(updated_activities[activity_name]["participants"])
        
        # All initial participants should still be there
        assert initial_participants.issubset(updated_participants)
        # Plus the new participant
        assert new_email in updated_participants
        # Count should be exactly 1 more
        assert len(updated_participants) == len(initial_participants) + 1
