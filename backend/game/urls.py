from django.urls import path
from .views import health_check, today_puzzle, submit_guess

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("puzzle/today/", today_puzzle, name="today-puzzle"),
    path("puzzle/today/guess/", submit_guess, name="submit-guess"),
]