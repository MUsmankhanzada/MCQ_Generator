import os
import json
import re
import traceback
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from src.mcq_generator.logger import logging

#imporing necessary packages packages from langchain
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain_core.utils import get_from_dict_or_env

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables just like you would with os.environ
key=os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama3-8b-8192",
    api_key=key,
    temperature=0.3,  # Lower temperature for consistent, factual responses
    max_tokens=2048,  # Higher limit for detailed MCQ explanations
    stop_sequences=["\n\nQuestion:", "\n\n---", "\n\n###"]  # Stop at question boundaries
)

llm_json_fixer = ChatGroq(
    model="llama3-70b-8192",
    api_key=key,
    temperature=0,
    max_tokens=4096,
    stop_sequences=[]
)

TEMPLATE = """
# MCQ Generation Instructions

## Input Text
{text}

## Task Description
You are an expert MCQ maker. Given the above text, it is your job to create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.

## Requirements
1. **Question Count**: Generate exactly {number} MCQs
2. **Uniqueness**: Ensure no questions are repeated
3. **Accuracy**: All questions must conform to the provided text content
4. **Format**: Follow the RESPONSE_JSON structure below exactly

## Response Format
Please format your response using the following JSON structure as a guide:

### RESPONSE_JSON
{response_json}

## Instructions
- Create clear, well-structured multiple choice questions
- Ensure all options are plausible and relevant
- Provide accurate explanations for correct answers
- Maintain consistency with the specified tone and subject level
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
    )

quiz_chain=LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)


TEMPLATE2 = """
# Quiz Review and Analysis Instructions

## Input Quiz
{quiz}

## Task Description
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students, you need to evaluate the complexity of the questions and provide a complete analysis of the quiz.

## Review Requirements
1. **Complexity Analysis**: Evaluate if questions match student cognitive abilities (max 50 words)
2. **Quality Assessment**: Check grammar, clarity, and educational value
3. **Difficulty Evaluation**: Assess if questions are appropriate for student level
4. **Tone Analysis**: Evaluate if tone fits student abilities
5. **Content Validation**: Ensure questions are appropriate for {subject} students

## Analysis Guidelines
- **Cognitive Level**: Assess if questions are too easy, too hard, or just right
- **Language Complexity**: Check vocabulary and sentence structure
- **Question Clarity**: Evaluate if questions are unambiguous and well-written
- **Option Quality**: Verify if distractors are plausible but clearly incorrect
- **Educational Value**: Confirm if questions promote learning and understanding

## Output Format
Provide your analysis in the following structure:

### COMPLEXITY ANALYSIS
[Your 50-word complexity assessment]

### QUALITY ASSESSMENT
[Grammar, clarity, and educational value review]

### DIFFICULTY EVALUATION
[Assessment of question difficulty relative to student level]

### TONE ANALYSIS
[Evaluation of language and tone appropriateness]

### CONTENT VALIDATION
[Assessment of subject matter appropriateness and educational value]

### OVERALL RECOMMENDATIONS
[Summary of findings and general recommendations for improvement]

## Instructions
- Be thorough but concise in your analysis
- Focus on educational appropriateness and student engagement
- Provide constructive feedback without making direct corrections
- Identify areas that need improvement while maintaining objectivity
"""


quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE2)

review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

TEMPLATE_fix_json = """
You will receive a string that is meant to be JSON but may contain syntax errors like:
- Missing commas, quotes, or brackets
- Trailing commas or unbalanced braces
- Wrongly escaped characters

Your task:
✅ Repair the string into valid JSON.  
✅ Return only **valid JSON output** with no surrounding text or formatting.  
✅ Do **not** wrap the JSON in markdown code fences (```), text like "Here is the JSON:", or any explanation.  
✅ Output only raw JSON.  

Here is the broken JSON string:
{quiz}
"""
fix_json_prompt = PromptTemplate(
    input_variables=["quiz"],
    template= TEMPLATE_fix_json 
)

fix_json_chain = LLMChain(
    llm=llm_json_fixer,
    prompt=fix_json_prompt,
    output_key="fixed_quiz",
    verbose=True
)

generate_evaluate_chain=SequentialChain(
    chains=[quiz_chain, review_chain, fix_json_chain],
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review", "fixed_quiz"],
    verbose=False
)








