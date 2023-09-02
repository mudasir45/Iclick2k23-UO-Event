from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
import os
import uuid

class Categories(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name


def get_upload_path(instance, filename):
    name = slugify(instance.title)
    return os.path.join(str(name), filename)

class Project(models.Model):
    uid = models.UUIDField(editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    supervisor = models.ForeignKey('Supervisor', related_name='project_supervisor', on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, related_name='project_category', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    sub_title = models.CharField(max_length=200, null=True, blank=True)
    body = RichTextUploadingField(max_length=5000, null=True, blank=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=get_upload_path)
    is_approved = models.BooleanField(default=False)
    is_winner = models.BooleanField(default=False)
    winner_title = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.title}'
    
    def save(self, *args, **kwargs):

        if self.slug==None:
            slug = slugify(self.title)

            has_slug = Project.objects.filter(slug = slug).exists()
            while has_slug:
                count = 1
                slug = slugify(self.title) + "-" + str(count)
                has_slug = Project.objects.filter(slug = slug).exists()
            
            self.slug = slug
        
        super().save(*args, **kwargs)
    

def get_group_upload_path(instance, filename):
    return os.path.join(str(instance.group_name), filename)

class Group(models.Model):
    uid = models.UUIDField(editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=50, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    smester = models.IntegerField(null=True, blank=True)
    section = models.CharField(max_length=50, null=True, blank=True)
    student1 = models.CharField(max_length=50, null=True, blank=True)
    roll_no1 = models.CharField(max_length=50, null=True, blank=True)
    img1 = models.ImageField(upload_to=get_group_upload_path)
    student2 = models.CharField(max_length=50, null=True, blank=True)
    roll_no2 = models.CharField(max_length=50, null=True, blank=True)
    img2 = models.ImageField(upload_to=get_group_upload_path)
    student3 = models.CharField(max_length=50, null=True, blank=True)
    roll_no3 = models.CharField(max_length=50, null=True, blank=True)
    img3 = models.ImageField(upload_to=get_group_upload_path)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.group_name
    
    
class Ratting(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reviewer = models.ForeignKey('Reviewer', on_delete=models.CASCADE)
    score1 = models.FloatField(null=True, blank=True)
    score2 = models.FloatField(null=True, blank=True)
    score3 = models.FloatField(null=True, blank=True)
    score4 = models.FloatField(null=True, blank=True)
    score5 = models.FloatField(null=True, blank=True)
    reviewText = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.project.title
    

class Supervisor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=50)
    qualif = models.CharField(max_length=50)
    institute = models.CharField(max_length=50)
    fieldOfStudy = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.user.first_name
    
    
class Reviewer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=50)
    qualif = models.CharField(max_length=50)
    institute = models.CharField(max_length=50)
    fieldOfStudy = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.user.first_name
