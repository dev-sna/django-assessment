from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView

from loan_app.apps.users.serializers import LoginRequestSerializer, UserSerializer
from loan_app.apps.utils.constants import INCORRECT_EMAIL_OR_PASSWORD, LOGIN_API_SUCCESS
from loan_app.apps.utils.jwt import get_tokens_for_user
from loan_app.apps.utils.response_format import failure_response, success_response


def user_data_with_jwt_token(user_data, user, remember_me=False):
    token_data = get_tokens_for_user(user)
    return {
        "user": user_data,
        "token": token_data["access"],
        "refresh": token_data["refresh"],
    }


class CreateUserApiView(APIView):
    def post(self, request):
        try:
            request_serializer = UserSerializer(data=request.data)
            request_serializer.is_valid(raise_exception=True)
            user = request_serializer.save()
            res_data = user_data_with_jwt_token(UserSerializer(user).data, user)
            return success_response(data=res_data, success_message=LOGIN_API_SUCCESS)
        except Exception as ex:
            return failure_response(
                failure_message=str(ex),
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class LoginUserAPIView(APIView):
    def post(self, request):
        request_serializer = LoginRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        email = request_serializer.validated_data["email"]
        password = request_serializer.validated_data["password"]

        user = authenticate(request, username=email, password=password)

        if not user:
            return failure_response(
                failure_message=INCORRECT_EMAIL_OR_PASSWORD,
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        serialized_user = UserSerializer(user).data
        data = user_data_with_jwt_token(serialized_user, user)
        return success_response(data=data, success_message=LOGIN_API_SUCCESS)
