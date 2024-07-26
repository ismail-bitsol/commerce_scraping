from django.db import models

class Website(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.CharField(max_length=255, default="$ 0.0")
    reviews = models.TextField()
    product_url = models.URLField()
    image_url = models.URLField()
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    sentiment_score = models.FloatField(default=0.5)
    sentiment_label = models.CharField(max_length=255, default="Neutral")
    keyword = models.CharField(max_length=255)  # Add this field

    def __str__(self):
        return f"Review for {self.name}"
