from django.db import models
from django.contrib.auth.models import User 

class Categories(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    sub_title = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField(max_length=1000, null=True, blank=True)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.title}'
    

class Group(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    smester = models.IntegerField(null=True, blank=True)
    section = models.CharField(max_length=50, null=True, blank=True)
    student1 = models.CharField(max_length=50, null=True, blank=True)
    roll_no1 = models.CharField(max_length=50, null=True, blank=True)
    # img1 = models.ImageField(upload_to='projects', default='')
    student2 = models.CharField(max_length=50, null=True, blank=True)
    roll_no2 = models.CharField(max_length=50, null=True, blank=True)
    # img2 = models.ImageField(upload_to='projects', default='')
    student3 = models.CharField(max_length=50, null=True, blank=True)
    roll_no3 = models.CharField(max_length=50, null=True, blank=True)
    # img3 = models.ImageField(upload_to='projects', default='')
    
    def __str__(self) -> str:
        return self.name
    
    
class Rating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reviewer = models.ForeignKey('Reviewer', on_delete=models.CASCADE)
    score1 = models.FloatField(null=True, blank=True)
    score2 = models.FloatField(null=True, blank=True)
    score3 = models.FloatField(null=True, blank=True)
    score4 = models.FloatField(null=True, blank=True)
    score5 = models.FloatField(null=True, blank=True)
    reviewText = models.CharField(max_length=500, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.project.title
    

class Supervisor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.CharField(max_length=50, null=True, blank=True)
    qualif = models.CharField(max_length=50, null=True, blank=True)
    institute = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.user.first_name
    
class Reviewer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.CharField(max_length=50, null=True, blank=True)
    qualif = models.CharField(max_length=50, null=True, blank=True)
    institute = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.user.first_name
