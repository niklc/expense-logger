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
export FLASK_APP=expense_logger && export FLASK_ENV=development
flask run
```

OAuth 2.0 local testing
```bash
export OAUTHLIB_INSECURE_TRANSPORT=1
```