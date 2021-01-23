from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests


CLIENT_SECRETS_FILE = 'credentials.json'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'openid'
]


def get_request_token(redirect_uri):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES
    )

    flow.redirect_uri = redirect_uri

    return flow.authorization_url(
        access_type='offline',
        include_granted_scopes='false'
    )


def get_credentials(callback_url, state, authorization_response):
    credentials = _get_access_tokens(
        callback_url, state, authorization_response)

    user_id = _get_user_id(credentials)

    return _credentials_to_dict(credentials, user_id)


def _get_access_tokens(callback_url, state, authorization_response):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state
    )

    flow.redirect_uri = callback_url

    flow.fetch_token(authorization_response=authorization_response)

    return flow.credentials


def _get_user_id(credentials):
    token = credentials.id_token
    request = requests.Request()

    id_info = id_token.verify_oauth2_token(token, request)

    return id_info['sub']


def _credentials_to_dict(credentials, user_id):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
        'user_id': user_id
    }
