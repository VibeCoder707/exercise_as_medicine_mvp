from datetime import datetime
from typing import Dict, List
from .data_models import Exercise

# Sample exercise database
EXERCISE_DB: Dict[str, Exercise] = {
    "ex_001": Exercise(
        id="ex_001",
        name="Chair Stand",
        description="Stand up from a seated position without using your hands",
        difficulty_level="beginner",
        target_areas=["lower body strength", "balance"],
        contraindications=["severe knee pain", "recent hip surgery"],
        video_url="https://example.com/chair-stand"
    ),
    "ex_002": Exercise(
        id="ex_002",
        name="Wall Push-Up",
        description="Standing push-ups against a wall",
        difficulty_level="beginner",
        target_areas=["upper body strength", "core"],
        contraindications=["shoulder injury", "acute wrist pain"],
        video_url="https://example.com/wall-pushup"
    ),
    "ex_003": Exercise(
        id="ex_003",
        name="Heel-Toe Walk",
        description="Walk in a straight line placing heel to toe",
        difficulty_level="beginner",
        target_areas=["balance", "coordination"],
        contraindications=["severe vertigo", "acute ankle injury"],
        video_url="https://example.com/heel-toe-walk"
    ),
}

# Condition to exercise mapping
CONDITION_EXERCISES: Dict[str, List[str]] = {
    "fall_prevention": ["ex_001", "ex_003"],
    "pain_management": ["ex_002"],
    "diabetes_management": ["ex_001", "ex_002"],
    "weight_management": ["ex_001", "ex_002", "ex_003"],
}

# Sample recommendation rules
def get_exercises_for_condition(condition: str) -> List[Exercise]:
    """Get recommended exercises for a specific condition."""
    exercise_ids = CONDITION_EXERCISES.get(condition, [])
    return [EXERCISE_DB[ex_id] for ex_id in exercise_ids]