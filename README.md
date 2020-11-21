venv
```bash
python3 -m venv venv
source venv/bin/activate
deactivate
```

Install dev dependencies
```bash
pip install -r requirements.txt
```

Run local dev server
```bash
export FLASK_APP=expense_logger
export FLASK_ENV=development
flask run
```

Read for deployment
- https://flask.palletsprojects.com/en/1.1.x/deploying/uwsgi/#configuring-nginx
- https://medium.com/bitcraft/docker-composing-a-python-3-flask-app-line-by-line-93b721105777

Google API:
- https://developers.google.com/sheets/api/quickstart/python
- https://developers.google.com/identity/sign-in/web/sign-in