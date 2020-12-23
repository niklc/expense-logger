Set-up
```bash
python3 -m venv venv
pip install -r requirements.txt
```

Activate venv
```bash
source venv/bin/activate
```

Deactivate venv
```bash
deactivate
```

Run local dev server
```bash
export FLASK_APP=expense_logger && export FLASK_ENV=development && export OAUTHLIB_INSECURE_TRANSPORT=1
flask run
```

Generate `credentials.json` file for Google API access. See https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the.