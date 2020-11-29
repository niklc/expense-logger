import flask

KEY = 'credentials'

def isCredentialsSet():
    if KEY in flask.session:
        return True

    return False


def getCredentials():
    return flask.session[KEY]


def setCredentials(credentials):
    flask.session[KEY] = credentials


def deleteCredentials():
    del flask.session[KEY]
