"""
Test dataset for Math Tutor evaluation
Contains problems from Class 6-10 curriculum with expected answers
"""

TEST_PROBLEMS = [
    {
        "id": 1,
        "problem": "Solve for x: 2x + 5 = 15",
        "expected_answer": "x = 5",
        "category": "Linear Algebra",
        "grade_level": "8-9",
        "difficulty": "medium"
    },
    {
        "id": 2,
        "problem": "What is 15% of 240?",
        "expected_answer": "36",
        "category": "Percentage",
        "grade_level": "6-7", 
        "difficulty": "easy"
    }
]

# Ambiguous test cases for fallback mechanism
AMBIGUOUS_QUERIES = [
    "help with math",
    "solve this problem",
    "I need help",
    "can you teach me?",
    "what is math?"
]

def get_test_problems():
    """Return all test problems"""
    return TEST_PROBLEMS

def get_problem_by_id(problem_id):
    """Get a specific problem by ID"""
    for problem in TEST_PROBLEMS:
        if problem["id"] == problem_id:
            return problem
    return None

def get_problems_by_category(category):
    """Get problems filtered by category"""
    return [p for p in TEST_PROBLEMS if p["category"] == category]

def get_problems_by_difficulty(difficulty):
    """Get problems filtered by difficulty"""
    return [p for p in TEST_PROBLEMS if p["difficulty"] == difficulty] 