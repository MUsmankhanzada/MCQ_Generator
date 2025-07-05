import os
import json
import re
import traceback
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file,save_mcqs_to_csv,run_quiz_app
import streamlit as st
from src.mcq_generator.logger import logging
from src.mcq_generator.MCQgenerator import generate_evaluate_chain

#loading json file
with open("Response.json","r") as f:
    RESPONSE_JSON = json.load(f)

st.title("MCQ Generator using Langchain")

# Initialize session state for quiz data
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "show_quiz" not in st.session_state:
    st.session_state.show_quiz = False

# MCQ Generation Form
with st.form("upload_file"):
    #upload the file
    upload_file = st.file_uploader("Upload a PDF or Text file")
    
    #INPUT Fields
    mcq_count = st.number_input("Number of MCQs to generate", min_value = 3 , max_value = 20)	
    #subject
    subject = st.text_input("Enter the subject of the file", max_chars=20)
    
    #Quiz Difficulty
    tone = st.text_input("Complexity level of the MCQs", max_chars=20,placeholder = 'Simple')
    
    #ADD Button
    button = st.form_submit_button("Generate MCQs")
    
    #Check if the button is clicked and all field have input
    if button and upload_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text = read_file(upload_file)
                response = generate_evaluate_chain({
                    "text":text,
                    "number":mcq_count,
                    "subject":subject,
                    "tone":tone,
                    "response_json":json.dumps(RESPONSE_JSON)
                })
                
                quiz = response["fixed_quiz"]
                if quiz is not None:
                    # Parse the JSON string to get the quiz data
                    try:
                        quiz_data = json.loads(quiz)
                        st.session_state.quiz_data = quiz_data
                        st.session_state.show_quiz = True
                        st.success("MCQs generated successfully! Scroll down to take the quiz.")
                    except json.JSONDecodeError as e:
                        st.error(f"Error parsing quiz data: {e}")
                    
                    save_mcqs_to_csv(quiz)
                    
                    # Display the review in the Streamlit app
                    st.subheader("Quiz Review")
                    st.write(response["review"])
                    
                else:
                    st.error("Error generating quiz")
    
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error generating MCQs")

# Display Quiz Interface (outside the form)
if st.session_state.show_quiz and st.session_state.quiz_data:
    st.markdown("---")
    st.subheader("📝 Take the Generated Quiz")
    
    # Add a button to reset the quiz
    if st.button("Generate New Quiz"):
        st.session_state.quiz_data = None
        st.session_state.show_quiz = False
        st.rerun()
    
    # Run the quiz app
    run_quiz_app(st.session_state.quiz_data)
                    