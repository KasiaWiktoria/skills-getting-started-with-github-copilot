"""
Pytest configuration and fixtures for FastAPI backend tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def test_client():
    """
    Fixture that provides a TestClient instance for making requests to the app.
    
    This allows tests to make HTTP requests to the FastAPI app without 
    spinning up a server.
    """
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """
    Fixture that provides sample activity data for testing.
    
    Returns a dictionary that mirrors the structure of the activities
    defined in the app, allowing tests to verify the correct data structure
    and values.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Practice team skills and compete in local matches",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["alex@mergington.edu", "nina@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Build swimming endurance and train for events",
            "schedule": "Wednesdays and Fridays, 3:00 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["liam@mergington.edu", "mia@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore drawing, painting, and mixed media art projects",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["avery@mergington.edu", "zoe@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform scenes, learn theater skills, and prepare for showcases",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["noah@mergington.edu", "harper@mergington.edu"]
        }
    }
