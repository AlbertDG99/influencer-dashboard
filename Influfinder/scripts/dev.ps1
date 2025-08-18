param()
$ErrorActionPreference = "Stop"
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH = "."
$env:FLASK_ENV = "development"
python backend/app.py
