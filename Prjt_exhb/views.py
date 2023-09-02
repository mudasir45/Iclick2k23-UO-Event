from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required


from .forms import *


def projectList(request):
    Projects = Project.objects.all()
    CategoriesList = Categories.objects.annotate(project_count = Count('project_category'))

    context = {
        'Projects':Projects,
        'CategoriesList':CategoriesList,
    }
    return render(request, 'project_exhib/projectList.html', context)

def projectDetails(request, uid):
    project_obj = Project.objects.get(uid = uid)
    group_obj = project_obj.group

    context = {
        'project':project_obj,
        'group_obj':group_obj,
    }
    return render(request, 'project_exhib/projectDetails.html', context)

# GROUP CRUD APIS START FROM HERE 
def addGroup(request):
    form = GroupForm()
    if request.method == "POST":
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.save()
        return redirect('home')
    context = {
        'form':form
    }
    return render(request, 'project_exhib/addGroup.html', context)

def updateGroup(request, uid):
    group_obj = Group.objects.get(uid = uid)
    form = GroupForm(instance=group_obj)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=group_obj)
        if form.is_valid():
            form.save()
        return redirect('home')
    
    context = {
        'form':form
    }
    return render(request, 'project_exhib/addGroup.html', context)

def deleteGroup(request, uid):
    group_obj = Group.objects.get(uid = uid)
    if request.method == "POST":
        group_obj.delete()
        return redirect('home')
    context = {
        'item':group_obj
    }
    return render(request, 'project_exhib/delete_alert.html', context)


# PROJECT CRUD APIS START FROM HERE 
@login_required(login_url='home')
def addProject(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
        return redirect('home')
    context = {
        'form':form
    }
    return render(request, 'project_exhib/addProject.html', context)

def updateProject(request, uid):
    project_obj = Project.objects.get(uid = uid)
    form = ProjectForm(instance=project_obj)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project_obj)
        if form.is_valid():
            form.save()
        return redirect('home')
    context = {
        'form':form
    }
    return render(request, 'project_exhib/addProject.html', context)

def deleteProject(request, uid):
    project_obj = Project.objects.get(uid = uid)
    if request.method == "POST":
        project_obj.delete()
        return redirect('home')
    context = {
        'item':project_obj
    }
    return render(request, 'project_exhib/delete_alert.html', context)