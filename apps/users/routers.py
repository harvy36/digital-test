from rest_framework import routers
from apps.users.apis import MemberViewSet, LoanViewSet, LoginView

router = routers.DefaultRouter()
router.register(r"members", MemberViewSet)
router.register(r"loans", LoanViewSet)
