from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm,CustomerForm, BICSetupForm, MCRegisterForm, PesoNetForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Branch, Profile, Record, BICSetup, MCRegister, PesoNet, Customer
from django.http import HttpResponse


from django.contrib import messages


def create_user_view(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            # Save the new user
            user = form.save()

            # Get the user type from the form
            user_type = form.cleaned_data['user_type']

            # Get the selected branch type
            branch_type = form.cleaned_data['branch_type']
            
            # Retrieve the corresponding Branch instance based on the selected branch type
            try:
                branch = Branch.objects.get(branch_name=branch_type)  # Assuming branch_name represents branch_type
            except Branch.DoesNotExist:
                # Handle the case where the branch doesn't exist (error response, log, etc.)
                return render(request, 'create_user.html', {'form': form, 'error': 'Branch not found'})
            
            # Create the user's profile with the correct branch and user type
            profile = Profile(user=user, user_type=user_type, branch=branch)
            profile.save()

            # Optionally, log in the new user and redirect to a success page
            login(request, user)
            return redirect('dashboard')  # Adjust as needed

    else:
        form = CreateUserForm()
    
    return render(request, 'webapp/admin/branch/dashboard.html', {'form': form})



#Homepage 
def home(request):

    return render(request, 'webapp/index.html')

# Register
def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            if user_type == 'admin':
                user.is_staff = True
            else:
                user.is_staff = False
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect("dashboard")
    else:
        form = CreateUserForm()
    context = {'form':form}
    return render(request, 'webapp/register.html', context=context)

# Login
def my_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect("dashboard")
                else:
                    return redirect("mc_register")
    else:
        form = LoginForm()
    context = {'form':form}
    return render(request, 'webapp/my-login.html', context=context)


# Admin Dashboard
@login_required(login_url='my-login')
def admin_dashboard(request):
    my_records = Record.objects.all()
    context = {'records': my_records}
    return render(request, 'webapp/admin/branch/dashboard.html', context=context)


# Cashier Dashboard
@login_required(login_url='my-login')
def cashier_dashboard(request):
    my_records = MCRegister.objects.all()

    #always add here {% for mc_register in mc_registers %}
    context = {'mc_registers': my_records}
    return render(request, 'webapp/cashier/mcregister/cashier.html', context=context)



# BRANCH SETUP
# Create a record 
@login_required(login_url='my-login')

def create_record(request):
    form = CreateRecordForm()
    if request.method == "POST":
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was created!")
            return redirect("dashboard")
    context = {'form': form}
    return render(request, 'webapp/admin/branch/create-record.html', context=context)


#Update 
@login_required(login_url='my-login')
def update_record(request, pk):

    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect("dashboard")
    context = {'form':form}
    return render(request, 'webapp/admin/branch/update-record.html', context=context)

# - Read / View a singular record
@login_required(login_url='my-login')
def singular_record(request, pk):

    all_records = Record.objects.get(id=pk)
    context = {'record':all_records}
    return render(request, 'webapp/admin/branch/view-record.html', context=context)

#Delete
@login_required(login_url='my-login')
def delete_record(request, pk):

    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, "Your record was deleted!")
    return redirect("dashboard")






# CUSTOMER
@login_required(login_url='my-login')
def customer(request):
    customers = Customer.objects.all()
    return render(request, 'webapp/admin/customer/customer.html', {'customers': customers})


@login_required(login_url='my-login')
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect('customer')
    else:
        form = CustomerForm()
        
    return render(request, 'webapp/admin/customer/customer_create.html', {'form': form})


@login_required(login_url='my-login')
def customer_update(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect('customer')
    else:
        form = CustomerForm(instance=customer)
        
    return render(request, 'webapp/admin/customer/customer_update.html', {'form': form})

    
@login_required(login_url='my-login')
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, customer_id=pk)  
    customer.delete()
    messages.success(request, "Your record was deleted!")
    return redirect("customer")





# BIC SETUP
@login_required(login_url='my-login')
def bic_setup(request):
    bic_setups = BICSetup.objects.all()
    for bic_setup in bic_setups:
        print(f"BICSetup product_code: {bic_setup.product_code}")  # Debugging line
    return render(request, 'webapp/admin/bic/bic_setup.html', {'bic_setups': bic_setups})


@login_required(login_url='my-login')
def bic_setup_create(request):
    if request.method == 'POST':
        form = BICSetupForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, "Your record was updated!")
            return redirect('bic_setup')
    else:
        form = BICSetupForm()
        
    return render(request, 'webapp/admin/bic/bic_setup_create.html', {'form': form})


@login_required(login_url='my-login')
def bic_setup_update(request, product_code):
    bicsetup = get_object_or_404(BICSetup, product_code=product_code)
    if request.method == 'POST':
        form = BICSetupForm(request.POST, instance=bicsetup)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect('bic_setup')
    else:
        form = BICSetupForm(instance=bicsetup)

    return render(request, 'webapp/admin/bic/bic_setup_update.html', {'form': form})


@login_required(login_url='my-login')
def bic_setup_delete(request, product_code):
    bicsetup = get_object_or_404(BICSetup, product_code=product_code)
    if request.method == 'POST':
        bicsetup.delete()
        messages.success(request, "Record deleted successfully!")
        return redirect('bic_setup')










#CASHIER
@login_required(login_url='my-login')
def mc_register(request):
    mc_registers = MCRegister.objects.all()
    return render(request, 'webapp/cashier/mcregister/cashier.html', {'mc_registers': mc_registers})


@login_required(login_url='my-login')
def mc_register_create(request):
    if request.method == 'POST':
        form = MCRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect('mc_register')
    else:
        form = MCRegisterForm()
        
    return render(request, 'webapp/cashier/mcregister/mc_create.html', {'form': form})


@login_required(login_url='my-login')
def mc_register_update(request, mc_register_id):
    mc_register = MCRegister.objects.get(pk=mc_register_id)
    if request.method == 'POST':
        form = MCRegisterForm(request.POST, instance=mc_register)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect('mc_register')
    else:
        form = MCRegisterForm(instance=mc_register)
        
    return render(request, 'webapp/cashier/mcregister/mc_update.html', {'form': form})








#PESOT
@login_required(login_url='my-login')
def peso_net(request):
    peso_nets = PesoNet.objects.all()
    return render(request, 'webapp/cashier/pesonet/peso_net.html', {'peso_nets': peso_nets})


@login_required(login_url='my-login')
def peso_create(request):
    if request.method == 'POST':
        form = PesoNetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect('peso_net')
    else:
        form = PesoNetForm()
        
    return render(request, 'webapp/cashier/pesonet/peso_create.html', {'form': form})


@login_required(login_url='my-login')
def peso_update(request, peso_net_id):
    peso_net = PesoNet.objects.get(pk=peso_net_id)
    if request.method == 'POST':
        form = PesoNetForm(request.POST, instance=peso_net)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect('peso_net')
    else:
        form = PesoNetForm(instance=peso_net)
        
    return render(request, 'webapp/cashier/pesonet/peso_update.html', {'form': form})






#BIC cashier
@login_required(login_url='my-login')
def bic_cashier(request):
    bic_setups = BICSetup.objects.all()
    return render(request, 'webapp/cashier/bic/bic_cashier.html', {'bic_setups': bic_setups})





#logout
def user_logout(request):
    auth.logout(request)
    messages.success(request, "Logout success!")
    return redirect("my-login")




