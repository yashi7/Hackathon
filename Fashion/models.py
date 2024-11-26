from django.db import models
import uuid
from django.utils import timezone
Type=(
    ("Apparel","Apparel"),
    ("Footwear","Footwear"),
    ("Accessories","Accessories"),
)

class user_new(models.Model):
    Username = models.CharField(max_length=200)
    Email = models.CharField(max_length=200)
    

class user_files(models.Model):
    image = models.ImageField(upload_to='user_images')
    gender= models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    color=models.CharField(max_length=200)
    occassion=models.CharField(max_length=200)


class new_user(models.Model):
    u_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    Gender=models.CharField(max_length=200)
    def __str__(self):
        return self.username


class Wardrobe(models.Model):
    w_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique identifier for each image
    u_id = models.ForeignKey(new_user, on_delete=models.CASCADE)  # Link to the user (ForeignKey)
    img_path = models.ImageField(upload_to='user_images')
    image_name = models.CharField(max_length=1000)

    def __str__(self):
        return self.image_name


class Rec(models.Model):
    rec_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique ID for recommendation
    u_id = models.ForeignKey(new_user, on_delete=models.CASCADE)  # Link to the user (ForeignKey)
    c_id = models.ForeignKey('Category', on_delete=models.CASCADE)  # Link to a category (ForeignKey)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Recommendation {self.rec_id} for User {self.u_id}"

class Category(models.Model):
    c_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique ID for category
    w_id = models.ForeignKey(Wardrobe, on_delete=models.CASCADE)  # Link to wardrobe (ForeignKey)
    u_id = models.ForeignKey(new_user, on_delete=models.CASCADE)  # Link to user (ForeignKey)
    Category = models.CharField(max_length=200)
    Color = models.CharField(max_length=200)
    Occassion = models.CharField(max_length=200)

    def __str__(self):
        return f"Category {self.Category} for {self.Occassion}"

class Favourites(models.Model):
    f_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique ID for favorite
    u_id = models.ForeignKey(new_user, on_delete=models.CASCADE)  # Link to user (ForeignKey)
    c_id = models.ForeignKey(Category, on_delete=models.CASCADE)  # Link to category (ForeignKey)

    def __str__(self):
        return f"Favorite {self.f_id} for User {self.u_id}"
from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=255)
    option_1 = models.CharField(max_length=100)
    option_2 = models.CharField(max_length=100)
    option_3 = models.CharField(max_length=100)
    option_4 = models.CharField(max_length=100)

class UserAnswer(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)

