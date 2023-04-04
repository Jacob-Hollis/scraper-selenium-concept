from django.db import models

class Listing(models.Model):
    listing_id = models.CharField(unique=True, max_length=255, null=False)
    title = models.CharField(max_length=255, null=False)
    price = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)