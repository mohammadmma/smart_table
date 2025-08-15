from rest_framework.routers import DefaultRouter
from .views import SensorDataViewSet

router = DefaultRouter()
router.register(r'sensor-data', SensorDataViewSet)

urlpatterns = router.urls
