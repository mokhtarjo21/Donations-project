from django.views.generic import TemplateView
from django.shortcuts import render
from django.db.models import Count, Sum
from projects.models import Project, Category
from users.models import User

class HomePage(TemplateView):

    template_name = 'main/home.html'
    
    # fetching some data to display as a starring point....
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get featured/recent projects with related data
        context['projects'] = Project.objects.select_related(
            'creator', 
            'category'
        ).prefetch_related(
            'tags',
            'projectpictures_set'
        ).annotate(
            image_count=Count('projectpictures'),
            total_donations=Sum('current_amount'),

        ).order_by('-start_time')[:10]

        # Get categories with project counts
        context['categories'] = Category.objects.annotate(
            project_count=Count('project')
        ).order_by('-project_count')[:8]
        
        return context
