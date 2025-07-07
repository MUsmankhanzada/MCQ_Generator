# MCQ Generator

An AI-powered Multiple Choice Question (MCQ) generator that uses the Groq API to create high-quality educational questions.

## Features

- 🤖 **AI-Powered Generation**: Uses Groq's Llama3-8b model for intelligent MCQ creation
- 📚 **Multiple Subjects**: Generate MCQs for any subject area (computer science, math, history, etc.)
- 🎯 **Difficulty Levels**: Support for easy, medium, and hard difficulty levels
- 📊 **Multiple Formats**: Export to JSON, CSV, and TXT formats
- 🖥️ **Multiple Interfaces**: Jupyter notebook, Streamlit app, and Python API
- 🔧 **Customizable**: Adjustable parameters for question count, difficulty, and subject area

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd MCQ_Generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirement.txt
   ```

3. **Set up your Groq API key**:
   - Get your API key from [Groq Console](https://console.groq.com/)
   - Create a `.env` file in the project root:
     ```
     GROQ_API_KEY=your_api_key_here
     ```

## Usage

### 1. Jupyter Notebook (Recommended for experimentation)

Run the Jupyter notebook in the `experiment/` directory:

```bash
jupyter notebook experiment/mcq.ipynb
```

The notebook includes:
- Basic MCQ generation
- Response parsing
- Multiple export formats
- Interactive generation

### 2. Streamlit App

Run the interactive web app:

```bash
streamlit run stramlitAPP.py
```

Features:
- Upload PDF or TXT files
- Configure number of questions, subject, and tone
- Generate MCQs and take quizzes interactively
- Download results in CSV format

### 3. Python API (Direct Programmatic Usage)

You can use the MCQ generator in your own Python scripts by calling the chain directly:

```python
from src.mcq_generator.MCQgenerator import generate_evaluate_chain
import json

# Load your input text (e.g., from a file)
input_text = """Your study material here."""

# Load the response JSON schema (see Response.json in the repo)
with open("Response.json", "r") as f:
    response_json = json.load(f)

# Call the chain
result = generate_evaluate_chain({
    "text": input_text,
    "number": 5,  # Number of MCQs
    "subject": "computer science",
    "tone": "Simple",
    "response_json": json.dumps(response_json)
})

# The result is a dict with keys: 'quiz', 'review', 'fixed_quiz'
quiz_json = result["fixed_quiz"]
print(quiz_json)
```

#### Saving MCQs to CSV

```python
from src.mcq_generator.utils import save_mcqs_to_csv
save_mcqs_to_csv(quiz_json, filename="my_mcqs")
```

### 4. Command Line Interface (CLI)

> **Note:** The CLI (`src/mcq_generator/cli.py`) and `example_usage.py` currently reference a non-existent `EnhancedMCQGenerator` class and will not work out-of-the-box. To use the CLI, update it to use the `generate_evaluate_chain` as shown above.

## Output Formats

### JSON Format
```json
[
  {
    "question": "What is the primary purpose of a function in programming?",
    "options": {
      "A": "To store data",
      "B": "To perform a specific task",
      "C": "To create variables",
      "D": "To print text"
    },
    "correct_answer": "B",
    "explanation": "Functions are designed to perform specific tasks and can be reused throughout the program."
  }
]
```

### CSV Format
| question_number | question | option_a | option_b | option_c | option_d | correct_answer | explanation |
|----------------|----------|----------|----------|----------|----------|----------------|-------------|
| 1 | What is the primary purpose... | To store data | To perform a specific task | To create variables | To print text | B | Functions are designed... |

### TXT Format
```
Question 1: What is the primary purpose of a function in programming?
A) To store data
B) To perform a specific task
C) To create variables
D) To print text
Correct Answer: B
Explanation: Functions are designed to perform specific tasks and can be reused throughout the program.
--------------------------------------------------
```

## Project Structure

```
MCQ_Generator/
├── experiment/
│   └── mcq.ipynb              # Jupyter notebook for experimentation
├── src/
│   └── mcq_generator/
│       ├── __init__.py
│       ├── MCQgenerator.py    # Main MCQ generation logic (chains, not a class)
│       ├── cli.py             # Command-line interface (needs update)
│       ├── utils.py           # Utility functions (file reading, CSV export)
│       └── logger.py
├── requirement.txt            # Python dependencies
├── setup.py                   # Package setup
├── stramlitAPP.py             # Streamlit web app
├── Response.json              # JSON schema for MCQ output
└── README.md                  # This file
```

## Configuration

### Model Parameters

The MCQ generator uses the following default parameters for the Groq API:

- **Model**: `llama3-8b-8192` (generation), `llama3-70b-8192` (JSON fixing)
- **Temperature**: 0.3 (for consistent, factual responses)
- **Max Tokens**: 2096 (generation), 4096 (JSON fixing)
- **Stop Sequences**: For question boundaries and JSON output

You can modify these in `src/mcq_generator/MCQgenerator.py`.

### Environment Variables

- `GROQ_API_KEY`: Your Groq API key (required)

## Recent Updates

### Enhanced Chain Logic (Latest)

The MCQ generation chain has been enhanced to provide better separation of concerns:

1. **Quiz Generation**: Creates the initial quiz
2. **Review & Enhancement**: Reviews the quiz and outputs two separate components:
   - **Enhanced Quiz**: An improved version of the original quiz
   - **Analysis**: Detailed assessment of complexity, quality, and suggested improvements
3. **JSON Fixing**: The enhanced quiz (not the original) is now processed for JSON validation

This ensures that the final output uses the improved quiz rather than the original one.

### Chain Output Variables

The `generate_evaluate_chain` now returns:
- `quiz`: Original generated quiz
- `review`: Complete review output with markers
- `fixed_quiz`: Final JSON-fixed enhanced quiz

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your `GROQ_API_KEY` is set correctly in the `.env` file
2. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirement.txt`
3. **Parsing Issues**: If MCQs aren't parsing correctly, check the LLM response format

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify your API key is valid
3. Ensure you have sufficient API credits
4. Try reducing the number of questions if you hit token limits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Groq](https://groq.com/) for providing the AI API
- [LangChain](https://langchain.com/) for the Python framework
- The open-source community for various dependencies