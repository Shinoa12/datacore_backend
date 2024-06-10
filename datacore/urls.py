from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from datacore import views
from .views import LoginWithGoogle
from rest_framework_simplejwt.views import TokenVerifyView

especialidades_por_facultad = views.EspecialidadViewSet.as_view(
    {"get": "list_por_facultad"}
)

getAllSolicitudes = views.SolicitudViewSet.as_view({"get": "list_por_usuario"})

getSolicitudDetalle = views.SolicitudViewSet.as_view({"get": "detalle_solicitud"})

getSolicitudResultado = views.ArchivoViewSet.as_view({"get": "descargar"})


router = routers.DefaultRouter()

router.register(r"facultades", views.FacultadViewSet, "facultades")
router.register(r"especialidades", views.EspecialidadViewSet, "especialidades")
router.register(r"estadosPersonas", views.EstadoPersonaViewSet, "estadosPersonas")
router.register(r"cpus", views.CPUViewSet, "cpus")
router.register(r"gpus", views.GPUViewSet, "gpus")
router.register(r"users", views.UsersViewSet, "users")
router.register(r"solicitudes", views.SolicitudViewSet, "solicitudes")
router.register(r"historial", views.HistorialViewSet, "historial")
router.register(r"archivos", views.ArchivoViewSet, "archivos")
router.register(r"herramientas", views.HerramientaViewSet, "herramientas")
router.register(r"librerias", views.LibreriaViewSet, "librerias")

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
        getSolicitudResultado,
        name="getSolicitudResultado",
    ),
    path(
        "api/v1/cancelarSolicitud/",
        views.cancelarSolicitud,
        name="cancelarSolicitud",
    ),
]
