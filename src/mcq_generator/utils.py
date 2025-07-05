import os
import re
import PyPDF2
import json
import pandas as pd
from datetime import datetime
import streamlit as st

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfFileReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
            
        except Exception as e:
            raise Exception("error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file suppoted"
        )

import streamlit as st

def run_quiz_app(quiz_data):
    st.title(quiz_data["quiz_info"]["title"])
    st.subheader(f"Subject: {quiz_data['quiz_info']['subject']}")
    st.markdown(f"**Difficulty:** {quiz_data['quiz_info']['difficulty'].capitalize()}")
    st.markdown(f"**Total Questions:** {quiz_data['quiz_info']['total_questions']}")

    st.markdown("---")

    # Session state to track current question and score
    if "current_q" not in st.session_state:
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answers = []

    questions = quiz_data["questions"]
    total_questions = len(questions)

    # Current Question
    q = questions[st.session_state.current_q]
    st.write(f"### Question {q['id']}: {q['question']}")
    selected_option = st.radio(
        "Choose an option:",
        list(q["options"].items()),
        format_func=lambda x: f"{x[0]}) {x[1]}"
    )

    if st.button("Submit Answer"):
        selected_key = selected_option[0]
        st.session_state.answers.append((q["id"], selected_key))

        if selected_key == q["correct_answer"]:
            st.session_state.score += 1
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect! The correct answer was **{q['correct_answer']}**.")
        
        st.info(f"📖 Explanation: {q['explanation']}")

        if st.session_state.current_q < total_questions - 1:
            st.session_state.current_q += 1
            st.button("Next Question", key="next")
        else:
            st.markdown("---")
            st.success(f"🎉 Quiz Completed! Your score: **{st.session_state.score}/{total_questions}**")
            st.button("Restart Quiz", on_click=restart_quiz)

def restart_quiz():
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.answers = []



def save_mcqs_to_csv(json_string, filename=None):
    """
    Save quiz data (quiz_info + questions) from a JSON string to CSV files.

    Parameters:
    - json_string (str): The quiz data as a JSON string.
    - filename (str, optional): The base filename for CSVs. If not provided, generates one.

    Returns:
    - tuple: Filenames of the saved CSV files (quiz_info_file, questions_file).
    """
    try:
        # Parse JSON string
        quiz_data = json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON string: {e}")
        return

    if not quiz_data or 'questions' not in quiz_data:
        print("❌ No quiz data to save")
        return

    # Create DataFrames
    quiz_info_df = pd.DataFrame([quiz_data.get("quiz_info", {})])
    questions_df = pd.DataFrame(quiz_data["questions"])

    # Generate base filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        subject = quiz_data.get('quiz_info', {}).get('subject', 'quiz').replace(' ', '_').lower()
        filename_base = f"{subject}_mcqs_{timestamp}"
    else:
        filename_base = filename.replace('.csv', '')  # Remove .csv if passed

    # Create filenames for quiz_info and questions
    quiz_info_file = f"{filename_base}_info.csv"
    questions_file = f"{filename_base}_questions.csv"

    # Save to CSV
    quiz_info_df.to_csv(quiz_info_file, index=False, encoding="utf-8")
    questions_df.to_csv(questions_file, index=False, encoding="utf-8")

    print(f"✅ Quiz Info saved to: {quiz_info_file}")
    print(f"✅ Questions saved to: {questions_file}")
    print(f"📊 Total questions saved: {len(questions_df)}")

    return quiz_info_file, questions_file
