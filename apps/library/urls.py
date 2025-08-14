from django.urls import path, include
from apps.library.routers import router

urlpatterns = [
    path("api/", include(router.urls)),
]
