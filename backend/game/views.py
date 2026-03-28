from django.shortcuts import render
from django.http import JsonResponse
from datetime import date
from .models import Puzzle


def health_check(request):
    """Return a JSON response confirming the backend is running."""

    return JsonResponse({"status": "ok"})


def today_puzzle(request):
    """Return brief JSON data for today's puzzle."""

    today = date.today()
    puzzle = Puzzle.objects.filter(date=today).first()
    match puzzle:
        case None:
            return JsonResponse({
                "exists": False,
                "date": str(today)},
                status=404)
        case _:
            return JsonResponse(
                {
                    "exists": True,
                    "id": puzzle.id,
                    "date": str(puzzle.date)}
            )
