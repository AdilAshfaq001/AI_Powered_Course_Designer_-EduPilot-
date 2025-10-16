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
DATA_PATH = r"D:\AI_MID_Project_Data\api_downloads\curriculums"
os.makedirs(DATA_PATH, exist_ok=True)

def generate_curriculum(input_data, semester_weeks=15, approach="Project-based", assessments="Mixed"):
    """
    Generate a structured weekly curriculum using Gemini 2.5 Pro.

    input_data: list of learning objectives OR path to JSON from Module 1
    semester_weeks: int
    approach: str, e.g., Project-based / Theory / Blended
    assessments: list or str, e.g., ["Quizzes", "Projects"]
    """
    try:
        # Load learning objectives if input is a JSON file
        if isinstance(input_data, str) and input_data.endswith(".json"):
            with open(input_data, "r", encoding="utf-8") as f:
                obj = json.load(f)
                learning_objectives = obj.get("objectives", [])
                course_name = obj.get("topic", "Unknown Course")
        else:
            learning_objectives = input_data
            course_name = "Custom Course"

        # Convert assessments to string if list
        if isinstance(assessments, list):
            assessments_str = ", ".join(assessments)
        else:
            assessments_str = assessments

        prompt = f"""
        You are an expert academic course designer.

Generate a {semester_weeks}-week university curriculum based on the following learning objectives:

{learning_objectives}

Course Parameters:
- Pedagogical Approach: {approach}
- Assessment Preferences: {assessments_str}
- Duration: {semester_weeks} weeks

Requirements:
1. Divide the course into exactly 4 modules:
   - Module 1: 
   - Module 2: 
   - Module 3: 
   - Module 4: 
2. Each module must indicate the weeks it covers (e.g., "Weeks 1-4").
3. For each week, provide:
   - Topics
   - Activities
   - Assessment (if applicable)
4. Use numbered list format for weeks.
5. Clearly mark module headers as: **Module 1: [Module Name]**, **Module 2: [Module Name]**, etc.
6. Output plain text only. Do not add introductory phrases like "Of course" or apologies.

Ensure the output is ready for Streamlit expanders.
"""

        # Generate response using Gemini
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)

        # Extract text safely
        if not hasattr(response, "text") or not response.text:
            raise ValueError("No valid response text from Gemini API.")

        curriculum_text = response.text.strip()

        # Save curriculum to JSON in a structured format for Module 3
        curriculum_json = {
            "course_name": course_name,
            "approach": approach,
            "assessments": assessments_str,
            "semester_weeks": semester_weeks,
            "learning_objectives": learning_objectives,
            "curriculum_text": curriculum_text
        }

        filename = f"{course_name.replace(' ', '_')}_curriculum.json"
        filepath = os.path.join(DATA_PATH, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(curriculum_json, f, indent=4)

        return curriculum_text, filepath

    except Exception as e:
        print(f"❌ Error generating curriculum (Gemini): {e}")
        return "", None
