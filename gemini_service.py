import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
from config import Config

class GeminiService:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = GoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=Config.GEMINI_API_KEY)
    
    def analyze_responses(self, responses):
        prompt = f"""
        Analyze these career interest responses and extract key themes:
        {responses}
        
        Return a JSON with:
        - interests: list of main interests
        - skills: list of mentioned skills
        - preferences: work style preferences
        - goals: career goals mentioned
        
        Be concise and specific.
        """
        return self.model.predict(prompt)
    
    def generate_roadmap(self, career_path, user_profile):
        prompt = f"""
        Create a detailed 3-month career roadmap for {career_path} based on this profile:
        {user_profile}
        
        Include:
        1. Month-by-month breakdown
        2. Free resources (courses, websites, books)
        3. Practical projects
        4. Skills to develop
        5. Networking opportunities
        
        Format as HTML-friendly text with clear sections.
        """
        return self.model.predict(prompt)
