### General set-up

Generate `credentials.json` file for Google API access. Callback URI should be https://localhost/authorize-callback. See https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the.

Copy `.env.example` to `.env` and fill its keys.

To initialise DB in conteiner or after installing Python requirements locally run:
```bash
export FLASK_APP=expense_logger
flask init-db
```


### Local development

Run:
```bash
docker-compose up
```

### Production

Get SSL certificate:
```bash
docker-compose -f docker-compose.yml -f docker-compose.get-certificates.yml up
```

Run:
```bash
docker-compose -f docker-compose.yml -f docker-compose.production.yml up -d
```
