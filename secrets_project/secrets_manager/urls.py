from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.SecretCreateListView.as_view(), name='secret-list'),
    path('auth/', include([
        path('login/', views.LoginView.as_view(), name='login'),
        path('logout/', views.LogoutView.as_view(), name='logout'),
    ])),
]

