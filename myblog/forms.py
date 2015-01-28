from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from myblog.models import MyBlog, Tag
from django.contrib.auth import logout, authenticate, login
from django import forms

class BlogCreateForm(forms.ModelForm):
    tags = forms.CharField(help_text='Add tags by separating by comma(,).')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            if instance:
                self.fields['tags'].initial = ', '.join([x.name for x in instance.tags.all()])

    def clean_title(self):
        data = self.cleaned_data['title']
        if MyBlog.objects.filter(title=data).exists():
            raise ValidationError('This title already exists')
        return data

    def save(self, commit=True):
        with transaction.atomic():
            instance = super().save(commit=True)
            tags = self.cleaned_data['tags'].split(',')
            for item in tags:
                tag, status = Tag.objects.get_or_create(name=item.strip())
                self.instance.tags.add(tag)
        return instance

    def save_author(self,user=None):
        if user and self.instance:
            self.instance.author = user
            return True
        return False


    class Meta:
        model = MyBlog
        fields = ['title', 'body']
        widgets = {
            'body': forms.Textarea(),
            }

class TagCreateForm(forms.ModelForm):

    def clean_name(self):
        data = self.cleaned_data['name']
        if Tag.objects.filter(name=data).exists():
            raise ValidationError('This tag already exists.')
        return data

    class Meta:
        model = Tag
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(),
            }


class RegisterForm(UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = False
        if commit:
            user.save()
        return user
    class Meta:
        model = User
        fields = ("username", 'first_name', 'last_name', 'email', )


class LogoutForm(forms.Form):

    def logout(self, request):
        logout(request)
        return True


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label="Username")
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput, label="Remember Me?")

    def authenticate(self, request):
        data = self.cleaned_data
        user = authenticate(username=data["username"], password=data["password"])
        if user is not None:
            if user.is_active:
                if user.is_staff:
                    login(request, user)
                    if not data['remember_me']:
                        request.session.set_expiry(0)
                    return True
                else:
                    raise Exception("Your account is disabled!")
            else:
                raise Exception("Your account is disabled!")

        else:
            raise Exception("Your username and password were incorrect.")
        return False