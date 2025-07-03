#!/usr/bin/env python3
"""
Command Line Interface for MCQ Generator
"""

import argparse
import sys
from pathlib import Path
from enhanced_mcq_generator import EnhancedMCQGenerator

def main():
    parser = argparse.ArgumentParser(
        description="Generate Multiple Choice Questions using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --topic "Python Basics" --num-questions 5
  python cli.py --topic "Data Structures" --difficulty hard --subject "computer science"
  python cli.py --interactive
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
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )
    
    parser.add_argument(
        "--format", "-f",
        type=str,
        choices=["json", "csv", "txt", "all"],
        default="all",
        help="Output format (default: all)"
    )
    
    args = parser.parse_args()
    
    try:
        generator = EnhancedMCQGenerator()
        
        if args.interactive:
            generator.interactive_generator()
        elif args.topic:
            # Validate inputs
            if not 1 <= args.num_questions <= 20:
                print("Error: Number of questions must be between 1 and 20")
                sys.exit(1)
            
            # Create output directory if it doesn't exist
            output_path = Path(args.output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            print(f"Generating {args.num_questions} {args.difficulty} MCQs on '{args.topic}'...")
            
            mcqs_response = generator.generate_mcqs(
                args.topic, 
                args.num_questions, 
                args.difficulty, 
                args.subject
            )
            
            if mcqs_response:
                parsed_mcqs = generator.parse_mcqs_response(mcqs_response)
                
                if parsed_mcqs:
                    # Create timestamp for unique filenames
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    safe_topic = args.topic.replace(' ', '_').lower().replace('/', '_')
                    filename_base = f"mcqs_{safe_topic}_{timestamp}"
                    
                    # Save in specified format(s)
                    if args.format in ["json", "all"]:
                        generator.save_mcqs_to_json(parsed_mcqs, output_path / f"{filename_base}.json")
                    
                    if args.format in ["csv", "all"]:
                        generator.save_mcqs_to_csv(parsed_mcqs, output_path / f"{filename_base}.csv")
                    
                    if args.format in ["txt", "all"]:
                        generator.save_mcqs_to_txt(parsed_mcqs, output_path / f"{filename_base}.txt")
                    
                    print(f"Successfully generated and saved {len(parsed_mcqs)} MCQs!")
                else:
                    print("Error: Failed to parse generated MCQs")
                    sys.exit(1)
            else:
                print("Error: Failed to generate MCQs")
                sys.exit(1)
        else:
            parser.print_help()
            sys.exit(1)
            
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 