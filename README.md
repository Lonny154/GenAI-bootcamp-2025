# Language Learning Portal

A prototype web application that serves as a comprehensive language learning platform with the following features:
- Vocabulary inventory management
- Learning progress tracking (LRS - Learning Record Store)
- Centralized launch pad for various learning applications

## Setup Instructions

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Features

### 1. Vocabulary Inventory
- Browse and search through available vocabulary
- Filter by language and difficulty level
- View detailed meanings and usage examples

### 2. Learning Record Store (LRS)
- Track correct and incorrect answers
- View progress statistics
- Monitor learning history

### 3. Learning Apps Launchpad
- Central hub for accessing various learning applications
- Easy navigation between different learning tools
- Quick access to favorite applications

## Database Schema

The application uses SQLite with the following main tables:
- `Vocabulary`: Stores vocabulary items with meanings and metadata
- `LearningRecord`: Tracks learning attempts and progress
- `LearningApp`: Manages available learning applications

## API Endpoints

- `GET /vocabulary`: Retrieve vocabulary list
- `POST /record`: Record a learning attempt
- `GET /apps`: Get available learning applications

