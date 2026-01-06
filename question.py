import os
import ast
from pathlib import Path
import streamlit as st

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
# Analyze Python file
# ---------------------------------
def analyze_file(file_path):
    """Parse a Python file and return functions, classes, variables, imports."""
    functions = []
    classes = []
    variables = []
    imports = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variables.append(target.id)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")

    except Exception as e:
        st.warning(f"⚠️ Could not analyze file {file_path}: {e}")

    return {"functions": functions, "classes": classes, "variables": variables, "imports": imports}

# ---------------------------------
# Generate questions
# ---------------------------------
def generate_questions(project_path):
    project_path = Path(project_path)
    project_name = get_project_name(project_path)
    questions = []

    # ---- GENERIC PROJECT QUESTIONS ----
    questions.extend([
        f"Explain the {project_name} project in detail.",
        f"What real-world problem does {project_name} solve?",
        f"Why did you decide to build {project_name}?",
        f"Who are the intended users of {project_name}?",
        f"Explain the end-to-end workflow of {project_name}.",
        f"What assumptions does {project_name} make?",
        f"What are the limitations of {project_name}?"
    ])

    # ---- CODE-AWARE QUESTIONS ----
    python_files = []
    if project_path.is_file() and project_path.suffix == ".py":
        python_files.append(project_path)
    elif project_path.is_dir():
        python_files.extend(project_path.rglob("*.py"))

    for py_file in python_files:
        elements = analyze_file(py_file)
        file_name = py_file.name

        for fn in elements["functions"]:
            questions.append(f"What does the function '{fn}' do in {file_name}?")
        for cls in elements["classes"]:
            questions.append(f"Explain the purpose of the class '{cls}' in {file_name}.")
        for var in elements["variables"]:
            questions.append(f"What is the role of the variable '{var}' in {file_name}?")
        for imp in elements["imports"]:
            questions.append(f"Why is '{imp}' imported in {file_name}?")

    # ---- FALLBACK QUESTIONS ----
    fallback = [
        "Explain the full execution flow of the project.",
        "Why is this project interview-ready?",
        "What trade-offs did you make?",
        "How would you improve maintainability?",
        "How would you migrate this project to the cloud?"
    ]
    while len(questions) < 50:
        questions.extend(fallback)

    return questions[:50]

# ---------------------------------
# STREAMLIT UI
# ---------------------------------
st.set_page_config(page_title="Smart Interview Question Generator", layout="wide")
st.title("🧠 Smart Interview Question Generator")
st.write("Generate *project-specific and code-aware interview questions* automatically.")

project_path_input = st.text_input(
    "📂 Enter project folder or Python file path",
    key="project_path_input"
)

num_questions = st.number_input(
    "Enter number of questions to generate",
    min_value=1,
    max_value=50,
    value=5,
    key="num_questions_input"
)

if st.button("Generate Questions", key="generate_button"):
    project_path_input = clean_path(project_path_input)

    if not project_path_input:
        st.warning("⚠️ Please enter a project path")
    else:
        questions = generate_questions(project_path_input)
        st.success(f"✅ {len(questions)} Questions Generated")

        for i, q in enumerate(questions[:num_questions], 1):
            st.write(f"*{i}.* {q}")
