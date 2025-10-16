import streamlit as st
from modules.module2_curriculum_structurer import generate_curriculum
import os
import re
from docx import Document  # dependency for .docx download

st.title("EduDesign AI — Module 2: Curriculum Structurer")

with st.form("curriculum_form"):
    uploaded_file = st.file_uploader("Upload Module 1 JSON file (optional)", type=["json"])
    learning_outcomes_input = st.text_area("Or paste Learning Outcomes here")

    time_weeks = st.slider("Course Duration (weeks)", 8, 20, 15)
    approach = st.selectbox("Pedagogical Approach", ["Project-based", "Theory", "Blended"])
    assessments = st.multiselect("Assessment Preferences", ["Quizzes", "Projects", "Exams", "Presentations", "Labs"])

    submitted = st.form_submit_button("Generate Curriculum")

if submitted:
    if uploaded_file:
        temp_path = os.path.join(r"D:\AI_MID_Project_Data\api_downloads", uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        learning_input = temp_path
    else:
        learning_input = learning_outcomes_input

    with st.spinner("Generating curriculum..."):
        curriculum_text, _ = generate_curriculum(learning_input, time_weeks, approach, assessments)
        st.success("Curriculum Generated!")

        # === Present curriculum in expanders ===
        modules = re.split(r"(?=\*\*Module \d+)", curriculum_text)  # split but keep header
        for mod in modules:
            if mod.strip():
                header_match = re.match(r"\*\*(Module \d+.*?)\*\*", mod)
                header = header_match.group(1) if header_match else "Module"
                body = mod.replace(f"**{header}**", "").strip()
                with st.expander(header):
                    st.markdown(body, unsafe_allow_html=True)

        # Full text fallback
        with st.expander("Full Curriculum Text"):
            st.text_area("Curriculum Plan", curriculum_text, height=400)

        # === TXT download ===
        download_path_txt = os.path.join(r"D:\AI_MID_Project_Data\api_downloads", "Curriculum_Plan.txt")
        with open(download_path_txt, "w", encoding="utf-8") as f:
            f.write(curriculum_text)

        st.download_button(
            label="📥 Download Curriculum Plan (TXT)",
            data=curriculum_text,
            file_name="Curriculum_Plan.txt",
            mime="text/plain"
        )

        # === DOCX download with module headers bold ===
        download_path_docx = os.path.join(r"D:\AI_MID_Project_Data\api_downloads", "Curriculum_Plan.docx")
        doc = Document()
        for mod in modules:
            if mod.strip():
                header_match = re.match(r"\*\*(Module \d+.*?)\*\*", mod)
                header = header_match.group(1) if header_match else "Module"
                body = mod.replace(f"**{header}**", "").strip()
                doc.add_paragraph(header, style='Heading2')
                doc.add_paragraph(body)
        doc.save(download_path_docx)

        st.download_button(
            label="📥 Download Curriculum Plan (DOCX)",
            data=open(download_path_docx, "rb").read(),
            file_name="Curriculum_Plan.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
