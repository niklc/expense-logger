import flask


def isCredentialsSet():
    if 'credentials' in flask.session:
        return True

    return False


def getCredentials():
    return flask.session['credentials']


def setCredentials(credentials):
    flask.session['credentials'] = credentials


def revokeCredentials():
    del flask.session['credentials']
