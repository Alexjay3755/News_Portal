# from django import forms
# from django.core.exceptions import ValidationError
# from simpleapp.models import Posts

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


# class PostForm(forms.ModelForm):
#     text = forms.CharField(min_length=20)
#
#     class Meta:
#         model = Posts
#         fields = ['title', 'text', 'category', 'author']
#
#     def clean(self):
#         cleaned_data = super().clean()
#         title = cleaned_data.get("text")
#         text = cleaned_data.get("user")
#
#         if title == text:
#             raise ValidationError(
#                 "Описание не должно быть идентично названию."
#             )
#
#         return cleaned_data
#






class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user