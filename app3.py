import streamlit as st
import asyncio
import os
from modules.module3_content_generator import generate_course_content

st.set_page_config(layout="wide")
st.title("EduDesign AI — Module 3: Content Generator")

st.info(
    "This module uses the curriculum from Module 2 to generate detailed course content "
    "for a specific module."
)

with st.form("content_generation_form"):
    uploaded_file = st.file_uploader("Upload Module 2 JSON file", type=["json"])

    # --- NEW: Add a dropdown to select the module number ---
    module_number = st.selectbox(
        "Select Module to Generate Content For",
        options=[1, 2, 3, 4],
        index=0  # Default to Module 1
    )

    complexity = st.select_slider(
        "Select Learning Complexity",
        options=["Beginner", "Intermediate", "Advanced", "Expert"],
        value="Intermediate"
    )

    multimedia_prefs = st.multiselect(
        "Multimedia Preferences",
        ["Text", "Images", "Videos", "Interactive simulations"],
        default=["Text", "Images"]
    )

    submitted = st.form_submit_button("Generate Course Content")

if submitted and uploaded_file:
    temp_dir = os.path.join(r"D:\AI_MID_Project_Data\api_downloads", "temp")
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner(f"🚀 Generating content for Module {module_number}..."):
        # --- Pass the selected module_number to the function ---
        content, filepath = asyncio.run(generate_course_content(
            temp_path, module_number, complexity, multimedia_prefs
        ))
        st.success(f"✅ Content generation for Module {module_number} complete!")

        st.subheader(f"Generated Content for Module {module_number}")

        with st.expander("📝 Lecture Notes"):
            st.markdown(content.get("lecture_notes", "Not available."))

        with st.expander("📚 Reading Materials & References"):
            st.markdown(content.get("reading_materials", "Not available."))

        with st.expander("💻 Exercises & Projects"):
            st.markdown(content.get("exercises_projects", "Not available."))

        with st.expander("❓ Assessment Questions"):
            st.markdown(content.get("assessment_questions", "Not available."))

        with open(filepath, "r", encoding="utf-8") as f:
            st.download_button(
                label=f"📥 Download Content for Module {module_number} (JSON)",
                data=f.read(),
                file_name=os.path.basename(filepath),
                mime="application/json"
            )

elif submitted and not uploaded_file:
    st.error("Please upload the JSON file from Module 2.")