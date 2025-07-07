#!/usr/bin/env python3
"""
Command Line Interface for MCQ Generator
"""

import argparse
import sys
from pathlib import Path
import json
from dotenv import load_dotenv
from src.mcq_generator.MCQgenerator import generate_evaluate_chain
from src.mcq_generator.utils import save_mcqs_to_csv

def main():
    parser = argparse.ArgumentParser(
        description="Generate Multiple Choice Questions using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --topic "Python Basics" --num-questions 5
  python cli.py --topic "Data Structures" --difficulty hard --subject "computer science"
        """
    )
    
    parser.add_argument(
        "--topic", "-t",
        type=str,
        help="Topic for MCQ generation"
    )
    
    parser.add_argument(
        "--num-questions", "-n",
        type=int,
        default=5,
        help="Number of questions to generate (default: 5)"
    )
    
    parser.add_argument(
        "--difficulty", "-d",
        type=str,
        choices=["easy", "medium", "hard"],
        default="medium",
        help="Difficulty level (default: medium)"
    )
    
    parser.add_argument(
        "--subject", "-s",
        type=str,
        default="general",
        help="Subject area (default: general)"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default=".",
        help="Output directory for generated files (default: current directory)"
    )
    
    parser.add_argument(
        "--format", "-f",
        type=str,
        choices=["json", "csv", "txt", "all"],
        default="all",
        help="Output format (default: all)"
    )
    
    args = parser.parse_args()
    
    if not args.topic:
        parser.print_help()
        sys.exit(1)
    
    if not 1 <= args.num_questions <= 20:
        print("Error: Number of questions must be between 1 and 20")
        sys.exit(1)
    
    # Load environment variables
    load_dotenv()
    
    # Load response JSON schema
    try:
        with open("Response.json", "r") as f:
            response_json = json.load(f)
    except Exception as e:
        print(f"Error loading Response.json: {e}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating {args.num_questions} {args.difficulty} MCQs on '{args.topic}'...")
    
    # Generate MCQs
    try:
        result = generate_evaluate_chain({
            "text": args.topic,
            "number": args.num_questions,
            "subject": args.subject,
            "tone": args.difficulty.capitalize(),
            "response_json": json.dumps(response_json)
        })
    except Exception as e:
        print(f"Error generating MCQs: {e}")
        sys.exit(1)
    
    quiz_json = result.get("fixed_quiz")
    if not quiz_json:
        print("Error: No MCQs generated.")
        sys.exit(1)
    
    # Parse the quiz JSON
    try:
        parsed_mcqs = json.loads(quiz_json)
    except Exception as e:
        print(f"Error parsing generated MCQs: {e}")
        sys.exit(1)
    
    # Create timestamp for unique filenames
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = args.topic.replace(' ', '_').lower().replace('/', '_')
    filename_base = f"mcqs_{safe_topic}_{timestamp}"
    
    # Save in specified format(s)
    if args.format in ["json", "all"]:
        with open(output_path / f"{filename_base}.json", "w", encoding="utf-8") as f:
            json.dump(parsed_mcqs, f, ensure_ascii=False, indent=2)
        print(f"Saved: {output_path / f'{filename_base}.json'}")
    
    if args.format in ["csv", "all"]:
        save_mcqs_to_csv(quiz_json, str(output_path / filename_base))
    
    if args.format in ["txt", "all"]:
        with open(output_path / f"{filename_base}.txt", "w", encoding="utf-8") as f:
            for i, q in enumerate(parsed_mcqs.get("questions", []), 1):
                f.write(f"Question {i}: {q.get('question', '')}\n")
                for key, value in q.get("options", {}).items():
                    f.write(f"{key}) {value}\n")
                f.write(f"Correct Answer: {q.get('correct_answer', '')}\n")
                f.write(f"Explanation: {q.get('explanation', '')}\n")
                f.write("-"*50 + "\n")
        print(f"Saved: {output_path / f'{filename_base}.txt'}")
    
    print(f"Successfully generated and saved {len(parsed_mcqs.get('questions', []))} MCQs!")

if __name__ == "__main__":
    main() 