# JSON Formatting Prompt Template for Groq Models
# This prompt is designed to convert malformed JSON into valid JSON format

JSON_FORMATTING_PROMPT = """
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

def create_json_formatting_prompt(malformed_json: str) -> str:
    """
    Create a formatted prompt for JSON formatting
    
    Args:
        malformed_json: The malformed JSON string to format
        
    Returns:
        The complete prompt string
    """
    return JSON_FORMATTING_PROMPT.format(input_json=malformed_json)

# Example usage
if __name__ == "__main__":
    # Example malformed JSON
    example_json = '''
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
    "question": "What is the main topic discussed in the text?",
    "options": {
    "A": "Acquiring, processing, analyzing, and understanding digital images",
    "B": "Machine learning and deep learning",
    "C": "Image recognition and object detection",
    "D": "Scene reconstruction and 3D modeling"
    },
    "correct_answer": "A",
    "explanation": "The text discusses the main topic of computer vision, which is acquiring, processing, analyzing, and understanding digital images."
    }
    ]
    }
    '''
    
    # Create the prompt
    prompt = create_json_formatting_prompt(example_json)
    print("Generated Prompt:")
    print("=" * 50)
    print(prompt)
    print("=" * 50) 