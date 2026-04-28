import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for testing the FastAPI application"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before and after each test"""
    original = {
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
            "description": "Practice drills and compete in weekend soccer matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["liam@mergington.edu", "ava@mergington.edu"]
        },
        "Yoga Club": {
            "description": "Relax, stretch, and build strength with guided yoga sessions",
            "schedule": "Wednesdays, 4:00 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["noah@mergington.edu", "mia@mergington.edu"]
        },
        "Art Workshop": {
            "description": "Explore painting, drawing, and mixed media art projects",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting, stagecraft, and performance preparation for school plays",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["mia@mergington.edu", "alex@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and discuss scientific discoveries",
            "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
            "max_participants": 14,
            "participants": ["chloe@mergington.edu", "ethan@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop arguments and compete in interschool debate tournaments",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 12,
            "participants": ["sophia@mergington.edu", "mason@mergington.edu"]
        }
    }
    
    # Clear and repopulate activities before test
    activities.clear()
    activities.update(original)
    
    yield
    
    # Reset after test
    activities.clear()
    activities.update(original)
