from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
import json

from rest_framework.generics import (
	CreateAPIView,
	RetrieveUpdateAPIView,
	ListAPIView,
	RetrieveAPIView,
	)

from users_account.models import (
	diary,
	bpdata,
	bpinputs,
)

from authentication.models import (
    clients,
)

from .serializers import (
	FetchClientBPDataSerializer,
)

from django.contrib.auth import get_user_model

USER = get_user_model()

class ClientBPDataListAPIView (ListAPIView):
    serializer_class = FetchClientBPDataSerializer

    def get_queryset(self, *args, **kwargs):
    	user_id = self.kwargs['user_id']
    	user_obj = USER.objects.get(id=user_id)
    	print(user_obj.is_app_client)
    	if user_obj.is_app_client:
    		client_obj = clients.objects.get(user=user_obj)
    		client_bp_data = bpdata.objects.filter(client=client_obj)

    		return client_bp_data

class UploadClientBloodPressureTestResultsAPIView(APIView):
	def post(self, request, *args, **kwargs):
		request_data = request.data 
		blood_pressure_inputs = request_data['blood_pressure']
		client_mood = request_data['client_mood']

		total_sbp = 0
		total_dbp = 0
		total_pulse = 0
		count = 0
		bpinputs_objs_list = []

		for data in blood_pressure_inputs:
			count += 1
			total_sbp += data['SBP']
			total_dbp += data['DBP']
			total_pulse += data['pulse_rate']

			print(data)

			bpinputs_obj = bpinputs(
				systolic_blood_pressure=data['SBP'],
				diastolic_blood_pressure=data['DBP'],
				pulse_rate=data['pulse_rate'],
				upload_count=count,
				datetime=data['datetime']
				)

			# bpinputs_obj.save()
			bpinputs_objs_list.append(bpinputs_obj)

		average_sbp = total_sbp/count
		average_dbp = total_dbp/count
		average_pulse = total_pulse/count

		user_obj = USER.objects.get(id=request_data['users'])
		client_obj = clients.objects.get(user=user_obj)

		blood_pressure_status = ''

		if(average_sbp < 90 or average_dbp < 60):
			blood_pressure_status = 'Low'
		elif((average_sbp >=90 and average_sbp <=120) and (average_dbp >= 60 and average_dbp <= 80)):
			blood_pressure_status = 'Normal'
		elif((average_sbp > 120 and average_sbp <= 140) or (average_dbp > 80 and average_dbp <= 90)):
			blood_pressure_status = 'Elevated'
		elif(average_sbp > 140 or average_dbp > 90):
			blood_pressure_status = 'High'
		else:
			blood_pressure_status = None

		bpdata_obj = bpdata(
			client=client_obj,
			average_SBP_per_upload=average_sbp,
			average_DBP_per_upload=average_dbp,
			average_pulse_rate_per_upload=average_pulse,
			blood_pressure_status=blood_pressure_status
			)

		bpdata_obj.save()

		for obj in bpinputs_objs_list:
			obj.average_of_inputs=bpdata_obj
			obj.save()

		bpdata_obj_list = bpdata.objects.filter(client=client_obj)

		bpdata_serializer = FetchClientBPDataSerializer(bpdata_obj_list,many=True).data 
		return Response(bpdata_serializer)

