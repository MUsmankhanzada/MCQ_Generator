import os
import json
import re
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

class GroqJSONFormatter:
    """
    A class to format and clean malformed JSON responses using Groq models
    """
    
    def __init__(self, api_key: str, model: str = "llama3.1-8b-8192"):
        """
        Initialize the JSON formatter with Groq
        
        Args:
            api_key: Groq API key
            model: Groq model name (recommended: llama3.1-8b-8192)
        """
        self.api_key = api_key
        self.model = model
        self.llm = self._initialize_groq_llm()
        
    def _initialize_groq_llm(self):
        """Initialize the Groq LLM for JSON formatting"""
        try:
            return ChatGroq(
                model=self.model,
                api_key=self.api_key,
                temperature=0.1,  # Very low temperature for consistent formatting
                max_tokens=4096,  # Higher limit for complex JSON
                stop_sequences=["```", "END_JSON", "JSON_END", "\n\n---"]
            )
        except ImportError:
            print("Error: langchain_groq not available. Please install: pip install langchain-groq")
            return None
    
    def get_json_formatting_prompt(self) -> str:
        """
        Create the prompt template for JSON formatting with Groq
        """
        return """
You are a JSON formatting expert. Your ONLY task is to convert malformed JSON into valid, properly formatted JSON.

INPUT: A malformed JSON string that may contain formatting issues.

TASK: Convert the input into valid JSON following these strict rules:
1. All keys must be in double quotes: "key"
2. All string values must be in double quotes: "value"
3. No trailing commas before closing braces/brackets
4. Proper nesting and indentation
5. Valid JSON structure

OUTPUT FORMAT: Return ONLY the valid JSON object, no additional text, no markdown formatting.

CRITICAL RULES:
- Start with { and end with }
- All strings in double quotes
- No trailing commas
- No comments or explanations
- No markdown code blocks
- No extra text before or after JSON

EXAMPLE INPUT:
{
"quiz_info": {
"title": "Computer Vision Quiz",
"subject": "Computer Vision",
"difficulty": "easy",
"total_questions": 10
},
"questions": [
{
"id": 1,
"question": "What is the main topic?",
"options": {
"A": "Option A",
"B": "Option B",
"C": "Option C",
"D": "Option D"
},
"correct_answer": "A",
"explanation": "Explanation here"
}
]
}

EXAMPLE OUTPUT:
{"quiz_info":{"title":"Computer Vision Quiz","subject":"Computer Vision","difficulty":"easy","total_questions":10},"questions":[{"id":1,"question":"What is the main topic?","options":{"A":"Option A","B":"Option B","C":"Option C","D":"Option D"},"correct_answer":"A","explanation":"Explanation here"}]}

Now format this JSON:
{input_json}

Return ONLY the valid JSON:
"""

    def clean_json_string(self, json_str: str) -> str:
        """
        Basic cleaning of JSON string before sending to LLM
        """
        # Remove markdown code blocks
        json_str = re.sub(r'```json\s*', '', json_str)
        json_str = re.sub(r'```\s*$', '', json_str)
        
        # Remove extra whitespace at beginning and end
        json_str = json_str.strip()
        
        # Find the first { and last }
        start = json_str.find('{')
        end = json_str.rfind('}')
        
        if start != -1 and end != -1 and end > start:
            json_str = json_str[start:end+1]
        
        return json_str
    
    def format_json_with_groq(self, malformed_json: str) -> Optional[Dict[str, Any]]:
        """
        Use Groq LLM to format malformed JSON
        
        Args:
            malformed_json: The malformed JSON string
            
        Returns:
            Parsed JSON dictionary or None if failed
        """
        if not self.llm:
            print("Groq LLM not available, using fallback method")
            return self._fallback_json_parsing(malformed_json)
        
        try:
            # Clean the input JSON
            cleaned_json = self.clean_json_string(malformed_json)
            
            # Create the prompt
            prompt = self.get_json_formatting_prompt().format(input_json=cleaned_json)
            
            print("🔄 Sending to Groq for JSON formatting...")
            
            # Get response from Groq LLM
            response = self.llm.invoke(prompt)
            formatted_json = str(response.content).strip()
            
            # Try to parse the formatted JSON
            try:
                parsed_json = json.loads(formatted_json)
                print("✅ Successfully formatted JSON with Groq!")
                return parsed_json
            except json.JSONDecodeError as e:
                print(f"❌ Groq formatted JSON still invalid: {e}")
                print(f"Formatted output: {formatted_json[:200]}...")
                return self._fallback_json_parsing(malformed_json)
                
        except Exception as e:
            print(f"❌ Error formatting JSON with Groq: {e}")
            return self._fallback_json_parsing(malformed_json)
    
    def _fallback_json_parsing(self, json_str: str) -> Optional[Dict[str, Any]]:
        """
        Fallback method for JSON parsing when LLM is not available
        """
        try:
            # Basic cleaning
            cleaned = self.clean_json_string(json_str)
            
            # Try to parse directly
            return json.loads(cleaned)
        except json.JSONDecodeError:
            try:
                # Try with regex fixes
                fixed = self._apply_regex_fixes(cleaned)
                return json.loads(fixed)
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON even with fallback: {e}")
                return None
    
    def _apply_regex_fixes(self, json_str: str) -> str:
        """
        Apply regex-based fixes to common JSON issues
        """
        # Fix missing quotes around keys
        json_str = re.sub(r'(\s*)(\w+)(\s*):', r'\1"\2"\3:', json_str)
        
        # Fix missing quotes around string values (but not numbers or booleans)
        json_str = re.sub(r':\s*([^"\d\{\}\[\]\s,]+)(\s*[,}])', r': "\1"\2', json_str)
        
        # Remove trailing commas
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
        
        # Fix newlines in strings
        json_str = re.sub(r'\n', r'\\n', json_str)
        
        return json_str

