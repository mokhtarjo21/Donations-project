from django import forms
from .models import Category
from .models import Project, ProjectPictures
from django.forms import modelformset_factory
from interactions.models import Report


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'tags', 'target', 'end_time']



# reprt form to handle the reports 
# class ReportForm(forms.ModelForm):
#     class Meta:
#         model = Report
#         fields = ['is_resolved', 'reason']  # Only allow editing these fields
#         widgets = {
#             'reason': forms.Textarea(attrs={'rows': 4}),
#         }
#         labels = {
#             'is_resolved': 'Mark as Resolved',
#         }
        widgets = {
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
class ProjectPictureForm(forms.ModelForm):
    class Meta:
        model = ProjectPictures
        fields = ['image']

ProjectPictureFormSet = modelformset_factory(ProjectPictures, form=ProjectPictureForm, extra=4, can_delete=True)