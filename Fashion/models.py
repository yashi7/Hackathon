from django.db import models
import uuid
from django.utils import timezone



class new_user(models.Model):
    u_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    Type=models.CharField(max_length=200)
    def __str__(self):
        return self.username



from django.db import models

class Restaurant(models.Model):
    location = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    cuisine = models.TextField()
    rating = models.FloatField()
    votes = models.IntegerField()
    cost = models.FloatField()

    def __str__(self):
        return f"{self.locality} - {self.city} (Rating: {self.rating})"


class Event(models.Model):
    type_of_food = models.CharField(max_length=255)
    number_of_guests = models.IntegerField()
    event_type = models.CharField(max_length=100)
    quantity_of_food = models.FloatField()
    storage_conditions = models.CharField(max_length=100)
    purchase_history = models.CharField(max_length=100)
    seasonality = models.CharField(max_length=100)
    preparation_method = models.CharField(max_length=100)
    geographical_location = models.CharField(max_length=100)
    pricing = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.event_type} - {self.geographical_location}"
    
class NGO(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_info = models.TextField()

    def __str__(self):
        return self.name

class Transaction(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="transactions")
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE, related_name="transactions")
    amount_of_food_donated = models.FloatField()  # in kilograms
    donation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.restaurant.locality} -> {self.ngo.name} ({self.amount_of_food_donated} kg)"
    
class CurrentBalance(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, null=True, blank=True, related_name="balance")
    ngo = models.OneToOneField(NGO, on_delete=models.CASCADE, null=True, blank=True, related_name="balance")
    current_capacity = models.FloatField(null=True, blank=True)  # for restaurants
    current_requirement = models.FloatField(null=True, blank=True)  # for NGOs

    def __str__(self):
        if self.restaurant:
            return f"Restaurant: {self.restaurant.locality} (Capacity: {self.current_capacity} kg)"
        elif self.ngo:
            return f"NGO: {self.ngo.name} (Requirement: {self.current_requirement} kg)"
        return "Balance Record"

