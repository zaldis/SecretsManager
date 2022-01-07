from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.SecretCreateListView.as_view(), name='secret-list'),
]

