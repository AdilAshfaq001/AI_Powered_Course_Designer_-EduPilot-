import streamlit as st
from modules.module1_learning_objective_setter import generate_learning_objectives

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_name}. Make sure the 'styles' directory and 'style.css' file exist.")

# --- Apply the custom CSS ---
local_css("HtmlCSS\streamlit.css")

st.set_page_config(layout="wide")
st.title("EduPilot — Module 1: Learning Objectives")

# --- Input Section moved to Sidebar ---
with st.sidebar:
    st.header("⚙️ Course Parameters")
    topic = st.text_input("🎓 Course Topic", value="Web Development")
    level = st.selectbox("🎯 Audience Level", ["Undergraduate_Basic", "Undergraduate_Advanced", "Graduate", "Professional"])
    credit_hours = st.number_input("⏱️ Credit Hours", min_value=1, max_value=6, value=3)
    submitted = st.button("Generate Learning Objectives")

# --- Output Section in Main Area ---
if submitted:
    with st.spinner("🔍 Analyzing trends and generating learning objectives..."):
        objectives, filepath = generate_learning_objectives(topic, level, credit_hours)

        if objectives:
            st.success("✅ Learning Objectives Generated Successfully!")
            st.subheader("🎯 Suggested Learning Objectives")
            # Using st.container to group the output
            with st.container(border=True):
                 for obj in objectives:
                    st.write(f"- {obj}")
            st.info(f"Results saved to: {filepath}")
        else:
            st.error("⚠️ Failed to generate learning objectives.")
else:
    st.info("Enter your course details in the sidebar and click 'Generate Learning Objectives'.")