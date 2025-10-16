import streamlit as st
from modules.module1_learning_objective_setter import generate_learning_objectives

st.title("EduDesign AI — Module 1: Learning Objectives (Gemini Powered)")

with st.form("input_form"):
    topic = st.text_input("🎓 Course Topic", value="Web Development")
    level = st.selectbox("🎯 Audience Level", ["Undergraduate_Basic", "Undergraduate_Advanced", "Graduate", "Professional"])
    credit_hours = st.number_input("⏱️ Credit Hours", min_value=1, max_value=6, value=3)
    submitted = st.form_submit_button("Generate Learning Objectives")

if submitted:
    with st.spinner("🔍 Analyzing trends and generating learning objectives using Gemini AI..."):
        objectives, filepath = generate_learning_objectives(topic, level, credit_hours)

        if objectives:
            st.success("✅ Learning Objectives Generated Successfully!")
            st.subheader("🎯 Suggested Learning Objectives")
            for obj in objectives:
                st.write(f"- {obj}")
            st.info(f"Results saved to: {filepath}")
        else:
            st.error("⚠️ Failed to generate learning objectives.")
