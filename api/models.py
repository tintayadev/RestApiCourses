from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    duration_weeks = models.IntegerField()
    