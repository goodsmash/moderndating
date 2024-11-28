from typing import List, Dict, Tuple
import numpy as np
from datetime import datetime
from models import User, UserResponse, Question, Match
from app import db

class MatchingSystem:
    def __init__(self):
        self.weights = {
            'questionnaire': 0.4,
            'demographics': 0.3,
            'activity': 0.2,
            'location': 0.1
        }

    def calculate_match_score(self, user1: User, user2: User) -> float:
        """Calculate the overall match score between two users."""
        if not self._is_compatible_orientation(user1, user2):
            return 0.0

        scores = {
            'questionnaire': self._calculate_questionnaire_similarity(user1, user2),
            'demographics': self._calculate_demographic_compatibility(user1, user2),
            'activity': self._calculate_activity_score(user2),
            'location': self._calculate_location_score(user1, user2)
        }
        
        weighted_score = sum(self.weights[key] * score for key, score in scores.items())
        return round(weighted_score * 100, 1)  # Convert to percentage with one decimal

    def _is_compatible_orientation(self, user1: User, user2: User) -> bool:
        """Check if users are compatible based on gender and preferences."""
        return (user1.looking_for == user2.gender and 
                user2.looking_for == user1.gender)

    def _calculate_questionnaire_similarity(self, user1: User, user2: User) -> float:
        """Calculate similarity score based on questionnaire responses."""
        user1_responses = {r.question_id: r.response for r in user1.responses}
        user2_responses = {r.question_id: r.response for r in user2.responses}
        
        # Get common questions answered by both users
        common_questions = set(user1_responses.keys()) & set(user2_responses.keys())
        if not common_questions:
            return 0.0
        
        # Calculate similarity for each question
        similarities = []
        for question_id in common_questions:
            question = Question.query.get(question_id)
            if question.question_type == 'scale':
                # For scale questions, calculate normalized difference
                score = 1 - abs(float(user1_responses[question_id]) - 
                              float(user2_responses[question_id])) / 10
            else:
                # For other questions, exact match = 1, no match = 0
                score = float(user1_responses[question_id] == user2_responses[question_id])
            similarities.append(score)
        
        return sum(similarities) / len(similarities)

    def _calculate_demographic_compatibility(self, user1: User, user2: User) -> float:
        """Calculate compatibility based on demographics (age, etc)."""
        if not (user1.birth_date and user2.birth_date):
            return 0.5  # Neutral score if data missing
        
        age1 = (datetime.now().date() - user1.birth_date).days / 365.25
        age2 = (datetime.now().date() - user2.birth_date).days / 365.25
        
        # Age difference penalty (0.1 point per year of difference, max 1.0)
        age_diff_penalty = min(abs(age1 - age2) * 0.1, 1.0)
        return 1.0 - age_diff_penalty

    def _calculate_activity_score(self, user: User) -> float:
        """Calculate activity score based on profile completeness and recent activity."""
        # Profile completeness (50% of activity score)
        required_fields = ['birth_date', 'gender', 'looking_for', 'bio', 'location']
        completed_fields = sum(1 for field in required_fields if getattr(user, field))
        profile_score = completed_fields / len(required_fields)
        
        # Recent activity (50% of activity score)
        days_since_creation = (datetime.utcnow() - user.created_at).days
        activity_score = 1.0 if days_since_creation < 30 else 0.5
        
        return (profile_score * 0.5) + (activity_score * 0.5)

    def _calculate_location_score(self, user1: User, user2: User) -> float:
        """Calculate location compatibility score."""
        if not (user1.location and user2.location):
            return 0.5  # Neutral score if location missing
        
        # Simple string comparison for now
        # TODO: Implement proper geocoding and distance calculation
        return 1.0 if user1.location.lower() == user2.location.lower() else 0.0

    def get_top_matches(self, user_id: int, limit: int = 10) -> List[Tuple[User, float]]:
        """Get top matches for a user."""
        user = User.query.get(user_id)
        if not user:
            return []
        
        # Get all potential matches
        potential_matches = User.query.filter(
            User.id != user_id,
            User.gender == user.looking_for,
            User.looking_for == user.gender
        ).all()
        
        # Calculate scores and sort
        matches = []
        for potential_match in potential_matches:
            score = self.calculate_match_score(user, potential_match)
            if score > 0:  # Only include non-zero scores
                matches.append((potential_match, score))
        
        # Sort by score and limit results
        matches.sort(key=lambda x: x[1], reverse=True)
        top_matches = matches[:limit]
        
        # Store matches in database
        for match_user, score in top_matches:
            existing_match = Match.query.filter(
                ((Match.user1_id == user.id) & (Match.user2_id == match_user.id)) |
                ((Match.user1_id == match_user.id) & (Match.user2_id == user.id))
            ).first()
            
            if not existing_match:
                new_match = Match(
                    user1_id=user.id,
                    user2_id=match_user.id,
                    match_score=score
                )
                db.session.add(new_match)
        
        db.session.commit()
        return top_matches
