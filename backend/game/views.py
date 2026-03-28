from django.shortcuts import render
from django.http import JsonResponse
from datetime import date
from .models import Puzzle


def health_check(request):
    """Return a JSON response confirming the backend is running."""

    return JsonResponse({"status": "ok"})