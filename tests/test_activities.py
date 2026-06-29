"""
Tests for retrieving activities from the Mergington High School API.

These tests verify the GET /activities endpoint using the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up the test client fixture
- Act: Make a GET request to /activities
- Assert: Verify the response status and content
"""

import pytest


class TestGetActivities:
    """Test suite for the GET /activities endpoint."""

    def test_successfully_retrieve_all_activities(self, test_client, sample_activities):
        """
        Test that GET /activities returns all available activities.
        
        AAA Pattern:
        - Arrange: test_client and sample_activities fixtures are ready
        - Act: Make GET request to /activities
        - Assert: Response contains all activities
        """
        # Act
        response = test_client.get("/activities")

        # Assert - Status code
        assert response.status_code == 200

        # Assert - Response contains all activities
        activities_response = response.json()
        assert len(activities_response) == len(sample_activities)
        for activity_name in sample_activities:
            assert activity_name in activities_response


    def test_activity_structure_is_correct(self, test_client, sample_activities):
        """
        Test that each activity has the correct structure with required fields.
        
        AAA Pattern:
        - Arrange: test_client and sample_activities fixtures
        - Act: Make GET request and extract one activity
        - Assert: Activity has all required fields with correct types
        """
        # Act
        response = test_client.get("/activities")
        activities_response = response.json()

        # Assert - Verify structure of activities
        required_fields = {"description", "schedule", "max_participants", "participants"}
        for activity_name, activity_data in activities_response.items():
            assert set(activity_data.keys()) == required_fields
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)


    def test_initial_participant_count(self, test_client, sample_activities):
        """
        Test that activities return the expected initial number of participants.
        
        AAA Pattern:
        - Arrange: test_client and sample_activities fixtures
        - Act: Retrieve activities and count participants per activity
        - Assert: Each activity has the expected number of initial participants
        """
        # Arrange
        expected_participants = {
            "Chess Club": 2,
            "Programming Class": 2,
            "Gym Class": 2,
            "Soccer Team": 2,
            "Swimming Club": 2,
            "Art Studio": 2,
            "Drama Club": 2
        }

        # Act
        response = test_client.get("/activities")
        activities_response = response.json()

        # Assert
        for activity_name, expected_count in expected_participants.items():
            actual_count = len(activities_response[activity_name]["participants"])
            assert actual_count == expected_count, \
                f"{activity_name} expected {expected_count} participants, got {actual_count}"
