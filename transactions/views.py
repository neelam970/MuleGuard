from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render,get_object_or_404

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionListCreateAPIView(APIView):

    def get(self, request):
        transactions = Transaction.objects.all().order_by("-transaction_date")

        serializer = TransactionSerializer(
            transactions,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TransactionDetailAPIView(APIView):

    def get(self, request, pk):

        try:
            transaction = Transaction.objects.get(pk=pk)

        except Transaction.DoesNotExist:

            return Response(
                {"error": "Transaction not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TransactionSerializer(transaction)

        return Response(serializer.data)

    def put(self, request, pk):

        try:
            transaction = Transaction.objects.get(pk=pk)

        except Transaction.DoesNotExist:

            return Response(
                {"error": "Transaction not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TransactionSerializer(
            transaction,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):

        try:
            transaction = Transaction.objects.get(pk=pk)

        except Transaction.DoesNotExist:

            return Response(
                {"error": "Transaction not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TransactionSerializer(
            transaction,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        try:
            transaction = Transaction.objects.get(pk=pk)

        except Transaction.DoesNotExist:

            return Response(
                {"error": "Transaction not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        transaction.delete()

        return Response(
            {"message": "Transaction deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


def transaction_page(request):
    return render(
        request,
        "transactions/transactions.html"
    )
def transaction_detail(request, pk):
    transaction = get_object_or_404(
        Transaction,
        pk=pk
    )

    return render(
        request,
        "transactions/transaction_detail.html",
        {"transaction": transaction}
    )