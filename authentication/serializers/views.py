from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from rest_framework_jwt.settings import api_settings
from django.core.mail import send_mail
from rest_framework.parsers import MultiPartParser
import json
from django.contrib.auth import get_user_model

from rest_framework.generics import (
	CreateAPIView,
	RetrieveUpdateAPIView,
	ListAPIView,
	RetrieveAPIView,
	)

from authentication.models import (
    locations,
    clients,
    emergy_contacts
)

from .serializers import (
    CreateUserSerializer,
    ClientCreateSerializer,
	CreateLocationSerializer
)

USER=get_user_model()
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

class RegisterClientAPIView(ObtainJSONWebToken):

    def post(self, request, *args, **kwargs):
        request_data = request.data

        user_class_data = {
            # 'username': request_data['username'],
            'first_name': request_data['first_name'],
            'last_name': request_data['last_name'],
            'email': request_data['email'],
            'password': request_data['password']
        }

        app_client_class_data = {
            'main_phone_number': request_data['main_phone_number'],
            'alt_phone_number': request_data['alt_phone_number'],
            'age': request_data['age'],
            'gender': request_data['gender']
        }

        client_location = {
		'county': request_data['county'],
		'sub_county': request_data['sub_county'],
		'village_or_estate': request_data['village_or_estate']
		}

        user_class_serializer = CreateUserSerializer(data=user_class_data)
        if user_class_serializer.is_valid():
            user_object = user_class_serializer.create(user_class_serializer.validated_data)

            location_serializer = CreateLocationSerializer(data=client_location)
            if location_serializer.is_valid():
                location_obj = location_serializer.create(location_serializer.validated_data)

                app_client_class_serializer = ClientCreateSerializer(data=app_client_class_data)
                if app_client_class_serializer.is_valid():
	                app_client_object = app_client_class_serializer.create(app_client_class_serializer.validated_data)
	                app_client_object.user = user_object
	                app_client_object.save()

	                user_login_cred = {
	                    'email': user_class_serializer.validated_data['email'],
	                    'password': user_class_serializer.validated_data['password']
	                }

	                login_serializer = ObtainJSONWebToken.get_serializer(self,data=user_login_cred)
	                if login_serializer.is_valid():
	                    user = login_serializer.object.get('user')
	                    token = login_serializer.object.get('token')

	                    response_data = jwt_response_payload_handler(token, user, request)
	                    response = Response(response_data)
	                    return response
	                return Response(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(app_client_class_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(location_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_class_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginClientAPIView(ObtainJSONWebToken):
	def post(self, request, *args, **kwargs):
		request_data = request.data
		serializer = ObtainJSONWebToken.get_serializer(self,data=request_data)

		if serializer.is_valid():
			user = serializer.object.get('user') or request.user
			token = serializer.object.get('token')
			response_data = jwt_response_payload_handler(token,user,request)
			response = Response(response_data)
			print(api_settings.JWT_AUTH_COOKIE)
			return response
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
