import google_auth_oauthlib.flow


CLIENT_SECRETS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_request_token(redirect_uri):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES
    )

    flow.redirect_uri = redirect_uri

    return flow.authorization_url(
        access_type='online',
        include_granted_scopes='false'
    )


def get_access_token(callback_url, state, authorization_response):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state
    )

    flow.redirect_uri = callback_url

    flow.fetch_token(authorization_response=authorization_response)

    return _credentials_to_dict(flow.credentials)


def _credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
