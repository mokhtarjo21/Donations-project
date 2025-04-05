from django import forms
from .models import Category
from .models import Project


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']




class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [ 'title', 'details', 'category', 'tags', 'target', 'end_time']
