from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .send_mails import send_info_mails
from .forms import *
from .models import Notification

POSTS_PER_PAGE = 6

@login_required(login_url='userLogin')
def projectList(request):
    Projects = Project.objects.filter(is_approved = True)
    CategoriesList = Categories.objects.annotate(project_count = Count('project_category'))

    page = request.GET.get('page', 1)
    PostPaginator = Paginator(Projects, POSTS_PER_PAGE)
    
    try:
        Projects = PostPaginator.page(page)
    except PageNotAnInteger:
        Projects = PostPaginator.page(1)
    except EmptyPage:
        Projects = PostPaginator.page(PostPaginator.num_pages)
    

    context = {
        'Projects':Projects,
        'CategoriesList':CategoriesList,
        'paginator' : PostPaginator,
        'IsPaginated' : True,
    }
    return render(request, 'project_exhib/projectList.html', context)

@login_required(login_url='userLogin')
def projectDetails(request, uid):
    project_obj = Project.objects.get(uid = uid)
    group_obj = project_obj.group

    context = {
        'project':project_obj,
        'group_obj':group_obj,
    }
    return render(request, 'project_exhib/projectDetails.html', context)

@login_required(login_url='userLogin')
def addGroup(request):
    form = GroupForm()
    if request.method == "POST":
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.save()
        messages.success(request, "You have successfully resgiter your group! Now Fill out this form to get register your project")
        return redirect('addProject')
    
    has_group = Group.objects.filter(user = request.user).exists()
    if has_group:
        messages.error(request, f"You have already registered a group! |{Group.objects.get(user = request.user)}| you just need to register your project")
        return redirect('info')
    
    context = {
        'form':form
    }
    return render(request, 'project_exhib/addGroup.html', context)

@login_required(login_url='userLogin')
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

@login_required(login_url='userLogin')
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

@login_required(login_url='userLogin')
def addProject(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
        messages.success(request, "You have successfully submit your project! you will get notified when your supervisor approve this project")
        return redirect('info')
    
    has_group = Group.objects.filter(user = request.user).exists()
    has_project = Project.objects.filter(user = request.user).exists()
    if not has_group:
        messages.info(request, "You have not register your group! First register your group here")
        return redirect('addGroup')
    
    if has_project:
        messages.error(request, "You have already Submit a project! You cannot add one more project")
        return redirect('info')
    
    form = ProjectForm(user=request.user)
    context = {
        'form':form
    }
    return render(request, 'project_exhib/addProject.html', context)

@login_required(login_url='userLogin')
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

@login_required(login_url='userLogin')
def deleteProject(request, uid):
    project_obj = Project.objects.get(uid = uid)
    if request.method == "POST":
        project_obj.delete()
        return redirect('home')
    context = {
        'item':project_obj
    }
    return render(request, 'project_exhib/delete_alert.html', context)


@login_required(login_url='userLogin')
def studentPortal(request, username):
    user = User.objects.get(username = username)
    alerts = Notification.objects.filter(user = user)
    has_project = Project.objects.filter(user = user).exists()
    if not has_project:
        messages.info(request, "It seems that you have not submit any project yet!")
        return redirect('info')
    try:
        project = Project.objects.get(user = user)
    except Exception as e:
        print(e)
    context = {
        'project':project,
        'alerts':alerts,
    }
    return render(request, 'project_exhib/studentPortal.html', context)




@login_required(login_url='userLogin')
def projectAproval(request):
    supervisor = Supervisor.objects.get(user = request.user)
    projects = Project.objects.filter(supervisor = supervisor)

    if request.method == "POST":
        uid = request.POST['uid']
        action = request.POST.get('action')
        project = Project.objects.get(uid = uid)
        if action == 'approve':
            project.is_approved = True
            project.save()
            message = "Your Project has been approved successfully by your supervisor now you can check this in active project list"
            subject = "Project Approved"
        else:
            subject = "Project Disapproved"
            message = "Your Project was contact with your supervisor as soon as possible"
        
        template = render_to_string('main/emailTemplate.html', {
            'supervisor':supervisor,
            'project': project,
            'username' : project.user.username,
            'message': message
        })
        send_to = project.user.email
        send_info_mails(subject, template, [send_to])
        alert = Notification.objects.create(user = project.user, message = message)


        messages.success(request, "Action complete successfully")
        return redirect('projectAproval')

        

       

    context = {
        'projects':projects,
    }
    return render(request, 'project_exhib/projectAproval.html', context)