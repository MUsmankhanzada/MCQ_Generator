# MCQ Generator

An AI-powered Multiple Choice Question (MCQ) generator that uses the Groq API to create high-quality educational questions.

## Features

- 🤖 **AI-Powered Generation**: Uses Groq's Llama3-8b model for intelligent MCQ creation
- 📚 **Multiple Subjects**: Generate MCQs for any subject area (computer science, math, history, etc.)
- 🎯 **Difficulty Levels**: Support for easy, medium, and hard difficulty levels
- 📊 **Multiple Formats**: Export to JSON, CSV, and TXT formats
- 🖥️ **Multiple Interfaces**: Jupyter notebook, command-line interface, and Python API
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

### 2. Command Line Interface

Generate MCQs directly from the command line:

```bash
# Basic usage
python src/mcq_generator/cli.py --topic "Python Basics" --num-questions 5

# With specific difficulty and subject
python src/mcq_generator/cli.py --topic "Data Structures" --difficulty hard --subject "computer science"

# Interactive mode
python src/mcq_generator/cli.py --interactive

# Save to specific directory
python src/mcq_generator/cli.py --topic "Machine Learning" --output-dir "./my_mcqs"

# Save in specific format only
python src/mcq_generator/cli.py --topic "Algorithms" --format csv
```

### 3. Python API

Use the MCQ generator in your own Python scripts:

```python
from src.mcq_generator.enhanced_mcq_generator import EnhancedMCQGenerator

# Initialize the generator
generator = EnhancedMCQGenerator()

# Generate MCQs
mcqs_response = generator.generate_mcqs(
    topic="Python Programming",
    num_questions=3,
    difficulty="medium",
    subject_area="computer science"
)

# Parse the response
parsed_mcqs = generator.parse_mcqs_response(mcqs_response)

# Save to files
generator.save_mcqs_to_json(parsed_mcqs, "my_mcqs.json")
generator.save_mcqs_to_csv(parsed_mcqs, "my_mcqs.csv")
```

## CLI Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--topic` | `-t` | Topic for MCQ generation | Required |
| `--num-questions` | `-n` | Number of questions (1-20) | 5 |
| `--difficulty` | `-d` | Difficulty level (easy/medium/hard) | medium |
| `--subject` | `-s` | Subject area | general |
| `--output-dir` | `-o` | Output directory | current directory |
| `--format` | `-f` | Output format (json/csv/txt/all) | all |
| `--interactive` | `-i` | Run in interactive mode | False |

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

## Examples

### Computer Science MCQs
```bash
python src/mcq_generator/cli.py --topic "Object-Oriented Programming" --difficulty hard --subject "computer science" --num-questions 10
```

### Mathematics MCQs
```bash
python src/mcq_generator/cli.py --topic "Calculus Derivatives" --difficulty medium --subject "mathematics" --num-questions 5
```

### History MCQs
```bash
python src/mcq_generator/cli.py --topic "World War II" --difficulty easy --subject "history" --num-questions 8
```

## Project Structure

```
MCQ_Generator/
├── experiment/
│   └── mcq.ipynb              # Jupyter notebook for experimentation
├── src/
│   └── mcq_generator/
│       ├── __init__.py
│       ├── enhanced_mcq_generator.py  # Main MCQ generator class
│       └── cli.py                     # Command-line interface
├── requirement.txt            # Python dependencies
├── setup.py                  # Package setup
└── README.md                 # This file
```

## Configuration

### Model Parameters

The MCQ generator uses the following default parameters for the Groq API:

- **Model**: `llama3-8b-8192`
- **Temperature**: 0.3 (for consistent, factual responses)
- **Max Tokens**: 2048 (for detailed explanations)
- **Top P**: 0.8 (for focused responses)
- **Top K**: 30 (for quality control)

You can modify these in the `EnhancedMCQGenerator` class.

### Environment Variables

- `GROQ_API_KEY`: Your Groq API key (required)

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