# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a RAG (Retrieval-Augmented Generation) example project built with Python using Poetry for dependency management. The project uses LangChain for RAG implementation and ChromaDB for vector storage.

## Development Setup

This project uses Poetry for dependency management. Make sure Poetry is installed on your system.

### Initial Setup
```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Copy environment file and configure
cp .env .env
# Edit .env with your API keys
```

## Common Commands

### Environment Management
- `poetry shell` - Activate virtual environment
- `poetry install` - Install dependencies
- `poetry add <package>` - Add new dependency
- `poetry add --group dev <package>` - Add development dependency

### Development
- `poetry run python rag_example/main.py` - Run main application
- `poetry run python -m streamlit run app.py` - Run Streamlit app (when created)

### Code Quality
- `poetry run black .` - Format code with Black
- `poetry run isort .` - Sort imports
- `poetry run flake8 .` - Run linting
- `poetry run mypy .` - Run type checking

### Testing
- `poetry run pytest` - Run all tests
- `poetry run pytest tests/test_specific.py` - Run specific test file
- `poetry run pytest -v` - Run tests with verbose output

## Project Structure

```
rag_example/           # Main package
├── __init__.py       # Package initialization
├── main.py          # Application entry point
├── models/          # Data models and schemas
├── vector_store/    # Vector database operations
├── retrieval/       # Document retrieval logic
└── generation/      # Response generation logic

tests/               # Test files
```

## Architecture Notes

- **LangChain**: Used for RAG pipeline orchestration
- **ChromaDB**: Vector database for storing document embeddings
- **OpenAI**: Default LLM provider (configurable)
- **Streamlit**: Web interface for demos
- **Pydantic**: Data validation and settings management

## Environment Variables

Required environment variables (copy from .env.example):
- `OPENAI_API_KEY`: OpenAI API key for LLM access
- `CHROMA_PERSIST_DIRECTORY`: ChromaDB storage directory