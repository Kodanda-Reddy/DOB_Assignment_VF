python -m venv venv
venv\Scripts\activate.bat && pip install -r requirements.txt && python -m pytest --html=report.html & deactivate