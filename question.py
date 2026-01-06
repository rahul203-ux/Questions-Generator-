import streamlit as st
import ast
from pathlib import Path
from collections import Counter

# ---------------------------------
# QUESTION GENERATOR (CORE LOGIC)
# ---------------------------------
def generate_questions(code, filename):
    tree = ast.parse(code)

    functions, classes, variables = [], [], []
    imports, loops, conditionals = [], 0, 0

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    variables.append(t.id)

        elif isinstance(node, (ast.For, ast.While)):
            loops += 1

        elif isinstance(node, ast.If):
            conditionals += 1

        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for n in node.names:
                imports.append(n.name)

    project_name = Path(filename).stem.replace("_", " ").title()

    questions = []
    used = set()

    def add(q):
        if q not in used:
            questions.append(q)
            used.add(q)

    # -------- Project understanding (code-based) --------
    add(f"Explain the main purpose of the {project_name} codebase.")
    add(f"Describe the execution flow starting from the entry point in {filename}.")

    # -------- Functions --------
    for f in functions:
        add(f"What logic is implemented inside the function '{f}'?")
        add(f"How does the function '{f}' interact with other parts of the code?")

    # -------- Classes --------
    for c in classes:
        add(f"What responsibility does the class '{c}' handle?")
        add(f"How is the class '{c}' instantiated and used?")

    # -------- Variable importance --------
    var_rank = Counter(variables).most_common(10)
    for v, _ in var_rank:
        add(f"Why is the variable '{v}' critical to the program’s behavior?")
        add(f"What would break if '{v}' were modified or removed?")

    # -------- Control flow --------
    if loops:
        add("How do loops affect data processing in this code?")
        add("What would change if loop conditions were altered?")

    if conditionals:
        add("How do conditional statements control decision-making?")
        add("Which conditions are most critical for correctness?")

    # -------- ML / AI detection --------
    ml_keywords = {
        "model", "vectorizer", "fit", "predict", "transform",
        "train", "x", "y", "labels", "classifier", "regressor"
    }

    if any(v.lower() in ml_keywords for v in variables) or any(
        lib in imports for lib in ["sklearn", "torch", "tensorflow"]
    ):
        add("Explain the machine learning pipeline implemented in this code.")
        add("How is training data prepared before model training?")
        add("How does the model generate predictions?")
        add("How would you evaluate the model’s performance?")
        add("What risks of overfitting exist in this implementation?")
        add("How would you improve model generalization?")

    # -------- NLP detection --------
    if "text" in variables or "texts" in variables:
        add("How is text data preprocessed in this code?")
        add("Which NLP techniques are implicitly used?")
        add("How could feature extraction be improved?")

    return questions


# ---------------------------------
# STREAMLIT UI
# ---------------------------------
st.set_page_config(
    page_title="Smart Interview Question Generator",
    layout="wide"
)

st.title("🧠 Smart Interview Question Generator")
st.write("Upload a Python file to generate **smart, code-aware interview questions**.")

uploaded_file = st.file_uploader(
    "📂 Upload your Python file",
    type=["py"]
)

if uploaded_file and st.button("Generate Questions"):
    try:
        code = uploaded_file.read().decode("utf-8")

        questions = generate_questions(
            code,
            uploaded_file.name
        )

        st.success(f"✅ {len(questions)} Questions Generated")

        for i, q in enumerate(questions, 1):
            st.write(f"**{i}.** {q}")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
