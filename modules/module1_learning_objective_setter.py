import os
import json
from dotenv import load_dotenv
from google import generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

# Data storage path
DATA_PATH = r"D:\AI_MID_Project_Data\api_downloads\Objectives"
os.makedirs(DATA_PATH, exist_ok=True)

# Bloom's taxonomy verbs
BLOOM_VERBS = {
    "Undergraduate_Basic": ["Describe", "Identify", "Explain", "Apply"],
    "Undergraduate_Advanced": ["Analyze", "Compare", "Construct", "Evaluate"],
    "Graduate": ["Critically assess", "Integrate", "Design", "Develop"],
    "Professional": ["Implement", "Optimize", "Strategize", "Lead"]
}

def generate_learning_objectives(topic, level, credit_hours):
    try:
        prompt = f"""
        You are an academic course designer.

        Generate 5 measurable learning objectives for a course titled '{topic}'.
        Audience: {level} students.
        Course Duration: {credit_hours} credit hours.

        Use Bloom’s Taxonomy verbs suitable for {level} level.
        Focus on both technical and practical skills that are highly relevant in today's job market.

        Return only the numbered list of objectives.
        """

        # Generate response using Gemini
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)

        # Extract text safely
        if not hasattr(response, "text") or not response.text:
            raise ValueError("No valid response text from Gemini API.")

        objectives_text = response.text.strip()
        objectives = [line.strip() for line in objectives_text.split("\n") if line.strip()]

        # Save output
        filename = f"{topic.replace(' ', '_')}_learning_objectives.json"
        filepath = os.path.join(DATA_PATH, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({"topic": topic, "objectives": objectives}, f, indent=4)

        return objectives, filepath

    except Exception as e:
        print(f"❌ Error generating objectives (Gemini): {e}")
        return [], None
