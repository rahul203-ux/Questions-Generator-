import streamlit as st
import ast
from pathlib import Path

st.set_page_config(page_title="Smart Interview Question Generator", layout="wide")

st.title("🧠 Smart Interview Question Generator")
st.write("Upload a Python file to generate code-aware interview questions.")

# ✅ ALWAYS VISIBLE
uploaded_file = st.file_uploader(
    "📂 Upload your Python file",
    type=["py"],
    key="file_uploader"
)

num_questions = st.number_input(
    "Enter number of questions to generate",
    min_value=1,
    max_value=50,
    value=10,
    key="num_questions"
)

def analyze_code(code):
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

    return functions, classes, variables

if uploaded_file and st.button("Generate Questions"):
    code = uploaded_file.read().decode("utf-8")
    project_name = Path(uploaded_file.name).stem.title()

    funcs, classes, vars_ = analyze_code(code)

    questions = [
        f"Explain the {project_name} project in detail.",
        f"What real-world problem does {project_name} solve?",
        f"Who are the intended users of {project_name}?"
    ]

    for f in funcs:
        questions.append(f"What does the function '{f}' do?")
    for c in classes:
        questions.append(f"Explain the purpose of the class '{c}'.")
    for v in vars_:
        questions.append(f"What is the role of the variable '{v}'?")

    st.success(f"✅ {len(questions[:num_questions])} Questions Generated")

    for i, q in enumerate(questions[:num_questions], 1):
        st.write(f"**{i}.** {q}")
