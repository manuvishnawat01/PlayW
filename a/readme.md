pip install -r requirements.txt   

playwright install chromium

python -m pytest -v

python -m pytest -s tests/test_complete_flow.py --headed --slowmo 500

python -m pytest -v tests/test_data_driven_login.py

