from octopype.errors.account import InvalidToken, AuthenticationError
from octopype.errors.general import BackendError

def account_update_check(request):
    if request.status_code == 401:
        raise InvalidToken("authentication failed, no token given")
    elif request.status_code == 403:
        raise AuthenticationError("returned status code 403 forbidden")
    elif request.status_code == 422:
        raise BackendError("validation failed or the endpoint has been spammed")