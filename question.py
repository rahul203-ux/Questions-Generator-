import streamlit as st
import ast
from pathlib import Path

st.set_page_config(page_title="🧠 Smart Interview Question Generator", layout="centered")

st.title("🧠 Smart Interview Question Generator")
st.write("Upload a Python file to generate **code-aware interview questions**.")

# ---------- Question Generator ----------
def generate_questions(code, filename, total_required):
    tree = ast.parse(code)

    functions, classes, variables = [], [], []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    variables.append(t.id)

    project_name = Path(filename).stem.replace("_", " ").title()
    questions = []

    # --- Core project questions ---
    base_questions = [
        f"Explain the {project_name} project in detail.",
        f"What real-world problem does {project_name} solve?",
        f"Who are the intended users of {project_name}?",
        f"Explain the end-to-end workflow of {project_name}.",
        f"What assumptions does {project_name} make?",
        f"What are the limitations of {project_name}?"
    ]
    questions.extend(base_questions)

    # --- Code-aware questions ---
    for f in functions:
        questions.append(f"What does the function '{f}' do in {filename}?")

    for c in classes:
        questions.append(f"Explain the purpose of the class '{c}' in {filename}.")

    for v in variables:
        questions.append(f"What is the role of the variable '{v}' in {filename}?")

    # --- Smart fallback pool (NO DUPLICATES) ---
    fallback = [
        "How does error handling work in this project?",
        "How would you improve performance?",
        "What design patterns are used here?",
        "How would you refactor this code?",
        "How would you add unit tests?",
        "How would you deploy this project?",
        "How would you secure this application?",
        "How would this project scale?",
        "What trade-offs did you make?",
        "How would you improve maintainability?",
        "How would you migrate this project to the cloud?",
        "What challenges did you face while building this?",
        "What would you improve if given more time?",
        "How does data flow through the application?"
    ]

    # --- Ensure EXACT number ---
    i = 0
    while len(questions) < total_required:
        questions.append(fallback[i % len(fallback)])
        i += 1

    return questions[:total_required]

# ---------- UI ----------
uploaded_file = st.file_uploader(
    "📂 Upload your Python file",
    type=["py"],
    help="Upload a .py file (Max 200MB)"
)

num_questions = st.number_input(
    "Enter number of questions to generate",
    min_value=1,
    max_value=100,
    value=20
)

# ---------- Button Action ----------
if uploaded_file and st.button("Generate Questions"):
    try:
        code = uploaded_file.read().decode("utf-8")
        questions = generate_questions(
            code,
            uploaded_file.name,
            num_questions
        )

        st.success(f"✅ {len(questions)} Questions Generated")

        for i, q in enumerate(questions, 1):
            st.write(f"**{i}.** {q}")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
