import os
import json
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai
from groq import AsyncGroq

# Load environment variables
load_dotenv()

# --- API KEY CONFIGURATION ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("⚠️ Gemini API Key not found. Please set it in your .env file.")

# --- Data storage path ---
DATA_PATH = r"D:\AI_MID_Project_Data\api_downloads\generated_content"
os.makedirs(DATA_PATH, exist_ok=True)

# --- MODEL AND CLIENT INITIALIZATION ---
gemini_model = None
if GEMINI_API_KEY:
    gemini_model = genai.GenerativeModel("gemini-2.5-pro")

groq_client = None
if GROQ_API_KEY:
    groq_client = AsyncGroq(api_key=GROQ_API_KEY)
else:
    print("⚠️ Groq API Key not found. Please set it in your .env file.")


async def generate_with_gemini(model, prompt):
    """Asynchronously generates content using a Gemini model."""
    if not model:
        return "Error: Gemini model is not initialized. Check API key."
    try:
        await asyncio.sleep(1)
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return f"Error with Gemini: {e}"

async def generate_with_groq(client, prompt):
    """Asynchronously generates content using a Groq model."""
    if not client:
        return "Error: Groq client is not initialized. Check API key."
    try:
        await asyncio.sleep(1)
        chat_completion = await client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error with Groq: {e}"

# --- UPDATED FUNCTION SIGNATURE to accept week_number ---
async def generate_course_content(curriculum_json_path, week_number=1, complexity="Intermediate", multimedia_prefs=None):
    """
    Generates comprehensive course content sequentially for a specific week.
    """
    if multimedia_prefs is None:
        multimedia_prefs = ["Text", "Images"]

    with open(curriculum_json_path, "r", encoding="utf-8") as f:
        curriculum_data = json.load(f)

    course_name = curriculum_data.get("course_name", "Unknown Course")
    curriculum_text = curriculum_data.get("curriculum_text", "")

    base_prompt = (
        f"You are an expert instructional designer creating content for a university course.\n"
        f"Course: {course_name}\n"
        f"Overall Curriculum:\n{curriculum_text}\n"
        f"Learning Complexity: {complexity}\n\n"
        f"Your task is to generate content *only* for the topics and activities listed for **Week {week_number}** in the curriculum."
    )

    # --- DYNAMIC PROMPTS BASED ON WEEK NUMBER ---
    prompts = {
        "lecture_notes": f"{base_prompt}\n\nGenerate detailed lecture notes for **Week {week_number}**. The notes should be clear, comprehensive, and include practical examples and explanations suitable for the specified complexity level.",
        "reading_materials": f"{base_prompt}\n\nProvide a list of 5-7 key reading materials (books, articles, websites, official documentation) that are highly relevant to the topics of **Week {week_number}**. For each, provide a brief description of its value.",
        "exercises_projects": f"{base_prompt}\n\nDesign two practical exercises and one project idea that directly correspond to the learning objectives and activities planned for **Week {week_number}**.",
        "assessment_questions": f"{base_prompt}\n\nDevelop a set of 10 assessment questions (a mix of multiple-choice and short-answer) that specifically test the knowledge and skills covered in **Week {week_number}**."
    }

    # --- SEQUENTIAL API CALLS ---
    print(f"Generating content for Week {week_number}...")
    lecture_notes = await generate_with_gemini(gemini_model, prompts["lecture_notes"])
    reading_materials = await generate_with_groq(groq_client, prompts["reading_materials"])
    exercises_projects = await generate_with_gemini(gemini_model, prompts["exercises_projects"])
    assessment_questions = await generate_with_groq(groq_client, prompts["assessment_questions"])

    generated_content = {
        "lecture_notes": lecture_notes,
        "reading_materials": reading_materials,
        "exercises_projects": exercises_projects,
        "assessment_questions": assessment_questions,
    }

    # Include week number in the filename for better organization
    output_filename = f"{course_name.replace(' ', '_')}_Week_{week_number}_content.json"
    output_filepath = os.path.join(DATA_PATH, output_filename)
    with open(output_filepath, "w", encoding="utf-8") as f:
        json.dump(generated_content, f, indent=4)

    return generated_content, output_filepath