import sys

from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.response import Response
from service_objects.errors import InvalidInputsError


def custom_exception_handler(exc, context):
    try:
        if isinstance(exc, InvalidInputsError):
            response_status = 400
            errors = [{error: exc.errors[error][0].messages[0]} for error in exc.errors]
            errors_response = {}
            for error in errors:
                errors_response |= error
            return Response(errors_response, status=response_status)
        elif isinstance(exc, NotAuthenticated):
            response_status = 401
        elif isinstance(exc, AuthenticationFailed):
            response_status = 403
        else:
            response_status = exc.response_status
    except AttributeError:
        response_status = 500
    return Response({sys.exc_info()[0].__name__: exc.__str__()}, status=response_status)
