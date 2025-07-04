import os
import json
import re
import traceback
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file,parse_json_quiz,save_mcqs_to_csv
import streamlit as st
from src.mcq_generator.logger import logging
from src.mcq_generator.MCQgenerator import generate_evaluate_chain

#loading json file
with open("Response.json","r") as f:
    RESPONSE_JSON = json.load(f)

st.title("MCQ Generator using Langchain")
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
                # quiz = response["quiz"]
                # st.write("Raw quiz output:", quiz)
    
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")
                
            else:
                quiz = response["quiz"]
                if quiz is not None:
                    quiz_data = parse_json_quiz(quiz)
                    if quiz_data is not None:
                        save_mcqs_to_csv(quiz_data)
                        st.success("MCQs generated successfully")
                    else:
                        st.error("Error parsing quiz data")
                else:
                    st.error("Error generating quiz")
                    