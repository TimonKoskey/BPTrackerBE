from django.contrib import admin
from .models import (
	diary,
	bpdata,
	bpinputs,
)


admin.site.register(diary)
admin.site.register(bpdata)
admin.site.register(bpinputs)
