from django.forms import ModelForm
from django.forms.models import ModelMultipleChoiceField
from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


class AddEnterpreneur(ModelForm):
    class Meta:
        model = Entrepreneurs
        exclude = (
            "user",
            "status",
        )


class AddPartner(ModelForm):
    class Meta:
        model = Bussiness_Partner
        exclude = (
            "user",
            "status",
        )


class AddProduct(ModelForm):
    class Meta:
        model = Product
        exclude = ("company",)


class Addimages(ModelForm):
    class Meta:
        model = Product_Image
        exclude = ("product",)


class Addfaqs(ModelForm):
    class Meta:
        model = FAQ
        exclude = ("product",)
