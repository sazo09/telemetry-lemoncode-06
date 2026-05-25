# Using python-dotenv

Py-dotenv (python-dotenv) loads environment variables from a `.env` file into your Python app, keeping secrets like API keys secure and separate from code. [geeksforgeeks](https://www.geeksforgeeks.org/python/using-python-environment-variables-with-python-dotenv/)
## Installation
Install via pip with `pip install python-dotenv`. [youtube](https://www.youtube.com/watch?v=pyUyeepCOjE)
## Setup Steps
Create a `.env` file in your project root:

```
SECRET_KEY=your_secret_here
DATABASE_URL=postgresql://user:pass@localhost/db
DEBUG=True
```

Add `.env` to `.gitignore` to avoid committing secrets. [geeksforgeeks](https://www.geeksforgeeks.org/python/using-python-environment-variables-with-python-dotenv/)
## Basic Usage
Import and load in your Python script:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env into os.environ

secret = os.getenv('SECRET_KEY')
debug = os.getenv('DEBUG', 'False') == 'True'  # With default and type conversion
```

Access variables via `os.getenv()`. By default, it doesn't override existing env vars; use `load_dotenv(override=True)` if needed. [geeksforgeeks](https://www.geeksforgeeks.org/python/using-python-environment-variables-with-python-dotenv/)
This setup works for Flask, Django, or any Python project—call `load_dotenv()` early. [youtube](https://www.youtube.com/watch?v=pyUyeepCOjE)
## CLI Features
Install with CLI support: `pip install "python-dotenv[cli]"`. Then use commands like `dotenv run -- python app.py` or `dotenv set KEY value`. [pypi](https://pypi.org/project/python-dotenv/)