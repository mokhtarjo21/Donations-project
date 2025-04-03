from django.db import models
from users.models import User
import os

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        # this is just for the admin panel ;)
        verbose_name_plural = "Categories"


class Tag(models.Model):

    name = models.CharField(max_length=50, unique=True) # to use in searching
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """
    The main project model for fundraising campaigns
    """
    # Basic information
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    details = models.TextField()
    
    # Category and tags
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    
    # Funding information
    target = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                help_text="Target amount to raise")
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Time information
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    
    def __str__(self):
        return self.title
    
    @property
    def funding_percentage(self):
        """Calculate what percentage of the target has been funded"""
        if self.target == 0:
            return 0
        return (self.current_amount / self.target) * 100
    
    @property
    def can_be_cancelled(self):
        """Check if project can be cancelled (less than 25% funded)"""
        return self.funding_percentage < 25


class ProjectPictures(models.Model):
    """
    Images for projects (multiple per project)
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/images')
    
    def __str__(self):
        return f"Image for {self.project.title}"
    
    # performing method overriding on delete() to delete the phisical image files in media 
    def delete(self, *args, **kwargs):
        """
        when we delete a Project instance,
        the delete() method will be called for each related ProjectPictures record

        """
        if self.image:
            # Get the path to the image file
            image_path = self.image.path
            # Check if the file exists and delete it
            if os.path.isfile(image_path):
                os.remove(image_path)
        super().delete(*args, **kwargs)
