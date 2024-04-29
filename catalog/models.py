from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator

class Brand(models.Model):

    """Model representing a shoe brand."""
    name = models.CharField(
        max_length=25,
        unique=True,
        help_text="Enter a shoe brand (e.g. Nike, New Balance.)"
    )

    location = models.CharField(
        max_length=100,
        help_text="Enter where the shoe brand is located (USA, China...)"
    )

    brandId = models.IntegerField(
        unique=True,
        help_text="Enter a unique id for the shoe brand"
    )
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular brand instance."""
        return reverse('brand-detail', args=[str(self.brandId)])

class Tech(models.Model):

    """Model for specific techs."""

    AIR = "AR"
    FOAM = "FO"

    TYPE_OF_TECH = [
        (AIR, "Air"),
        (FOAM, "Foam"),
    ]
    
    techId = models.PositiveIntegerField(
        unique=True
    )

    name = models.CharField(
        max_length=30,
    )
    foamType = models.CharField(
        max_length=2,
        choices=TYPE_OF_TECH,
        default=None
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tech-detail', args=[str(self.id)])

class Shoe(models.Model):

    """Model representing a shoe."""

    name = models.CharField(
        max_length=50,
        unique=True
    )
    
    shoeId = models.IntegerField(
        unique=True
    )

    brand = models.ForeignKey('Brand', on_delete=models.RESTRICT, null=True)

    date_of_model = models.DateField(null=True, blank=True)

    lockdown = models.PositiveIntegerField(
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    traction = models.PositiveIntegerField(
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    comfort = models.PositiveIntegerField(
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    looks = models.PositiveIntegerField(
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    
    tech = models.ManyToManyField(
        Tech, help_text="Select tech for this shoe")
    def display_tech(self):
        """Create a string for the Tech. This is required to display tech in Admin."""
        return ', '.join(tech.name for tech in self.tech.all()[:8])

    display_tech.short_description = 'Tech'

    def __str__(self):
        """String for representing the model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('shoe-detail', args=[str(self.id)])


