from rest_framework.serializers import (
	EmailField,
	CharField,
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField,
)
from authentication.models import (
    locations,
    clients,
    emergy_contacts
)
from django.contrib.auth import get_user_model

USER = get_user_model()

class CreateUserSerializer(ModelSerializer):

    class Meta:
        model = USER
        fields = [
			# "username",
			"first_name",
			"last_name",
			"email",
			"password"
        ]

        extra_kwargs={
            "password":{"write_only":True}
            }

    def create(self, validated_data):

        user_obj = USER(
        	# username = validated_data['username'],
			first_name = validated_data['first_name'],
			last_name = validated_data['last_name'],
			email = validated_data['email']
        )

        user_obj.set_password(validated_data['password'])
        user_obj.save()
        return user_obj

class CreateLocationSerializer(ModelSerializer):
	class Meta:
		model=locations
		fields = [
			'county',
			'sub_county',
			'village_or_estate'
		]

	def create(self,validated_data):
		county = validated_data['county']
		sub_county = validated_data['sub_county']
		village_or_estate = validated_data['village_or_estate']

		location_obj = locations(
			county = county,
			sub_county = sub_county,
			village_or_estate = village_or_estate
		)

		location_obj.save()
		return location_obj

class ClientCreateSerializer(ModelSerializer):
	class Meta:
		model = clients
		fields = [
            'main_phone_number',
            'alt_phone_number',
            'age',
            'gender'
        ]
	def create(self, validated_data):
		main_phone_number = validated_data['main_phone_number']
		alt_phone_number = validated_data['alt_phone_number']
		age = validated_data['age']
		gender = validated_data['gender']

		app_client_obj = clients(
			main_phone_number = main_phone_number,
			alt_phone_number = alt_phone_number,
			age = age,
			gender = gender
		)
		app_client_obj.save()

		return app_client_obj

class GetUserDetailsSerializer(ModelSerializer):
	class Meta:
		model=USER
		fields=[
			'id',
			'first_name',
			'last_name',
			'email',
		]
