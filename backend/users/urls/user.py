from users.routers import CustomRouter
from users.views import CustomUserViewSet

app_name = 'users'

router = CustomRouter(trailing_slash=False)

router.register('users', CustomUserViewSet, basename='users')

urlpatterns = router.urls
