from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.library.models import Book
from apps.library.serializers import BookSerializer
from datetime import datetime


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "author": ["icontains"],
        "published_date": ["gte", "lte"],
    }
    page_size = 10

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        author = request.query_params.get("author", None)
        published_date_after = request.query_params.get("published_date_after", None)
        published_date_before = request.query_params.get("published_date_before", None)
        page_size = request.query_params.get("page_size", self.page_size)

        if int(page_size) > 0:
            self.page_size = int(page_size)

        # Validation
        if (
            published_date_after
            and published_date_before
            and published_date_after > published_date_before
        ):
            return Response(
                {
                    "error": "published_date_after must be earlier than published_date_before"
                },
                status=400,
            )

        # Validate date format YYYY-MM-DD
        if published_date_after and not self.is_valid_date_format(published_date_after):
            return Response(
                {"error": "published_date_after must have format YYYY-MM-DD"},
                status=400,
            )
        if published_date_before and not self.is_valid_date_format(
            published_date_before
        ):
            return Response(
                {"error": "published_date_before must have format YYYY-MM-DD"},
                status=400,
            )

        if author:
            queryset = queryset.filter(author__icontains=author)
        if published_date_after:
            queryset = queryset.filter(published_date__gte=published_date_after)
        if published_date_before:
            queryset = queryset.filter(published_date__lte=published_date_before)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def is_valid_date_format(self, date_str):

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
