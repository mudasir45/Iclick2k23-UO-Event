from django.forms import ModelForm
from .models import *

class GroupForm(ModelForm):
    
    class Meta:
        model = Group
        exclude = ['user']


class ProjectForm(ModelForm):
    
    class Meta:
        model = Project
        exclude = ['slug', 'user']
    