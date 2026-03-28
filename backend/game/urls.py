from django.urls import path
from .views import health_check, today_puzzle

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("puzzle/today/", today_puzzle, name="today-puzzle"),
]