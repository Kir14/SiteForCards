from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import User, SecurityUser, TypesCard, Client, Card


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UserProfileForm(ModelForm):
    class Meta:
        model = Client
        # fields= '__all__'
        fields = ['phone', 'avatar']
        exclude = ['user']
        # fields = ['phone','avatar']
        widgets = {
            'avatar': forms.FileInput(),
        }


class TypeCard(ModelForm):
    class Meta:
        model = TypesCard
        fields = '__all__'


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = '__all__'
