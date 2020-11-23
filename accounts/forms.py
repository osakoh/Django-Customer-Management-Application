from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Order, Customer


# ModelForm: is a class that converts a model into a Django form.

class OrderModelForm(ModelForm):
    # specifies the name of the model to use
    class Meta:  # Meta: describes anything that's not a field
        model = Order
        fields = ['customer', 'product', 'status', 'note']
        # fields = '__all__'  # create a form with all the fields


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']