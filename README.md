# Medicine Recommendation System

A web-based personal medicine recommendation system that uses machine learning to predict diseases based on symptoms and recommend appropriate medicines.

## Features

- Disease prediction based on symptoms
- Medicine recommendations
- User authentication (Patients, Admins, Medical Experts)
- Responsive UI with Bootstrap
- Machine Learning powered predictions using SVC model

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the application:
```bash
flask run
```

## Project Structure

- `/app` - Main application package
  - `/static` - Static files (CSS, JS)
  - `/templates` - HTML templates
  - `/models` - Database models
  - `/ml` - Machine learning models
- `/migrations` - Database migrations
- `config.py` - Configuration settings
- `run.py` - Application entry point
