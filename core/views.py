from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
import requests

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

@api_view(['POST'])
def incoming_data(request):
    token = request.headers.get('CL-X-TOKEN')
    if not token:
        return Response({"message": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        account = Account.objects.get(app_secret_token=token)
    except Account.DoesNotExist:
        return Response({"message": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data
    if request.method == 'GET' and not isinstance(data, dict):
        return Response({"message": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

    destinations = account.destinations.all()
    for destination in destinations:
        headers = destination.headers
        method = destination.http_method.lower()
        url = destination.url

        if method == 'get':
            response = requests.get(url, params=data, headers=headers)
        elif method == 'post':
            response = requests.post(url, json=data, headers=headers)
        elif method == 'put':
            response = requests.put(url, json=data, headers=headers)

        # Handle response if needed

    return Response({"message": "Data sent to destinations"}, status=status.HTTP_200_OK)

