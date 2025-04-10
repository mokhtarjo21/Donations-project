from django import forms
from .models import Category
from .models import Project
from interactions.models import Report


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']




class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [ 'title', 'details', 'category', 'tags', 'target', 'end_time']



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
