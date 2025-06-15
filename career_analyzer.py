from gemini_service import GeminiService
from vector_service import VectorService
import json

class CareerAnalyzer:
    def __init__(self):
        self.gemini = GeminiService()
        self.vector_db = VectorService()
    
    def analyze_user_responses(self, responses):
        # Combine all responses into analysis text
        analysis_text = " ".join([f"{q}: {a}" for q, a in responses.items()])
        
        # Extract profile using Gemini
        profile_raw = self.gemini.analyze_responses(analysis_text)
        
        # Find matching careers using vector search
        matches = self.vector_db.find_matching_career(analysis_text)
        
        return {
            'profile': profile_raw,
            'career_matches': matches[:2]  # Top 2 matches
        }
    
    def generate_career_roadmap(self, career_path, user_profile):
        return self.gemini.generate_roadmap(career_path, user_profile)
