from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from projects.models import Project
# for validation below
from django.core.exceptions import ValidationError  


class Donation(models.Model):
    """
    Donations made by users to projects
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.fname} {self.user.lname} donated {self.amount} to {self.project.title}"
    
    def save(self, *args, **kwargs):
        """Override save to update project's current amount when donation is added"""
        is_new = self.pk is None  # Check if this is a new donation
        super().save(*args, **kwargs)
        
        if is_new:  # Only update the project amount for new donations in order to prevent addint the money again if the user updated the project name or time for example 
            self.project.current_amount += self.amount
            self.project.save()


class Comment(models.Model):
    """
    Comments on projects with optional replies
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Ya mokhtar this approach is much simpler in implementing replies, Reply is just a comment on another comment ;)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    def __str__(self):
        return f"Comment by {self.user.fname} {self.user.lname} on {self.project.title}"


class Rating(models.Model):
    """
        project ratings 
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings')
    value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # composite primay key to add one rating to one project
        unique_together = ('user', 'project')
    
    def __str__(self):
        return f"{self.user.fname} {self.user.lname} rated {self.project.title}: {self.value}/5"


class Report(models.Model):
    """
    Reports for inappropriate projects or comments
    """
    # a list to hold two tubles of the type of the report ;)
    REPORT_TYPES = [
        ('project', 'Project'),
        ('comment', 'Comment'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=10, choices=REPORT_TYPES)

    # either project or comment will be filled (not both) we will use validation to ensure this 
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='reports')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name='reports')
    
    reason = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.report_type == 'project':
            return f"Report on project: {self.project.title}"
        else:
            return f"Report on comment by: {self.comment.user.fname} {self.user.lname}"
    # to validate one of the fields is filled only 
    def validate(self):
        if self.report_type == 'project':
            if not self.project:
                raise ValidationError("Project must be specified for project reports")
            if self.comment:
                raise ValidationError("Cannot report both project and comment")
        elif self.report_type == 'comment':
            if not self.comment:
                raise ValidationError("Comment must be specified for comment reports")
            if self.project:
                raise ValidationError("Cannot report both project and comment")

    def save(self, *args, **kwargs):
        # call the validation each time we save
        self.validate()
        super().save(*args, **kwargs)