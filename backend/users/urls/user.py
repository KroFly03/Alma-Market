from rest_framework.routers import SimpleRouter

from users.routers import CustomRouter
from users.views import CustomUserViewSet

router = CustomRouter()

router.register('', CustomUserViewSet, basename="users")

urlpatterns = router.urls
