from django.db import models


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TouristDestination(models.Model):
    place_name = models.CharField(max_length=100)
    weather = models.CharField(max_length=100, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    google_map_link = models.URLField(null=True)
    description = models.TextField(null=True)
    main_image = models.ImageField(upload_to='tourist_destination_images/', null=True, blank=True)
    landmark = models.CharField(max_length=255, null=True)

    def save(self, *args, **kwargs):
        if self.state_id:
            self.state_name = State.objects.get(id=self.state_id).name
        if self.category_id:
            self.category_name = Category.objects.get(id=self.category_id).name
        super(TouristDestination, self).save(*args, **kwargs)

    def __str__(self):
        return self.place_name


class DestinationSubImage(models.Model):
    destination = models.ForeignKey(TouristDestination, related_name='sub_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='destination_images/')

    def __str__(self):
        return f"Sub Image for {self.destination.place_name}"


# Create your models here.
