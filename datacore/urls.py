from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from datacore import views
from .views import LoginWithGoogle
from .views import enviar_email_view
from .views import requests_by_month, requests_by_resource, requests_by_specialty, average_processing_duration,solicitudes_creadas,solicitudes_en_proceso,solicitudes_finalizadas
from rest_framework_simplejwt.views import TokenVerifyView

especialidades_por_facultad = views.EspecialidadViewSet.as_view(
    {"get": "list_por_facultad"}
)

getAllSolicitudes = views.SolicitudViewSet.as_view({"get": "list_por_usuario"})

getSolicitudDetalle = views.SolicitudViewSet.as_view({"get": "detalle_solicitud"})


router = routers.DefaultRouter()

router.register(r"facultades", views.FacultadViewSet, "facultades")
router.register(r"especialidades", views.EspecialidadViewSet, "especialidades")
router.register(r"estadosPersonas", views.EstadoPersonaViewSet, "estadosPersonas")
router.register(r"cpus", views.CPUViewSet, "cpus")
router.register(r"gpus", views.GPUViewSet, "gpus")
router.register(r"users", views.UsersViewSet, "users")
router.register(r"solicitudes", views.SolicitudViewSet, "solicitudes")
router.register(r"historial", views.HistorialViewSet, "historial")
router.register(r"herramientas", views.HerramientaViewSet, "herramientas")
router.register(r"librerias", views.LibreriaViewSet, "librerias")
router.register(r"ajustes", views.AjustesViewSet, "ajustes")

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("docs/", include_docs_urls(title="DataCore API")),
    path(
        "api/v1/especialidades/porFacultad/<int:id_facultad>/",
        especialidades_por_facultad,
        name="especialidadesPorFacultad",
    ),
    path("api/v1/crear-solicitud/", views.crear_solicitud, name="crear_solicitud"),
    path(
        "api/v1/login-with-google/", LoginWithGoogle.as_view(), name="login-with-google"
    ),
    # Historial
    # path('api/v1/getAllHistorial/', views.list_historial, name = 'getAllHistorial'),
    # Solicitudes
    path(
        "api/v1/getAllSolicitudes/<int:id_user>/",
        getAllSolicitudes,
        name="getAllSolicitudes",
    ),
    path(
        "api/v1/getSolicitudDetalle/<int:id_solicitud>/",
        getSolicitudDetalle,
        name="getSolicitudDetalle",
    ),
    path(
        "api/v1/getSolicitudResultado/<int:id_solicitud>/",
        views.descargar,
        name="getSolicitudResultado",
    ),
    path(
        "api/v1/cancelarSolicitud/<int:id_solicitud>/",
        views.cancelarSolicitud,
        name="cancelarSolicitud",
    ),
    path(
        "api/v1/InicioProcesamientoSolicitud/<int:id_solicitud>/",
        views.inicioProcesamientoSolicitud,
        name="inicioProcesamientoSolicitud",
    ),
    path(
        "api/v1/FinProcesamientoSolicitud/",
        views.finProcesamientoSolicitud,
        name="finProcesamientoSolicitud",
    ),
    path("api/v1/enviar-email/", enviar_email_view, name="enviar_email"),
    path('api/v1/requests_by_month/', requests_by_month),
    path('api/v1/requests_by_resource/', requests_by_resource),
    path('api/v1/requests_by_specialty/', requests_by_specialty),
    path('api/v1/average_processing_duration/', average_processing_duration),
    path('api/v1/solicitudes_creadas/', solicitudes_creadas, name='solicitudes_creadas'),
    path('api/v1/solicitudes_en_proceso/', solicitudes_en_proceso, name='solicitudes_en_proceso'),
    path('api/v1/solicitudes_finalizadas/', solicitudes_finalizadas, name='solicitudes_finalizadas'),
]
