from django.urls import path,include
from rest_framework import routers
from datacore import views

router = routers.DefaultRouter()
router.register(r'companies',views.CompanyViewSet , 'companies')

urlpatterns = [
    path('api/v1/',include(router.urls))
]
    
