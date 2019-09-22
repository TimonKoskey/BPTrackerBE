from django.urls import path
from .views import (
	RegisterClientAPIView,
	LoginClientAPIView,
)

urlpatterns = [
    path(r'login', LoginClientAPIView.as_view()),
	path(r'register', RegisterClientAPIView.as_view()),
]
