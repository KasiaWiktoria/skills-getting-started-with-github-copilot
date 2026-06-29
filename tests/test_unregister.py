"""
Tests for unregistering students from activities in the Mergington High School API.

These tests verify the DELETE /activities/{activity_name}/participants endpoint using the 
AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and test client
- Act: Make a DELETE request to the unregister endpoint
- Assert: Verify response status, content, and side effects
"""

import pytest


class TestUnregisterParticipant:
    """Test suite for the DELETE /activities/{activity_name}/participants endpoint."""

    def test_successfully_remove_participant(self, test_client):
        """
        Test that an existing participant can be successfully removed.
        
        AAA Pattern:
        - Arrange: Select a participant from an activity
        - Act: DELETE request to remove the participant
        - Assert: Verify success and participant is removed
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Initially in participants

        # Act
        response = test_client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert - Status and response message
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]
        assert email in response.json()["message"]

        # Assert - Verify participant was actually removed
        activities = test_client.get("/activities").json()
        assert email not in activities[activity_name]["participants"]


    def test_unregister_nonexistent_activity_returns_404(self, test_client):
        """
        Test that removing from a non-existent activity returns 404.
        
        AAA Pattern:
        - Arrange: Prepare non-existent activity name
        - Act: DELETE request for fake activity
        - Assert: Verify 404 status and error message
        """
        # Arrange
        nonexistent_activity = "Fake Activity"
        email = "student@mergington.edu"

        # Act
        response = test_client.delete(
            f"/activities/{nonexistent_activity}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


    def test_unregister_nonexistent_participant_returns_400(self, test_client):
        """
        Test that removing a non-existent participant returns 400.
        
        AAA Pattern:
        - Arrange: Prepare email not in activity's participants
        - Act: DELETE request for non-existent participant
        - Assert: Verify 400 status and "Participant not found" error
        """
        # Arrange
        activity_name = "Gym Class"
        email = "nonexistent@mergington.edu"

        # Act
        response = test_client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "Participant not found" in response.json()["detail"]


    def test_unregister_decrements_participant_count(self, test_client):
        """
        Test that removing a participant decrements the participant count.
        
        AAA Pattern:
        - Arrange: Get initial participant count
        - Act: Remove a participant
        - Assert: Verify count decreased by 1
        """
        # Arrange
        activity_name = "Swimming Club"
        initial_activities = test_client.get("/activities").json()
        initial_count = len(initial_activities[activity_name]["participants"])
        email = "liam@mergington.edu"

        # Act
        test_client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        updated_activities = test_client.get("/activities").json()
        updated_count = len(updated_activities[activity_name]["participants"])
        assert updated_count == initial_count - 1


    def test_unregister_preserves_other_participants(self, test_client):
        """
        Test that removing one participant doesn't affect others.
        
        AAA Pattern:
        - Arrange: Get initial participant list
        - Act: Remove one specific participant
        - Assert: Verify only that one is removed, others remain
        """
        # Arrange
        activity_name = "Art Studio"
        initial_activities = test_client.get("/activities").json()
        initial_participants = set(initial_activities[activity_name]["participants"])
        email_to_remove = "avery@mergington.edu"
        other_participants = initial_participants - {email_to_remove}

        # Act
        test_client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email_to_remove}
        )

        # Assert
        updated_activities = test_client.get("/activities").json()
        updated_participants = set(updated_activities[activity_name]["participants"])
        
        # All other participants should still be there
        assert other_participants == updated_participants
        # The removed email should not be present
        assert email_to_remove not in updated_participants


    def test_signup_then_unregister_sequence(self, test_client):
        """
        Test the sequence of signing up and then unregistering a student.
        
        AAA Pattern:
        - Arrange: Initial state with test client
        - Act: Sign up a new student, then unregister them
        - Assert: Verify participant count returns to original level
        """
        # Arrange
        activity_name = "Drama Club"
        email = "new_drama_student@mergington.edu"
        initial_activities = test_client.get("/activities").json()
        initial_count = len(initial_activities[activity_name]["participants"])

        # Act - Sign up
        test_client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert - Participant was added
        after_signup = test_client.get("/activities").json()
        assert len(after_signup[activity_name]["participants"]) == initial_count + 1
        assert email in after_signup[activity_name]["participants"]

        # Act - Unregister
        response = test_client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert - Participant was removed and back to original count
        assert response.status_code == 200
        after_unregister = test_client.get("/activities").json()
        assert len(after_unregister[activity_name]["participants"]) == initial_count
        assert email not in after_unregister[activity_name]["participants"]


    def test_cannot_unregister_twice(self, test_client):
        """
        Test that attempting to unregister the same student twice fails on second attempt.
        
        AAA Pattern:
        - Arrange: Remove a participant once
        - Act: Attempt to remove the same participant again
        - Assert: Verify second attempt returns 400 (not found)
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"

        # Act - First unregister (should succeed)
        response1 = test_client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        assert response1.status_code == 200

        # Act - Second unregister (should fail)
        response2 = test_client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response2.status_code == 400
        assert "Participant not found" in response2.json()["detail"]
