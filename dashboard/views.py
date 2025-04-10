# main/dashboard/category_views.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .forms import *
# 
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm  
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test


# You'll create this form
from .models import Category
from .models import Tag 

def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/category_list.html', {'categories': categories})


@login_required
@user_passes_test(lambda u: u.is_staff)
def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'dashboard/category_form.html', {'form': form})
#
@login_required
@user_passes_test(lambda u: u.is_staff)
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'dashboard/category_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'dashboard/category_confirm_delete.html', {'category': category})





#manage Projects


@login_required
def project_list(request):
    projects = Project.objects.select_related('category', 'creator') \
        .prefetch_related('tags') \
        .filter(creator=request.user)  

    return render(request, 'dashboard/project_list.html', {'projects': projects})





@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        images = request.FILES.getlist('images')  

        if form.is_valid():
          
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            form.save_m2m()

            for image in images:
                ProjectPictures.objects.create(project=project, image=image)

            return redirect('project_list')

    else:
        form = ProjectForm()

    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, 'dashboard/project_form.html', {
        'form': form,
        'categories': categories,
        'tags': tags,
    })





@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.creator != request.user:
        return HttpResponseForbidden("❌ You are not allowed to edit this project.")

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'dashboard/project_form.html', {
        'form': form,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    })





def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk) 
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'dashboard/project_confirm_delete.html', {'project': project})

    