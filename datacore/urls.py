from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from datacore import views
from .views import LoginWithGoogle
from rest_framework_simplejwt.views import TokenVerifyView

especialidades_por_facultad = views.EspecialidadViewSet.as_view(
    {"get": "list_por_facultad"}
)

router = routers.DefaultRouter()

router.register(r"facultades", views.FacultadViewSet, "facultades")
router.register(r"especialidades", views.EspecialidadViewSet, "especialidades")
router.register(r"estadosPersonas", views.EstadoPersonaViewSet, "estadosPersonas")
router.register(r"cpus", views.CPUViewSet, "cpus")
router.register(r"gpus", views.GPUViewSet, "gpus")
router.register(r"users", views.UsersViewSet, "users")
router.register(r"solicitudes", views.SolicitudViewSet, "solicitudes")
router.register(r"hostorial", views.HistorialViewSet, "hostorial")


urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("docs/", include_docs_urls(title="DataCore API")),
    path(
        "api/v1/especialidades/porFacultad/<int:id_facultad>/",
        especialidades_por_facultad,
        name="especialidadesPorFacultad",
    ),
    path('api/v1/crear-solicitud/', views.crear_solicitud, name='crear_solicitud'),
    path('api/v1/login-with-google/', LoginWithGoogle.as_view(), name = 'login-with-google'),

    # Hitstorial

    # Solicitudes
]
