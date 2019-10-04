from rest_framework.serializers import (
	EmailField,
	CharField,
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField,
)

from users_account.models import (
	diary,
	bpdata,
	bpinputs,
)

class FetchClientBPDataSerializer(ModelSerializer):

	class Meta:
		model = bpdata
		fields = [
			'average_SBP_per_upload',
			'average_DBP_per_upload',
			'average_pulse_rate_per_upload',
			'blood_pressure_status',
			'datetime'
		]