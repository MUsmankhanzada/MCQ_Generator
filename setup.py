from setuptools import setup, find_packages

setup(
    name="mcq_generator",
    version="0.1.0",
    author="Muhammad Usman Khanzada",
    author_email="usmankz.khan363@gmail.com",
    description="A multiple choice question generator using Groq AI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "groq",
        "langchain",
        "langchain-groq",  # LangChain integration for Groq
        "streamlit",
        "python-dotenv",
        "PyPDF2",
        "requests",  # For API calls
        "pandas",  # For data handling
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)