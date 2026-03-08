from django.db import models
from django.db.models import F


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low",    "Low"),
        ("medium", "Medium"),
        ("high",   "High"),
    ]

    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date    = models.DateField(null=True, blank=True)
    priority    = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    completed   = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["completed", F("due_date").asc(nulls_last=True), "-priority"]

    def __str__(self):
        return self.title
