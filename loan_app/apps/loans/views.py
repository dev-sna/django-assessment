from re import T
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from loan_app.apps.loans.models import Loan
from loan_app.apps.loans.serializers import (
    LoansSerializer,
    CreateLoanRequestSerializer,
    PayLoanRequestSerializer,
    UpdateLoanRequestSerializer
)
from loan_app.apps.utils.constants import (
    LOAN_REQUEST_CREATION_SUCCESS,
    LOAN_PAYMENT_SUCCESS,
    LOAN_STATUS_UPDATE_SUCCESS
)
from loan_app.apps.utils.response_format import failure_response, success_response


class LoansApi(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return LoansSerializer

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)

    def list(self, request):
        loans = Loan.objects.filter(user=request.user)
        serializer = LoansSerializer(loans, many=True)
        return success_response(data=serializer.data, status_code=status.HTTP_200_OK)

    def create(self, request):
        request.data["user"] = request.user.id
        request_serializer = CreateLoanRequestSerializer(data=request.data)
        
        request_serializer.is_valid(raise_exception=True)
        request_serializer.save()

        response_data = request_serializer.data
        return success_response(
            data=response_data, success_message=LOAN_REQUEST_CREATION_SUCCESS
        )

    @action(detail=False, methods=["POST"])
    def pay_loan(self, request):
        try:
            request.data["user"] = request.user.id
            loan_id = request.data.get("id")
            loan = Loan.objects.filter(id=loan_id).first()
            request_serializer = PayLoanRequestSerializer(
                instance=loan, data=request.data
            )
            request_serializer.is_valid(raise_exception=True)
            request_serializer.save()

            return success_response(
                data=request_serializer.data, status_code=status.HTTP_200_OK, success_message=LOAN_PAYMENT_SUCCESS
            )
        except Exception as ex:
            return failure_response(
                failure_message=str(ex), status_code=status.HTTP_400_BAD_REQUEST
            )


class AdminView(APIView):
    permission_classes = [IsAdminUser,IsAuthenticated,]

    def get(self, request):
        queryset = Loan.objects.all()
        serializer = LoansSerializer(queryset)
        return success_response(data=serializer.data, status_code=status.HTTP_200_OK)

    def post(self, request):
        loan_id = request.data.get("id")
        loan = Loan.objects.filter(id=loan_id).first()
        request_serializer = UpdateLoanRequestSerializer(
            instance=loan, data=request.data
        )
        request_serializer.is_valid(raise_exception=True)
        request_serializer.save()
        return success_response(
            data=request_serializer.data, status_code=status.HTTP_200_OK, success_message=LOAN_STATUS_UPDATE_SUCCESS
        )
