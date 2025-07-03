#!/usr/bin/env python3
"""
Example usage of the MCQ Generator
"""

import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from mcq_generator.enhanced_mcq_generator import EnhancedMCQGenerator
except ImportError:
    print("Error: Could not import EnhancedMCQGenerator")
    print("Make sure you have installed the package: pip install -e .")
    sys.exit(1)

def main():
    """Example usage of the MCQ Generator"""
    
    print("=== MCQ Generator Example ===\n")
    
    try:
        # Initialize the generator
        generator = EnhancedMCQGenerator()
        print("✓ MCQ Generator initialized successfully\n")
        
        # Example 1: Generate basic MCQs
        print("Example 1: Generating basic MCQs")
        print("-" * 40)
        
        mcqs_response = generator.generate_mcqs(
            topic="Python Variables and Data Types",
            num_questions=3,
            difficulty="easy",
            subject_area="computer science"
        )
        
        if mcqs_response:
            parsed_mcqs = generator.parse_mcqs_response(mcqs_response)
            print(f"✓ Generated {len(parsed_mcqs)} MCQs successfully")
            
            # Display the first MCQ
            if parsed_mcqs:
                first_mcq = parsed_mcqs[0]
                print(f"\nSample MCQ:")
                print(f"Question: {first_mcq.get('question', 'N/A')}")
                print(f"Options: {first_mcq.get('options', {})}")
                print(f"Correct Answer: {first_mcq.get('correct_answer', 'N/A')}")
                print(f"Explanation: {first_mcq.get('explanation', 'N/A')}")
            
            # Save to files
            generator.save_mcqs_to_json(parsed_mcqs, "example_mcqs.json")
            generator.save_mcqs_to_csv(parsed_mcqs, "example_mcqs.csv")
            generator.save_mcqs_to_txt(parsed_mcqs, "example_mcqs.txt")
            print("\n✓ MCQs saved to example_mcqs.json, example_mcqs.csv, and example_mcqs.txt")
        
        print("\n" + "="*50 + "\n")
        
        # Example 2: Generate advanced MCQs
        print("Example 2: Generating advanced MCQs")
        print("-" * 40)
        
        advanced_mcqs = generator.generate_mcqs(
            topic="Object-Oriented Programming Concepts",
            num_questions=2,
            difficulty="hard",
            subject_area="computer science"
        )
        
        if advanced_mcqs:
            parsed_advanced = generator.parse_mcqs_response(advanced_mcqs)
            print(f"✓ Generated {len(parsed_advanced)} advanced MCQs successfully")
            
            # Save with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_base = f"advanced_mcqs_{timestamp}"
            
            generator.save_mcqs_to_json(parsed_advanced, f"{filename_base}.json")
            print(f"✓ Advanced MCQs saved to {filename_base}.json")
        
        print("\n" + "="*50 + "\n")
        
        # Example 3: Batch generation
        print("Example 3: Batch generation for different topics")
        print("-" * 40)
        
        topics = [
            ("Basic Mathematics", "mathematics", "easy"),
            ("World History", "history", "medium"),
            ("Chemistry Basics", "science", "easy")
        ]
        
        for topic, subject, difficulty in topics:
            print(f"Generating MCQs for: {topic}")
            response = generator.generate_mcqs(
                topic=topic,
                num_questions=2,
                difficulty=difficulty,
                subject_area=subject
            )
            
            if response:
                parsed = generator.parse_mcqs_response(response)
                print(f"✓ Generated {len(parsed)} MCQs for {topic}")
                
                # Save with topic name
                safe_topic = topic.replace(' ', '_').lower()
                generator.save_mcqs_to_json(parsed, f"{safe_topic}_mcqs.json")
            else:
                print(f"✗ Failed to generate MCQs for {topic}")
        
        print("\n" + "="*50)
        print("✓ All examples completed successfully!")
        print("\nCheck the generated files in the current directory:")
        print("- example_mcqs.json/csv/txt")
        print("- advanced_mcqs_*.json")
        print("- basic_mathematics_mcqs.json")
        print("- world_history_mcqs.json")
        print("- chemistry_basics_mcqs.json")
        
    except ValueError as e:
        print(f"Error: {e}")
        print("Make sure your GROQ_API_KEY is set in the .env file")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main() 