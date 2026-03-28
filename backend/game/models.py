from django.db import models

class Puzzle(models.Model):
    """Stores a daily puzz."""

    date = models.DateField()
    solution_text = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.date}: {self.solution_text}"