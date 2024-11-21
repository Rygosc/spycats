import requests
from django.db import models
from django.core.exceptions import ValidationError


# Модель для SpyCat
class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def clean(self):
        breed = self.breed
        response = requests.get(f"https://api.thecatapi.com/v1/breeds/search?q={breed}")
        if not response.json():
            raise ValidationError(f"Invalid breed: {breed}")


# Модель для Target
class Target(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField()
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Модель для Mission
class Mission(models.Model):
    spy_cat = models.ForeignKey(SpyCat, on_delete=models.CASCADE)
    targets = models.ManyToManyField(Target)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Mission for {self.spy_cat.name}"

    def update_targets(self, target_id, complete=None, notes=None):
        try:
            target = self.targets.get(id=target_id)
            if target.complete:
                raise ValidationError("Cannot update target, it is already completed.")
            if complete is not None:
                target.complete = complete
            if notes is not None:
                target.notes = notes
            target.save()
        except Target.DoesNotExist:
            raise ValidationError("Target not found.")
