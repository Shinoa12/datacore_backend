from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from datacore import views

router = routers.DefaultRouter()
router.register(r"facultades", views.FacultadViewSet, "facultades")
router.register(r"especialidades", views.EspecialidadViewSet, "especialidades")
router.register(r"estadosPersonas", views.EstadoPersonaViewSet, "estadosPersonas")
router.register(r"cpus", views.CPUViewSet, "cpus")
router.register(r"gpus", views.GPUViewSet, "gpus")

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("docs/", include_docs_urls(title="DataCore API")),
    path(
        "api/v1/especialidades/porFacultad/<int:id_facultad>/",
        views.EspecialidadViewSet.as_view({"get": "getEspecialidadesPorFacultad"}),
        name="especialidadesPorFacultad",
    ),
]
