import os
import json
import traceback
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file, save_mcqs_to_csv
import streamlit as st
from src.mcq_generator.logger import logging
from src.mcq_generator.MCQgenerator import generate_evaluate_chain

# Load environment variables
load_dotenv()

# Load response JSON
with open("Response.json", "r") as f:
    RESPONSE_JSON = json.load(f)

# App Title
st.title("🎯 MCQ Generator & Interactive Quiz App")

# Initialize session state
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "show_quiz" not in st.session_state:
    st.session_state.show_quiz = False
if "quiz_review" not in st.session_state:
    st.session_state.quiz_review = None
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

# Tabs for clean UI
tab1, tab2 = st.tabs(["📄 MCQ Generator", "📊 Review & Take Quiz"])

# ==========================
# TAB 1: MCQ Generator
# ==========================
with tab1:
    st.header("📄 Generate MCQs from Your File")
    st.markdown("Upload a PDF or text file and configure options to generate MCQs.")

    with st.form("upload_file"):
        # Upload the file
        upload_file = st.file_uploader("Upload a PDF or Text file")

        # INPUT Fields
        mcq_count = st.slider("Number of MCQs to generate", min_value=3, max_value=20, value=5)
        subject = st.text_input("Enter the subject", max_chars=30, placeholder="e.g. Computer Vision")
        tone = st.selectbox("Select complexity level", ["Simple", "Moderate", "Complex"], index=0)

        # Submit button
        button = st.form_submit_button("🚀 Generate MCQs")

        if button and upload_file and mcq_count and subject and tone:
            with st.spinner("⏳ Generating MCQs... This may take a few seconds..."):
                try:
                    text = read_file(upload_file)
                    response = generate_evaluate_chain({
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    })

                    quiz = response["fixed_quiz"]
                    if quiz:
                        try:
                            quiz_data = json.loads(quiz)
                            st.session_state.quiz_data = quiz_data
                            st.session_state.show_quiz = True
                            st.session_state.quiz_review = response["review"]
                            st.session_state.user_answers = {}  # reset answers
                            st.session_state.quiz_submitted = False  # reset submission

                            st.success("✅ MCQs generated successfully! Saved as CSV.")
                            save_mcqs_to_csv(quiz)

                            # Debug raw review
                            with st.expander("🔍 Debug: Raw Review Output"):
                                st.code(response["review"], language="text")

                        except json.JSONDecodeError as e:
                            st.error(f"❌ Error parsing quiz data: {e}")

                    else:
                        st.error("⚠️ Error generating quiz.")

                except Exception as e:
                    traceback.print_exception(type(e), e, e.__traceback__)
                    st.error("❌ An error occurred while generating MCQs.")

# ==========================
# TAB 2: Review & Take Quiz
# ==========================
with tab2:
    st.header("📊 Review Analysis & Take Quiz")

    # Display Quiz Review
    if st.session_state.quiz_review:
        st.subheader("📝 Quiz Analysis")

        # Format and display review nicely
        formatted_review = st.session_state.quiz_review.replace("\n", "\n\n")

        for section in formatted_review.split("\n\n"):
            if section.strip():
                title_line = section.split("\n")[0]  # First line as title
                body = "\n".join(section.split("\n")[1:])  # Rest as body
                st.markdown(f"""
<div style="background-color:#f0f2f6;padding:15px;border-radius:10px;margin-bottom:10px;">
    <h5 style="color:#0f62fe">{title_line.strip('**')}</h5>
    <p>{body}</p>
</div>
""", unsafe_allow_html=True)

    else:
        st.info("ℹ️ No analysis available. Please generate a quiz in the 'MCQ Generator' tab.")

    # Display Quiz
    if st.session_state.show_quiz and st.session_state.quiz_data:
        st.markdown("---")
        st.subheader("📝 Take the Generated Quiz")

        # Reset button
        if st.button("🔄 Generate New Quiz"):
            st.session_state.quiz_data = None
            st.session_state.show_quiz = False
            st.session_state.quiz_review = None
            st.session_state.user_answers = {}
            st.session_state.quiz_submitted = False
            st.rerun()

        # Display questions as cards
        if 'questions' in st.session_state.quiz_data:
            for q in st.session_state.quiz_data['questions']:
                question_key = f"q_{q['id']}"
                user_choice = st.radio(
                    f"❓ Q{q['id']}: {q['question']}",
                    [f"{key}. {value}" for key, value in q['options'].items()],
                    key=question_key
                )
                st.session_state.user_answers[q['id']] = user_choice[0]  # Save chosen option (A/B/C/D)

            # Submit Quiz Button
            if not st.session_state.quiz_submitted:
                if st.button("✅ Submit Quiz"):
                    st.session_state.quiz_submitted = True

            # Show Results if Submitted
            if st.session_state.quiz_submitted:
                st.subheader("📈 Quiz Results")
                correct = 0
                total = len(st.session_state.quiz_data['questions'])
                for q in st.session_state.quiz_data['questions']:
                    user_ans = st.session_state.user_answers.get(q['id'])
                    correct_ans = q['correct_answer']
                    explanation = q['explanation']

                    if user_ans == correct_ans:
                        correct += 1
                        st.success(f"✅ Q{q['id']} Correct! ({correct_ans})")
                    else:
                        st.error(f"❌ Q{q['id']} Wrong. Correct Answer: {correct_ans}")

                    st.markdown(f"**💡 Explanation:** {explanation}")

                st.markdown(f"### 🏆 Your Score: {correct} / {total}")

        else:
            st.warning("⚠️ No questions found in the quiz data.")
    else:
        st.info("ℹ️ No quiz available. Please generate one in the 'MCQ Generator' tab.")
