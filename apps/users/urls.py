from django.urls import path, include
from apps.users.routers import router

urlpatterns = [
    path("api/", include(router.urls)),
]
