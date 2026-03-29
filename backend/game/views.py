import json
from django.http import JsonResponse
from datetime import date
from .models import Puzzle

def get_todays_puzzle():
    """Return today's puzzle."""
    return Puzzle.objects.filter(date=date.today()).order_by("-id").first()

def get_todays_puzzle_solution():
    """Return the solution to today's puzzle."""
    return get_todays_puzzle().solution_text

def get_guess_string(request):
    """
    (1) Takes the request and pulls the body with request.body. 
    (2) Uses json.loads() on that to translate into Python object (dict for this type of JSON). 
    (3) Uses dict.get() method to get the pair from the key/value guess pair. 
    (4) Cleans the string with .strip() and .lower(). 
    (5) Returns the cleaned string guess from the request. 
    """
    return json.loads(request.body or "{}").get("guess").strip().lower()

def screen_guess(guess: str):
    """Screens guess for possible formatting issues. Returns errors if so."""

    # Error if guess isn't 10 letters long exactly.
    if len(guess) != 10:
        return JsonResponse(
            {"error": "Guess must be exactly 10 letters."},
            status=400,
        )

    # Error if guess isn't fully alphabetical. 
    if not guess.isalpha():
        return JsonResponse(
            {"error": "Guess must contain letters only."},
            status=400,
        )

def health_check(request):
    """Return a JSON response confirming the backend is running."""

    return JsonResponse({"status": "ok"})


def today_puzzle(request):
    """Return brief JSON data for today's puzzle."""

    # Set today to today's date with the datetime module. 
    today = date.today()

    # Set puzzle to the newest puzzle in the DB from today's date. 
    puzzle = Puzzle.objects.filter(date=today).order_by("-id").first()
    match puzzle:

        # If no puzzle exists for today, return a 404 JSON response.
        case None:
            return JsonResponse(
                {
                    "exists": False,
                    "date": str(today)
                },
                status=404)

        # If a puzzle exists, return some metadata. 
        case _:
            return JsonResponse(
                {
                    "exists": True,
                    "id": puzzle.id,
                    "date": str(puzzle.date)
                }
            )

def submit_guess(request):
    """Accept a guess for today's puzzle and return per-letter feedback."""

    # Only allow POST because this endpoint is meant to receive submitted data.
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed."},
            status=405,
        )
    
    # The guess
    guess = get_guess_string(request)

    # The solution
    solution = get_todays_puzzle_solution()

    # Screen the guess for potential formatting issues
    screen_guess(guess)
    
    # NO LOWER !!

    # Looks up today's puzzle (still prefers newest ID if dupes). 
    today = date.today()
    puzzle = Puzzle.objects.filter(date=date.today()).order_by("-id").first()

    # Error if there's no puzzle today. 
    if puzzle is None:
        return JsonResponse(
            {"error": "No puzzle exists for today."},
            status=404,
        )

    # Normalize the stored solution and prepare the feedback structures.

    # Clean solution string 
    solution = puzzle.solution_text.lower()
    result = ["absent"] * len(guess)
    remaining_letters = {}

    # First pass: mark exact matches as correct and count leftover solution letters.
    for i, letter in enumerate(solution):
        if guess[i] == letter:
            result[i] = "correct"
        else:
            remaining_letters[letter] = remaining_letters.get(letter, 0) + 1

    # Second pass: mark misplaced letters as present only if some are still unused.
    for i, letter in enumerate(guess):
        if result[i] == "correct":
            continue

        if remaining_letters.get(letter, 0) > 0:
            result[i] = "present"
            remaining_letters[letter] -= 1

    # Return the scored guess in JSON so the frontend can render the feedback.
    return JsonResponse(
        {
            "guess": guess,
            "length": len(guess),
            "result": result,
            "is_correct": guess == solution,
        }
    )
