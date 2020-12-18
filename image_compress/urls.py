from django.urls import path
from . import views

urlpatterns = [
    path('get_image/<int:id_image>', views.get_image),
    path('random_image/', views.get_random_image)
]
