from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from .models import Customer
from .serializers import CustomerSerializer



class CustomerListCreateAPIView(APIView):

    def get(self, request):
        customers = Customer.objects.all()

        serializer = CustomerSerializer(
            customers,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(
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


class CustomerDetailAPIView(APIView):

    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)

        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomerSerializer(customer)

        return Response(serializer.data)

    def put(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)

        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomerSerializer(
            customer,
            data=request.data
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
            customer = Customer.objects.get(pk=pk)

        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        customer.delete()

        return Response(
            {"message": "Customer deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    def patch(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)

        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomerSerializer(
            customer,
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
def customer_page(request):
    return render(
        request,
        "customers/customers.html"
    )
def customer_investigate(request, pk):
    customer = get_object_or_404(
        Customer,
        pk=pk
    )

    return render(
        request,
        "customers/investigate.html",
        {
            "customer": customer
        }
    )