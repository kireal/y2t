import pytest
from typing import Dict, List


@pytest.fixture
def sample_transcript_data() -> List[Dict]:
    """Fixture providing sample transcript data for testing."""
    return [
        {
            "text": "All right, so here we are at the zoo.",
            "start": 0.0,
            "duration": 2.0,
        },
        {"text": "The elephants are over there.", "start": 2.0, "duration": 2.5},
    ]