class JSONCorrector:
    def __init__(self):
        """Initialize the JSON correction model"""
        self.key = os.getenv("GROQ_API_KEY")
        if not self.key:
            print("Warning: GROQ_API_KEY environment variable not found!")
            print("Please set your Groq API key as an environment variable or enter it below:")
            self.key = input("Enter your Groq API key: ")
        
        # Initialize the advanced model for JSON correction
        self.json_correction_llm = ChatGroq(
            model="llama3-70b-8192",  # Using the more advanced model for JSON tasks
            groq_api_key=self.key,
            temperature=0.1,  # Very low temperature for consistent JSON formatting
            max_tokens=4096,  # Higher limit for complex JSON structures
            top_p=0.9,
            top_k=20
        )
        
        # JSON Correction and Formatting Prompt Template
        self.json_correction_prompt = """
You are an expert JSON validator and formatter. Your task is to take a JSON-like structure and convert it into properly formatted, valid JSON.

Input JSON (may contain errors):
{input_json}

Instructions:
1. Fix any JSON syntax errors (missing quotes, commas, brackets, etc.)
2. Ensure all strings are properly quoted
3. Validate the structure and fix any inconsistencies
4. Format the JSON with proper indentation
5. Ensure all required fields are present and properly structured
6. Return ONLY the corrected JSON, no additional text

Expected structure for MCQ JSON:
{{
  "quiz_info": {{
    "title": "string",
    "subject": "string", 
    "difficulty": "string",
    "total_questions": number
  }},
  "questions": [
    {{
      "id": number,
      "question": "string",
      "options": {{
        "A": "string",
        "B": "string", 
        "C": "string",
        "D": "string"
      }},
      "correct_answer": "string (A, B, C, or D)",
      "explanation": "string"
    }}
  ]
}}

Return the corrected JSON:
"""

    def correct_and_format_json(self, input_json_str):
        """Correct and format JSON input to proper JSON structure"""
        try:
            # First, try to parse as JSON to check if it's already valid
            json.loads(input_json_str)
            print("JSON is already valid!")
            return input_json_str
        except json.JSONDecodeError as e:
            print(f"JSON has errors: {e}")
            print("Attempting to correct...")
        
        prompt = self.json_correction_prompt.format(input_json=input_json_str)
        
        try:
            response = self.json_correction_llm.invoke(prompt)
            corrected_json = response.content.strip()
            
            # Validate the corrected JSON
            json.loads(corrected_json)
            print("JSON successfully corrected and formatted!")
            return corrected_json
            
        except Exception as e:
            print(f"Error correcting JSON: {e}")
            return None

    def save_corrected_json(self, corrected_json, filename="corrected_mcqs.json"):
        """Save the corrected JSON to a file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(json.loads(corrected_json), f, indent=2, ensure_ascii=False)
            print(f"Corrected JSON saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving JSON: {e}")
            return False

    def validate_mcq_structure(self, json_data):
        """Validate the MCQ JSON structure"""
        try:
            data = json.loads(json_data) if isinstance(json_data, str) else json_data
            
            # Check required top-level keys
            if 'quiz_info' not in data or 'questions' not in data:
                return False, "Missing required top-level keys: quiz_info or questions"
            
            # Check quiz_info structure
            quiz_info = data['quiz_info']
            required_quiz_fields = ['title', 'subject', 'difficulty', 'total_questions']
            for field in required_quiz_fields:
                if field not in quiz_info:
                    return False, f"Missing required field in quiz_info: {field}"
            
            # Check questions structure
            questions = data['questions']
            if not isinstance(questions, list):
                return False, "Questions must be a list"
            
            for i, question in enumerate(questions):
                required_question_fields = ['id', 'question', 'options', 'correct_answer', 'explanation']
                for field in required_question_fields:
                    if field not in question:
                        return False, f"Missing required field in question {i+1}: {field}"
                
                # Check options structure
                options = question['options']
                if not isinstance(options, dict):
                    return False, f"Options in question {i+1} must be a dictionary"
                
                required_options = ['A', 'B', 'C', 'D']
                for option in required_options:
                    if option not in options:
                        return False, f"Missing option {option} in question {i+1}"
            
            return True, "JSON structure is valid"
            
        except Exception as e:
            return False, f"Validation error: {e}"

def process_quiz_response(quiz_response: str, api_key: str, model: str = "llama3.1-8b-8192") -> Optional[Dict[str, Any]]:
    """
    Process a quiz response and return properly formatted JSON using Groq
    
    Args:
        quiz_response: The raw quiz response from the first LLM
        api_key: Groq API key
        model: Groq model to use for formatting
        
    Returns:
        Parsed quiz dictionary or None if failed
    """
    formatter = GroqJSONFormatter(api_key, model)
    
    print("🔄 Processing quiz response with Groq...")
    print(f"Input length: {len(quiz_response)} characters")
    
    # Try to format with Groq LLM
    formatted_quiz = formatter.format_json_with_groq(quiz_response)
    
    if formatted_quiz:
        print("✅ Quiz successfully formatted!")
        return formatted_quiz
    else:
        print("❌ Failed to format quiz")
        return None

def save_formatted_quiz(quiz_data: Dict[str, Any], filename: str = None) -> str:
    """
    Save the formatted quiz to a file
    
    Args:
        quiz_data: The formatted quiz data
        filename: Optional filename, will generate one if not provided
        
    Returns:
        The filename where the quiz was saved
    """
    if filename is None:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        subject = quiz_data.get('quiz_info', {}).get('subject', 'quiz').replace(' ', '_').lower()
        filename = f"formatted_{subject}_quiz_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Quiz saved to: {filename}")
    return filename

def main():
    """Main function to test the JSON corrector"""
    # Your input JSON
    test_json_input = '''{
"quiz_info": {
"title": "Computer Vision Quiz",
"subject": "Computer Vision",
"difficulty": "easy",
"total_questions": 7
},
"questions": [
{
"id": 1,
"question": "What is the main topic discussed in the text?",
"options": {
"A": "Acquiring, processing, and analyzing digital images",
"B": "Understanding digital images",
"C": "Extracting high-dimensional data from the real world",
"D": "Applying computer vision theories to construction"
},
"correct_answer": "B",
"explanation": "The text discusses the scientific discipline of computer vision and its concern with the theory behind artificial systems that extract information from images."
},
{
"id": 2,
"question": "What is the term for the transformation of visual images into descriptions of the world?",
"options": {
"A": "Image understanding",
"B": "Scene reconstruction",
"C": "Object detection",
"D": "Activity recognition"
},
"correct_answer": "A",
"explanation": "Image understanding is the transformation of visual images into descriptions of the world that make sense to thought processes and can elicit appropriate action."
},
{
"id": 3,
"question": "What is the technological discipline of computer vision concerned with?",
"options": {
"A": "Applying computer vision theories to construction",
"B": "Understanding digital images",
"C": "Extracting high-dimensional data from the real world",
"D": "Theory behind artificial systems that extract information from images"
},
"correct_answer": "A",
"explanation": "The technological discipline of computer vision seeks to apply its theories and models to the construction of computer vision systems."
},
{
"id": 4,
"question": "What is an example of image data?",
"options": {
"A": "Video sequences",
"B": "3D point clouds from LiDaR sensors",
"C": "Multi-dimensional data from a 3D scanner",
"D": "All of the above"
},
"correct_answer": "D",
"explanation": "Image data can take many forms, including video sequences, 3D point clouds from LiDaR sensors, and multi-dimensional data from a 3D scanner."
},
{
"id": 5,
"question": "What is a subdiscipline of computer vision?",
"options": {
"A": "Scene reconstruction",
"B": "Object recognition",
"C": "Event detection",
"D": "All of the above"
},
"correct_answer": "D",
"explanation": "Subdisciplines of computer vision include scene reconstruction, object recognition, event detection, and more."
},
{
"id": 6,
"question": "What is the goal of image understanding?",
"options": {
"A": "To extract high-dimensional data from the real world",
"B": "To apply computer vision theories to construction",
"C": "To transform visual images into descriptions of the world",
"D": "To understand digital images"
},
"correct_answer": "C",
"explanation": "The goal of image understanding is to transform visual images into descriptions of the world that make sense to thought processes and can elicit appropriate action."
},
{
"id": 7,
"question": "What is the scientific discipline of computer vision concerned with?",
"options": {
"A": "Applying computer vision theories to construction",
"B": "Understanding digital images",
"C": "Theory behind artificial systems that extract information from images",
"D": "Extracting high-dimensional data from the real world"
},
"correct_answer": "C",
"explanation": "The scientific discipline of computer vision is concerned with the theory behind artificial systems that extract information from images."
}
]'''

    # Initialize the JSON corrector
    corrector = JSONCorrector()
    
    # Test the JSON correction function
    print("Testing JSON correction...")
    corrected_json = corrector.correct_and_format_json(test_json_input)
    
    if corrected_json:
        print("\nCorrected JSON:")
        print(corrected_json)
        
        # Validate the corrected JSON
        is_valid, message = corrector.validate_mcq_structure(corrected_json)
        print(f"\nValidation result: {message}")
        
        if is_valid:
            # Parse and display some info
            parsed_data = json.loads(corrected_json)
            print(f"Quiz title: {parsed_data['quiz_info']['title']}")
            print(f"Total questions: {parsed_data['quiz_info']['total_questions']}")
            print(f"Actual questions: {len(parsed_data['questions'])}")
            
            # Save the corrected JSON
            corrector.save_corrected_json(corrected_json, "computer_vision_mcqs_corrected.json")
        else:
            print("JSON structure validation failed!")

if __name__ == "__main__":
    main() 