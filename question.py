import streamlit as st

# Title
st.title("🧠 Smart Interview Question Generator")

# Input: Project folder or Python file path
project_path = st.text_input(
    "📂 Enter project folder or Python file path",
    key="project_path_input"
)

# Input: Number of questions to generate
num_questions = st.number_input(
    "Enter number of questions to generate",
    min_value=1,
    max_value=50,
    value=5,
    key="num_questions_input"
)

# Button to generate questions
if st.button("Generate Questions", key="generate_button"):
    # Placeholder for your question generation logic
    st.write(f"Generating {num_questions} questions for: {project_path}")

# Optional: Add more widgets below, but always give them a unique 'key'
# Example:
# another_input = st.text_input("Another input", key="another_input_key")
