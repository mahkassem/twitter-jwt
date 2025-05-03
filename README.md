# Twitter Flask Clone

> A Twitter clone built with Flask for educational purposes.

## Project Setup

```sh
# Clone the repo
git clone <repo>

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Migration
flask db upgrade

# Seed the database
python seed.py

# Run the application
flask run
```

## Structure

```sh
├── src
│   ├── api
│   │   ├── auth.py
│   │   ├── tweets.py
│   │   └── users.py
│   ├── middleware
│   │   └── auth_guard.py
│   ├── models.py
│   ├── __init__.py
├── seed.py
├── requirements.txt
├── wsgi.py
```
