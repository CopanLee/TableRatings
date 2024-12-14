from django.db import models
from django.db.models import Avg

from restaurant.models import Restaurant

# Create your models here.
class Reviews(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    rating = models.IntegerField()
    review = models.TextField()
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)
    reviewer = models.ForeignKey('users.Users', on_delete=models.CASCADE)

    @classmethod
    def update_average_rating(cls, restaurant_id):
        avg_rating = cls.objects.filter(restaurant_id=restaurant_id).aggregate(Avg('rating'))['rating__avg']
        # Assuming there is a Restaurant model with an average_rating field
        Restaurant.objects.filter(id=restaurant_id).update(rating=avg_rating)
