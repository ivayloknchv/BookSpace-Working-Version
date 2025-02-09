from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm


DISPLAYED_GENRE_CHOICES = [
    ('Action', 'Action'), ('Adventure', 'Adventure'), ('Autobiography', 'Autobiography'),
    ('Biography', 'Biography'), ('Business', 'Business'), ('Childrens', 'Childrens'),
    ('Classics', 'Classics'), ('Cookbooks', 'Cookbooks'), ('Drama', 'Drama'),
    ('Dystopia', 'Dystopia'), ('Fantasy', 'Fantasy'), ('Health', 'Health'),
    ('Historical Fiction', 'Historical Fiction'), ('History', 'History'), ('Horror', 'Horror'),
    ('Humor', 'Humor'), ('Memoir', 'Memoir'), ('Mystery', 'Mystery'), ('Philosophy', 'Philosophy'),
    ('Poetry', 'Poetry'), ('Popular Science', 'Popular Science'), ('Psychology', 'Psychology'),
    ('Religion', 'Religion'), ('Romance', 'Romance'), ('Science Fiction', 'Science Fiction'),
    ('Thriller', 'Thriller'), ('Young Adult', 'Young Adult'),
]


class MyLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['password'].required = False


class MySignupForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None


class MyUpdatePictureForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('profile_picture', )


class MySignupGenresForm(forms.Form):

    preferred_genres = forms.MultipleChoiceField(
        choices=DISPLAYED_GENRE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


class MyEditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
        help_texts = {'username' : None }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None


class MyPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None


class MyChangeGenresForm(forms.ModelForm):

    preferred_genres = forms.MultipleChoiceField(
        choices=DISPLAYED_GENRE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = User
        fields = ('preferred_genres', )