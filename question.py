import os
import streamlit as st
from pathlib import Path

# ---------------------------------
# Clean path input (Windows safe)
# ---------------------------------
def clean_path(path):
    return path.strip().strip('"').strip("'")

# ---------------------------------
# Get project name safely
# ---------------------------------
def get_project_name(project_path):
    try:
        return Path(project_path).stem.replace("_", " ").title()
    except:
        return "The Project"

# ---------------------------------
# MAIN QUESTION GENERATOR (ONLY ONE)
# ---------------------------------
def generate_questions(project_path):
    project_name = get_project_name(project_path)

    questions = []

    # ---- PROJECT UNDERSTANDING ----
    questions.extend([
        f"Explain the {project_name} project in detail.",
        f"What real-world problem does {project_name} solve?",
        f"Why did you decide to build {project_name}?",
        f"Who are the intended users of {project_name}?",
        f"Explain the end-to-end workflow of {project_name}.",
        f"What assumptions does {project_name} make?",
        f"What are the limitations of {project_name}?",
        f"If you had more time, what would you improve first?",
    ])

    # ---- ARCHITECTURE & DESIGN ----
    questions.extend([
        "Describe the overall architecture of the project.",
        "Why did you choose this project structure?",
        "How does data flow through the application?",
        "What design principles did you follow?",
        "How do different modules interact?",
        "How would you refactor this project for scalability?",
    ])

    # ---- IMPLEMENTATION ----
    questions.extend([
        "Which technologies and libraries did you use and why?",
        "Which part of the code was most challenging?",
        "How do you manage configuration and constants?",
        "How does the project handle invalid inputs?",
        "How does error handling work in this project?",
    ])

    # ---- PERFORMANCE & SECURITY ----
    questions.extend([
        "What are potential performance bottlenecks?",
        "How would you optimize this project?",
        "How does the project behave with large inputs?",
        "What security risks exist in this project?",
        "How would you secure user inputs?",
    ])

    # ---- TESTING ----
    questions.extend([
        "How would you write unit tests for this project?",
        "Which components are most critical to test?",
        "How would you mock external dependencies?",
        "Which testing framework would you use?",
        "How would you ensure good test coverage?",
    ])

    # ---- DEPLOYMENT ----
    questions.extend([
        "How would you deploy this project in production?",
        "What environment variables are required?",
        "How would you containerize this project using Docker?",
        "How would this project scale with many users?",
        "What logging and monitoring would you add?",
    ])

    # ---- FUTURE & PRODUCT ----
    questions.extend([
        "What future features can be added?",
        "How would you convert this into a SaaS product?",
        "How would you add AI automation?",
        "How would you improve user experience?",
        "How would you make this project enterprise-ready?",
    ])

    # ---- GUARANTEED 40–50 QUESTIONS ----
    fallback = [
        "Explain the full execution flow of the project.",
        "Why is this project interview-ready?",
        "What trade-offs did you make?",
        "How would you improve maintainability?",
        "How would you migrate this project to the cloud?",
    ]

    while len(questions) < 50:
        questions.extend(fallback)

    return questions[:50]

# ---------------------------------
# STREAMLIT UI
# ---------------------------------
st.set_page_config(page_title="Smart Interview Question Generator", layout="wide")

st.title("🧠 Smart Interview Question Generator")
st.write("Generate **project-specific interview questions** automatically.")

project_path = st.text_input("📂 Enter project folder or Python file path")

if st.button("Generate Questions"):
    project_path = clean_path(project_path)

    if not project_path:
        st.warning("⚠️ Please enter a project path")
    else:
        questions = generate_questions(project_path)

        st.success(f"✅ {len(questions)} Questions Generated")

        for i, q in enumerate(questions, 1):
            st.write(f"**{i}.** {q}")
