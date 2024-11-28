from your_package import db
from your_package.models import Question

questions = [
    # Basic Info
    {
        "question_text": "What is your age range?",
        "category": "Basic Info",
        "question_type": "multiple_choice",
        "options": ["18-24", "25-30", "31-35", "36-40", "41-50", "51+"],
        "weight": 1.5
    },
    {
        "question_text": "What is your height?",
        "category": "Basic Info",
        "question_type": "multiple_choice",
        "options": ["Under 5'0\"", "5'0\"-5'4\"", "5'5\"-5'8\"", "5'9\"-6'0\"", "6'1\"-6'4\"", "Over 6'4\""],
        "weight": 1.0
    },
    
    # Lifestyle
    {
        "question_text": "How would you describe your lifestyle?",
        "category": "Lifestyle",
        "question_type": "multiple_choice",
        "options": ["Very Active", "Moderately Active", "Balanced", "Relaxed", "Homebody"],
        "weight": 2.0
    },
    {
        "question_text": "How often do you exercise?",
        "category": "Lifestyle",
        "question_type": "multiple_choice",
        "options": ["Daily", "3-4 times a week", "1-2 times a week", "Occasionally", "Rarely"],
        "weight": 1.5
    },
    
    # Values
    {
        "question_text": "How important is religion/spirituality in your life?",
        "category": "Values",
        "question_type": "scale",
        "options": None,
        "weight": 2.5
    },
    {
        "question_text": "What are your political views?",
        "category": "Values",
        "question_type": "multiple_choice",
        "options": ["Liberal", "Moderate", "Conservative", "Other", "Prefer not to say"],
        "weight": 2.0
    },
    
    # Interests
    {
        "question_text": "What are your favorite hobbies?",
        "category": "Interests",
        "question_type": "text",
        "options": None,
        "weight": 1.5
    },
    {
        "question_text": "What type of music do you enjoy?",
        "category": "Interests",
        "question_type": "text",
        "options": None,
        "weight": 1.0
    },
    
    # Personality
    {
        "question_text": "How would you describe your personality?",
        "category": "Personality",
        "question_type": "multiple_choice",
        "options": ["Extroverted", "Introverted", "Ambivert"],
        "weight": 2.0
    },
    {
        "question_text": "How do you typically spend your weekends?",
        "category": "Personality",
        "question_type": "text",
        "options": None,
        "weight": 1.5
    },
    
    # Goals
    {
        "question_text": "What are you looking for in a relationship?",
        "category": "Goals",
        "question_type": "multiple_choice",
        "options": ["Long-term relationship", "Dating", "Friendship", "Not sure yet"],
        "weight": 2.5
    },
    {
        "question_text": "Do you want children in the future?",
        "category": "Goals",
        "question_type": "multiple_choice",
        "options": ["Yes", "No", "Maybe", "Have children already"],
        "weight": 2.0
    },
    
    # Habits
    {
        "question_text": "Do you smoke?",
        "category": "Habits",
        "question_type": "multiple_choice",
        "options": ["Yes", "No", "Occasionally", "Trying to quit"],
        "weight": 2.0
    },
    {
        "question_text": "How often do you drink alcohol?",
        "category": "Habits",
        "question_type": "multiple_choice",
        "options": ["Never", "Rarely", "Socially", "Regularly"],
        "weight": 1.5
    },
    
    # Social
    {
        "question_text": "How do you prefer to spend your free time?",
        "category": "Social",
        "question_type": "text",
        "options": None,
        "weight": 1.5
    },
    {
        "question_text": "What's your ideal first date?",
        "category": "Social",
        "question_type": "text",
        "options": None,
        "weight": 1.0
    },
    
    # Career
    {
        "question_text": "What is your current career status?",
        "category": "Career",
        "question_type": "multiple_choice",
        "options": ["Student", "Employed", "Self-employed", "Looking for work", "Retired"],
        "weight": 1.0
    },
    {
        "question_text": "What are your career ambitions?",
        "category": "Career",
        "question_type": "text",
        "options": None,
        "weight": 1.0
    },
    
    # Family
    {
        "question_text": "How important is family in your life?",
        "category": "Family",
        "question_type": "scale",
        "options": None,
        "weight": 2.0
    },
    {
        "question_text": "What's your relationship with your family like?",
        "category": "Family",
        "question_type": "text",
        "options": None,
        "weight": 1.5
    }
]

def populate_questions():
    for q in questions:
        question = Question(
            question_text=q["question_text"],
            category=q["category"],
            question_type=q["question_type"],
            options=q["options"],
            weight=q["weight"]
        )
        db.session.add(question)
    
    try:
        db.session.commit()
        print("Successfully added questions to the database!")
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    populate_questions()
