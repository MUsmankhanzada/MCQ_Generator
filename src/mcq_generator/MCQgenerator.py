import os
import json
import re
import traceback
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file
from src.mcq_generator.logger import logging

#imporing necessary packages packages from langchain
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables just like you would with os.environ
key=os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama3-8b-8192",
    groq_api_key=key,
    temperature=0.3,  # Lower temperature for consistent, factual responses
    max_tokens=2048,  # Higher limit for detailed MCQ explanations
    top_p=0.8,       # Slightly lower for more focused responses
    stop=["\n\nQuestion:", "\n\n---", "\n\n###"]  # Stop at question boundaries
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
# Quiz Review and Enhancement Instructions

## Input Quiz
{quiz}

## Task Description
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students, you need to evaluate the complexity of the questions and provide a complete analysis of the quiz.

## Review Requirements
1. **Complexity Analysis**: Evaluate if questions match student cognitive abilities (max 50 words)
2. **Quality Assessment**: Check grammar, clarity, and educational value
3. **Difficulty Adjustment**: Update questions that don't match student level
4. **Tone Optimization**: Adjust tone to perfectly fit student abilities
5. **Content Validation**: Ensure questions are appropriate for {subject} students

## Analysis Guidelines
- **Cognitive Level**: Assess if questions are too easy, too hard, or just right
- **Language Complexity**: Check vocabulary and sentence structure
- **Question Clarity**: Ensure questions are unambiguous and well-written
- **Option Quality**: Verify distractors are plausible but clearly incorrect
- **Educational Value**: Confirm questions promote learning and understanding

## Enhancement Instructions
- If questions are too complex: Simplify language and reduce difficulty
- If questions are too simple: Increase complexity and add analytical elements
- If tone is inappropriate: Adjust to match student age and subject level
- If grammar is poor: Correct all grammatical and punctuation errors
- If explanations are unclear: Improve clarity and educational value

## Output Format
Provide your analysis and any necessary updates in the following structure:

### COMPLEXITY ANALYSIS
[Your 50-word complexity assessment]

### QUALITY ASSESSMENT
[Grammar, clarity, and educational value review]

### ENHANCED QUIZ
[Updated quiz with improved questions, tone, and difficulty level]

### CHANGES MADE
[List of specific improvements and modifications]

## Instructions
- Be thorough but concise in your analysis
- Focus on educational appropriateness and student engagement
- Maintain the original quiz structure while improving quality
- Ensure all changes enhance learning outcomes
"""

quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE2)

review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True,)








