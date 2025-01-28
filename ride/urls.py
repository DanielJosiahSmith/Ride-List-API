from .views import RideViewSet,RideEventViewSet
from user.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'rides', RideViewSet, basename='ride')
router.register(r'ride_events', RideEventViewSet, basename='ride_event')
urlpatterns = router.urls