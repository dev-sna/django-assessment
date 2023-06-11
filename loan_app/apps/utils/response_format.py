from rest_framework.response import Response
from rest_framework import status
from loan_app.apps.utils.constants import (
    DEFAULT_FAILURE_MESSAGE,
    DEFAULT_SUCCESS_MESSAGE,
)


def success_response(
    data=None,
    success_message=DEFAULT_SUCCESS_MESSAGE,
    status_code=status.HTTP_200_OK,
):
    response_data = {"success": True, "message": success_message, "data": data}
    response = Response(response_data, status=status_code)
    return response


def failure_response(
    failure_message=DEFAULT_FAILURE_MESSAGE,
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    data=None,
    # force_logout=False,
):

    response_data = {
        "status_code": status_code,
        "success": False,
        "message": failure_message,
        "data": data,
    }

    response = Response(response_data, status=status_code)
    # if force_logout:
    #     remove_login_cookie(response)
    return response
