from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory
from django.contrib import messages, auth
from django.contrib.auth.models import User  # user model
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import OrderModelForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only


# classes for the url pattern
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()  # returns the total number of customers
    total_orders = orders.count()  # returns the total number of orders
    delivered = orders.filter(status='Delivered').count()  # returns total number of orders that have been 'Delivered'
    pending = orders.filter(status='Pending').count()  # returns the total number of orders that are 'Pending'

    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = get_object_or_404(Customer, id=pk)  # get a single customer

    customer_orders = customer.order_set.all()  # retrieves all orders made by a single customer
    count_customer_orders = customer_orders.count()  # total orders for a single customer

    order_filter = OrderFilter(request.GET, queryset=customer_orders)  # creates an object of django-filters
    customer_orders = order_filter.qs

    context = {'single_customer': customer,
               'customer_orders': customer_orders,
               'count_customer_orders': count_customer_orders,
               'order_filter': order_filter
               }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    order_form_set = inlineformset_factory(Customer, Order, fields=('product', 'status', 'note'))
    # pk is passed because orders are created from the customers page
    customer = Customer.objects.get(id=pk)
    # queryset=Order.objects.none(): hides initial data
    formset = order_form_set(queryset=Order.objects.none(), instance=customer)
    # order_form = OrderModelForm(initial={'customer': customer})  # recall that the form is sent as method="post"
    if request.method == 'POST':
        formset = order_form_set(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            messages.success(request, f'Successfully created an order!')
            # cus_id = request.POST['customer']
            # return redirect('/customer/'+cus_id)  # redirect to customers detail page
            return redirect('/')  # redirect to dashboard(home)

    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order_instance = Order.objects.get(id=pk)  # retrieve details belong to a single customer
    # order_form = OrderModelForm(instance=order_instance)  # prefill in the form with the customers orders
    order_form = OrderModelForm(instance=order_instance)  # prefill in the form with the customers orders

    if request.method == 'POST':
        order_form = OrderModelForm(request.POST, instance=order_instance)
        if order_form.is_valid():
            order_form.save()
            messages.info(request, f'Order updated to [{order_instance.product.name}]')
            cus_id = request.POST['customer']
            return redirect('/customer/' + cus_id)  # redirect to customers detail page
            # return redirect('/')  # redirect to dashboard/home

    context = {'order_form': order_form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    delete_item = Order.objects.get(id=pk)
    if request.method == "POST":
        delete_item.delete()
        messages.info(request,
                      f'Your order [{delete_item.product.name} - £{delete_item.product.price}] has been deleted')
        return redirect('/')

    context = {'item': delete_item}
    return render(request, 'accounts/delete.html', context)


@unauthenticated_user
def register_user(request):
    if request.method == 'POST':
        # form values
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']

        # password check
        if password != password2:
            messages.error(request, "Password don't match")
            return redirect('register')
        elif password == password2:
            # check username
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is taken.")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email is taken.")
                    return redirect('register')
                else:
                    # ***** register user
                    User.objects.create_user(username=username, password=password, email=email)

                    messages.success(request,
                                     "Registration successful. Please login")

                    return redirect('login')

        else:
            messages.error(request, 'Passwords don\'t match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


@unauthenticated_user
def login_user(request):
    # next_param = request.POST['next']

    if request.method == 'POST':  # form is submitted
        username = request.POST['username']
        password = request.POST['password']

        # authenticate user
        user = auth.authenticate(username=username, password=password)

        if user is not None:  # user exist in database
            auth.login(request, user)
            messages.success(request, f"Welcome {request.POST['username'].title()}, You are now logged in.")

            if user.is_staff:  # if user is staff
                return redirect('/')  # redirect to home
            else:
                return redirect('user_page')  # redirect to user_page
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)  # logout(): is an in-built django function that handles the logging out of the user
    messages.success(request, f"You are logged out.")
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def user_page(request):
    orders = request.user.customer.order_set.all()  # get all others relevant to a specific customer from the User model

    total_orders = orders.count()  # returns the total number of orders
    delivered = orders.filter(status='Delivered').count()  # returns total number of orders that have been 'Delivered'
    pending = orders.filter(status='Pending').count()  # returns the total number of orders that are 'Pending'

    context = {'orders': orders,
               'total_orders': total_orders,
               'delivered': delivered,
               'pending': pending,
               }
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def account_settings(request):
    current_customer = request.user.customer

    form = CustomerForm(instance=current_customer)  # instance: the form loads with the users details

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=current_customer)  # request.FILES: for files
        if form.is_valid():
            form.save()
            messages.success(request, f"Profile Updated.")

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


"""
@unauthenticated_user
def register_user(request):
    if request.method == 'POST':
        # form values
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']

        # password check
        if password != password2:
            messages.error(request, "Password don't match")
            return redirect('register')
        elif password == password2:
            # check username
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is taken.")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email is taken.")
                    return redirect('register')
                else:
                    # ***** register user
                    user = User.objects.create_user(username=username, password=password, email=email)

                    Customer.objects.create(user=user)  # create a Customer from the user object

                    group = Group.objects.get(name='customer')  # assign a new user to the 'customer' group
                    user.groups.add(group)  # add the users group to Django Group

                    # ***** login user
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in')
                    # return redirect('login_user')

                    user.save()
                    print(f"user:{user}\n username:{username}")

                    messages.success(request,
                                     "Registration successful. Please login")
                    return redirect('login')

        else:
            messages.error(request, 'Passwords don\'t match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


 in models.Customer
def __str__(self):
    return self.name

# in dashboard.html
<td>{{ customer.user }}</td>


def register_user(request):
    form = CreateUserForm()
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')  # assign a new user to the 'customer' group
            user.groups.add(group)  # add the users group to Django Group
            
            messages.success(request, f"Account created for {username.title()}")
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)
"""
