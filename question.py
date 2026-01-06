import ast
from pathlib import Path
import streamlit as st

# -----------------------------
# Clean path input (Windows safe)
# -----------------------------
def clean_path(path):
    return path.strip().strip('"').strip("'")

# -----------------------------
# Analyze Python code
# -----------------------------
def analyze_python_file(file_path):
    """Extract functions, classes, and imports from a Python file."""
    functions, classes, imports = [], [], []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.Import):
                for n in node.names:
                    imports.append(n.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module if node.module else ""
                for n in node.names:
                    imports.append(f"{module}.{n.name}" if module else n.name)

    except Exception as e:
        st.error(f"⚠️ Could not analyze file: {e}")

    return functions, classes, imports

# -----------------------------
# Generate interview questions
# -----------------------------
def generate_questions(file_path):
    functions, classes, imports = analyze_python_file(file_path)
    project_name = Path(file_path).stem.replace("_", " ").title()
    questions = []

    # Generic project questions
    questions.extend([
        f"Explain the {project_name} project in detail.",
        f"What real-world problem does {project_name} solve?",
        f"Who are the intended users of {project_name}?",
    ])

    # Questions for classes
    for cls in classes:
        questions.append(f"Explain the purpose of the class `{cls}` in {project_name}.")
        questions.append(f"Which methods are implemented in `{cls}` and what do they do?")
        questions.append(f"How would you test the `{cls}` class?")

    # Questions for functions
    for func in functions:
        questions.append(f"What does the function `{func}()` do?")
        questions.append(f"How would you test the `{func}()` function?")
        questions.append(f"Where is `{func}()` used in the project?")

    # Questions for imports / dependencies
    for imp in imports:
        questions.append(f"Why is `{imp}` imported in this project?")
        questions.append(f"How does `{imp}` help in the project?")

    # Fallback questions if total < 50
    fallback = [
        "Explain the overall workflow of the project.",
        "What are potential performance bottlenecks?",
        "How would you optimize this project?",
        "What are the security risks?",
        "How would you improve maintainability?",
    ]
    while len(questions) < 50:
        questions.extend(fallback)

    return questions[:50]

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="Smart Interview Question Generator", layout="wide")

st.title("🧠 Smart Interview Question Generator")
st.write("Generate *project-specific interview questions* automatically from your Python code.")

# Input: Python file path
project_path = st.text_input(
    "📂 Enter Python file path",
    key="project_path_input"
)

# Input: Number of questions
num_questions = st.number_input(
    "Enter number of questions to generate",
    min_value=1, max_value=50,
    value=10,
    key="num_questions_input"
)

# Generate questions button
if st.button("Generate Questions", key="generate_button"):
    project_path = clean_path(project_path)

    if not project_path:
        st.warning("⚠️ Please enter a valid Python file path")
    else:
        questions = generate_questions(project_path)
        st.success(f"✅ {len(questions)} Questions Generated")

        for i, q in enumerate(questions[:num_questions], 1):
            st.write(f"*{i}.* {q}")
