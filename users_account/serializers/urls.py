from django.urls import path

from .views import (
    ClientBPDataListAPIView,
    UploadClientBloodPressureTestResultsAPIView
)

urlpatterns = [
    path(r'datalist/<int:user_id>/', ClientBPDataListAPIView.as_view()),
    path(r'upload-test', UploadClientBloodPressureTestResultsAPIView.as_view()),
]