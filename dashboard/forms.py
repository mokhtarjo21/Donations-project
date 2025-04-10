from django import forms
from .models import Category
from .models import Project, ProjectPictures
from django.forms import modelformset_factory


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'tags', 'target', 'end_time']
        widgets = {
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
class ProjectPictureForm(forms.ModelForm):
    class Meta:
        model = ProjectPictures
        fields = ['image']

ProjectPictureFormSet = modelformset_factory(ProjectPictures, form=ProjectPictureForm, extra=4, can_delete=True)