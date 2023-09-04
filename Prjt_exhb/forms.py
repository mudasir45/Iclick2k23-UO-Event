from django.forms import ModelForm
from .models import *

class GroupForm(ModelForm):
    
    class Meta:
        model = Group
        exclude = ['user']

class RattingForm(ModelForm):
    
    class Meta:
        model = Ratting
        exclude = ['project', 'reviewer']


class ProjectForm(ModelForm):
    
    class Meta:
        model = Project
        exclude = ['slug', 'user', 'is_approved', 'is_winner', 'winner_title']


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from keyword arguments
        super(ProjectForm, self).__init__(*args, **kwargs)

        # Limit the choices for the 'group' field to groups associated with the user
        if user is not None:
            self.fields['group'].queryset = Group.objects.filter(user=user)