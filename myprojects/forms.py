from django.contrib.auth.models import User
from myblog.models import MyBlog, Tag
from django.contrib.auth import logout, authenticate, login
from django import forms


class BlogCreateForm(forms.ModelForm):
    tags = forms.CharField(help_text='Add tags by separating by comma(,).')

    def save(self, commit=True):
        instance = super().save(commit)
        tags = self.cleaned_data['tags'].split(',')
        for item in tags:
            tag, status = Tag.objects.get_or_create(name=item.strip())
            instance.tags.add(tag)
        return instance

    def add_author(self, user):
        instance = self.instance
        instance.author = user
        instance.save()


    class Meta:
        model = MyBlog
        fields = ['title', 'body']
        widgets = {
            'body': forms.Textarea(),
            }
        exclude = ['tags']

class TagCreateForm(forms.ModelForm):

    class Meta:
        model = Tag
        # fields = ['body']
        widgets = {
            'description': forms.Textarea(),
            }


class RegisterForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': ("A user with that username already exists."),
        'password_mismatch': ("The two password fields didn't match."),
        }
    username = forms.RegexField(label=("Username"), max_length=30,
                                regex=r'^[\w.@+-]+$',
                                help_text=("Required. 30 characters or fewer. Letters, digits and "
                                            "@/./+/-/_ only."),
                                error_messages={
                                    'invalid': ("This value may contain only letters, numbers and "
                                                 "@/./+/-/_ characters.")})
    password1 = forms.CharField(label=("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=("Enter the same password as above, for verification."))

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
                login(request, user)
                if not data['remember_me']:
                    request.session.set_expiry(0)
                return True
            else:
                raise Exception("Your account has been disabled!")
        else:
            raise Exception("Your username and password were incorrect.")
        return False