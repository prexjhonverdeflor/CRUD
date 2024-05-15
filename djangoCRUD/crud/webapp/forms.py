from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Record, BICSetup, MCRegister, PesoNet, Customer

from django import forms

from django.forms.widgets import PasswordInput, TextInput, DateInput, Textarea
from django.contrib.auth.forms import AuthenticationForm



class CreateUserForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('cashier', 'Cashier'),
    ]
    BRANCH_TYPE_CHOICES = [
        ('head', 'Head Office'),
        ('camalig', 'Camalig Office'),
        ('daraga', 'Daraga Office'),
        ('manito', 'Manito Office'),
        ('legazpi', 'Legazpi Office'),
    ]
    
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect)
    branch_type = forms.ChoiceField(choices=BRANCH_TYPE_CHOICES, widget=forms.Select)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'user_type', 'branch_type']
        help_texts = {
            'username': '',
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


#create record
class CreateRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['category_id','category_desc']


#update record
class UpdateRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['category_id','category_desc']



#CUSTOMER

class CustomerForm(forms.ModelForm):
    
    LEVEL_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]

    customer_level = forms.ChoiceField(choices=LEVEL_CHOICES, label='Level', required=True)

    class Meta:
        model = Customer
        fields = [
            'customer_id',
            'customer_fullname',
            'customer_firstname',
            'customer_middlename',
            'customer_lastname',
            'customer_address',
            'customer_level',
        ]
        labels = {
            'customer_id': 'ID',
            'customer_fullname': 'Fullname',
            'customer_firstname': 'Firstname',
            'customer_middlename': 'Middlename',
            'customer_lastname': 'Lastname',
            'customer_address': 'Address',
            'customer_level': 'Level',
        }




class BICSetupForm(forms.ModelForm):
    class Meta:
        model = BICSetup
        fields = [
            'product_code',
            'category',
            'item_code',
            'product_desc',
            'product_barcode',
            'level_1',
            'level_2',
            'level_3',
            'level_4',
            'level_5',
            'unit',
            'product_price'
        ]
        labels = {
            'product_code': 'ID',
            'category': 'Item Type',
            'item_code': 'Item Code',
            'product_desc': 'Description',
            'product_barcode': 'Barcode',
            'level_1': 'Level 1',
            'level_2': 'Level 2',
            'level_3': 'Level 3',
            'level_4': 'Level 4',
            'level_5': 'Level 5',
            'unit': 'Unit',
            'product_price': 'Price'
        }

        



#CASHIER
class MCRegisterForm(forms.ModelForm):

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, label='Status', required=True)

    class Meta:
        model = MCRegister
        fields = ['branch_name', 'date_issued', 'payee', 'amount', 'check_number', 'status', 'branch_remarks']
        
        widgets = {
            'date_issued': DateInput(attrs={'type': 'date'}),
            'branch_remarks': Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        

#PESOT
class PesoNetForm(forms.ModelForm):

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, label='Status', required=True)

    class Meta:
        model = PesoNet
        fields = ['branch_name', 'OFI_reference_num', 'transact_amount', 'transact_date', 'status']
        
        widgets = {
            'transact_date': DateInput(attrs={'type': 'date'}),
        }


    