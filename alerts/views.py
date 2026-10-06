from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render,get_object_or_404
from .models import Alert
from .serializers import AlertSerializer


class AlertListCreateAPIView(APIView):

    def get(self, request):
        alerts = Alert.objects.all().order_by("-created_at")

        serializer = AlertSerializer(
            alerts,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = AlertSerializer(
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


class AlertDetailAPIView(APIView):

    def get(self, request, pk):

        try:
            alert = Alert.objects.get(pk=pk)

        except Alert.DoesNotExist:

            return Response(
                {"error": "Alert not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AlertSerializer(alert)

        return Response(serializer.data)

    def patch(self, request, pk):

        try:
            alert = Alert.objects.get(pk=pk)

        except Alert.DoesNotExist:

            return Response(
                {"error": "Alert not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AlertSerializer(
            alert,
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
def alert_page(request):
    return render(request, "alerts/alerts.html")

def alert_detail_page(request, pk):
    alert = get_object_or_404(Alert, pk=pk)

    return render(
        request,
        "alerts/alert_detail.html",
        {"alert": alert},
    )