from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth, TruncMinute, TruncHour
from django.views.generic import DeleteView, UpdateView
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.models import Project, Category
from interactions.models import Donation, Comment, Rating, Report 
from users.models import User
from django.views.generic import TemplateView, DetailView
from django.shortcuts import get_object_or_404
from .forms import UserUpdateForm
from decimal import Decimal
from django.db.models import Count, Sum
from django.contrib import messages
@login_required
def donate_view(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = Decimal(amount)
            if amount > 0:
                project.current_amount += amount
                project.save()
                messages.success(request, f"Thanks for donating ${amount:.2f}!")
                return redirect('project_detail', pk=project.pk)
            else:
                messages.error(request, "Amount must be greater than 0.")
        except ValueError:
            messages.error(request, "Invalid amount entered.")

    return render(request, 'components/donation_form.html', {'project': project})


class ProjectDetailView(LoginRequiredMixin,DetailView):
    model = Project
    template_name = 'components/project_detail.html'  
    context_object_name = 'project'

class HomePage(TemplateView):
    template_name = 'main/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        category_slug = request.GET.get('category')

        project_query = Project.objects.select_related(
            'creator', 'category'
        ).prefetch_related(
            'tags', 'projectpictures_set'
        ).annotate(
            image_count=Count('projectpictures'),
            total_donations=Sum('current_amount'),
        )

        if category_slug:
            project_query = project_query.filter(category__slug=category_slug)

        context['projects'] = project_query.order_by('-start_time')[:10]

        context['categories'] = Category.objects.annotate(
            project_count=Count('project')
        ).order_by('-project_count')[:8]

        context['selected_category'] = category_slug

        return context

class ProfilePage(LoginRequiredMixin,View):
    def get(self, request):
        # Only show the logged-in user's data
        user = request.user
        context = {}
        # user info
        context['user'] = {
            'id': user.id,
            'first_name': user.fname,
            'last_name': user.lname,
            'email': user.email,
            'facebook': user.facebook_acount,
            'birthdate': user.Birthdate,
            'phone': user.phone,
            'is_active': user.active_email,
            'picture_url': user.picture.url if user.picture else 'default.jpg',
            'date_joined': user.date_joined,
            'username': user.username,
        }
        
        # Basic user statistics
        user_donations = Donation.objects.filter(user=user)
        
        context['user_stats'] = {
            'total_donated': user_donations.aggregate(
                total=Sum('amount')
            )['total'] or 0,
            'projects_supported': user_donations.values(
                'project'
            ).distinct().count(),
        }
        ##########################the chart ###########################
        # Get donations for the last 24 hours
        last_24_hours = datetime.now() - timedelta(hours=24)
        
        # Get hourly donations with proper timezone handling
        all_donations = user_donations.filter(
            created_at__gte=last_24_hours
        ).annotate(
            ## we have to remove the tzinfo to match the datetime.now()
            hour=TruncHour('created_at', tzinfo=None)  
        ).values('hour').annotate(
            total=Sum('amount')
        ).order_by('hour')

        print("Donations >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", all_donations)

        # here I created a timeline and truncated anything lower than hour
        all_hours = []
        current = last_24_hours.replace(minute=0, second=0, microsecond=0)  # Normalize to hour start
        end_time = datetime.now().replace(minute=0, second=0, microsecond=0)
        
        while current <= end_time:
            all_hours.append(current)
            current += timedelta(hours=1)

        # create a dictionary of donations by hour 
        donation_dict = {}
        for donation in all_donations:
            hour_key = donation['hour'].replace(tzinfo=None)  # we have to remove the timezone information
            donation_dict[hour_key] = float(donation['total'])

        # Fill in missing hours with zero and create chart data
        context['chart_data'] = {
            'labels': [d.strftime('%H:00') for d in all_hours],
            'values': [donation_dict.get(d, 0) for d in all_hours]
        }

        ##############################################################


        # Recent donations with project details
        # Get first image for each project
        recent_donations = user_donations.select_related('project').order_by('-created_at')[:4]
        
        # We need to process the donations to include project images
        donations_with_details = []
        for donation in recent_donations:
            # Get the first image for this project (if any)
            project_image = donation.project.projectpictures_set.first()
            donation_dict = {
                'amount': donation.amount,
                'project_title': donation.project.title,
                'donation_date': donation.created_at,
                'project_image': project_image.image if project_image else None
            }
            donations_with_details.append(donation_dict)
        
        context['recent_donations'] = donations_with_details

        # Calculate category-based impact
        category_donations = user_donations.select_related('project__category').values(
            'project__category__name'
        ).annotate(
            total=Sum('amount')
        )
        
        # Define impact metrics based on categories
        # This is where you'd implement your specific impact calculations
        impacts = []
        for cat_donation in category_donations:
            category = cat_donation['project__category__name']
            amount = cat_donation['total']
            impacts.append({
                'category': category,
                'amount': amount,
            })
            
        
        # Impact summary
        annual_target = 100000  # This should be configurable
        context['impact_summary'] = {
            'annual_target': annual_target,
            'current_progress': context['user_stats']['total_donated'],
            'progress_percentage': min(100, (context['user_stats']['total_donated'] / annual_target) * 100),
            'impacts': impacts
        }


        
    

        for key, value in context.items():
            print(f"{key} ====> : {value}")
        return render(request, 'main/profile.html', context)
    

class EditProfile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "main/edit_profile.html"
    form_class = UserUpdateForm  
    success_url = reverse_lazy("profile") 

    # to edit the current user rather than passing the user pk in the url 
    def get_object(self, queryset=None):
        return self.request.user
    

class DonationHistory(LoginRequiredMixin,View):
    template_name = 'main/donation_history.html'
    
    def get(self, request):
        user = request.user
        donations = Donation.objects.filter(
            user=user
        ).select_related(
            'project'
        ).prefetch_related(
            'project__projectpictures_set'
        ).order_by('-created_at')

        # Calculate total stats
        total_stats = {
            'total_donated': donations.aggregate(Sum('amount'))['amount__sum'] or 0,
            'total_projects': donations.values('project').distinct().count(),
            'total_donations': donations.count()
        }
        
        context = {
            'donations': donations,
            'stats': total_stats,
            'user': user,
        }
        return render(request, self.template_name, context)


# view to display all projects created by the user

class UserProjects(LoginRequiredMixin,View):
    def get(self, request):
        user = request.user
        
        # Get all projects created by user with related data
        projects = Project.objects.filter(
            creator=user
        ).select_related(
            'category'
        ).prefetch_related(
            'projectpictures_set',
            'donations'
        ).annotate(
            donation_count=Count('donations'),
            total_raised=Sum('donations__amount'),
            average_rating=Avg('ratings__value')
        ).order_by('-start_time')

        context = {
            'projects': projects,
            'total_projects': projects.count(),
            'total_raised': projects.aggregate(
                total=Sum('current_amount')
            )['total'] or 0,
        }
        
        return render(request, 'main/user_projects.html', context)
