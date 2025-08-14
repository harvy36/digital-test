# import routers
from rest_framework import routers
from rest_framework import viewsets
from apps.library.models import Book
from apps.library.apis import BookViewSet
from apps.library.serializers import BookSerializer

router = routers.DefaultRouter()
router.register(r"books", BookViewSet)
