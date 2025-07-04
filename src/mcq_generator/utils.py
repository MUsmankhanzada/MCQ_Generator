import os
import re
import PyPDF2
import json
import pandas as pd
from datetime import datetime

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
        
import re
import json

import re
import json
import json

def parse_json_quiz(quiz_text):
    """Extract and parse the first JSON object from the LLM output, even if pretty-printed and surrounded by text."""
    try:
        # Find the first '{' and parse until the matching '}'
        start = quiz_text.find('{')
        if start == -1:
            print("Could not find JSON object in the text!")
            return None

        # Use a stack to find the matching closing brace
        stack = []
        for i, char in enumerate(quiz_text[start:]):
            if char == '{':
                stack.append('{')
            elif char == '}':
                stack.pop()
                if not stack:
                    end = start + i + 1
                    break
        else:
            print("Could not find matching closing brace for JSON object!")
            return None

        json_str = quiz_text[start:end]

        # Parse JSON
        quiz_data = json.loads(json_str)
        return quiz_data
    except Exception as e:
        print("Error parsing quiz JSON:", e)
        print("Quiz string that failed to parse:", repr(json_str))
        return None
    
def save_mcqs_to_csv(quiz_data, filename=None):
    """Save MCQs to CSV format"""
    if not quiz_data or 'questions' not in quiz_data:
        print("No quiz data to save")
        return
    
    # Create rows for CSV
    rows = []
    for question in quiz_data['questions']:
        row = {
            'Question_Number': question.get('id', ''),
            'Question': question.get('question', ''),
            'Option_A': question.get('options', {}).get('A', ''),
            'Option_B': question.get('options', {}).get('B', ''),
            'Option_C': question.get('options', {}).get('C', ''),
            'Option_D': question.get('options', {}).get('D', ''),
            'Correct_Answer': question.get('correct_answer', ''),
            'Explanation': question.get('explanation', '')
        }
        rows.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(rows)
    
    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        subject = quiz_data.get('quiz_info', {}).get('subject', 'quiz').replace(' ', '_').lower()
        filename = f"{subject}_mcqs_{timestamp}.csv"
    
    # Save to CSV
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"✅ MCQs saved to CSV: {filename}")
    print(f"📊 Total questions saved: {len(rows)}")
    
    return filename