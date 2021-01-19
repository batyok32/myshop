from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order
from shop.models import Comment, Contact
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user = authenticate(request, 
                                username=cd['username'],
                                password=cd['password'])

            if user is not None:
                if  user.is_active:
                    login(request, user)
                    return HttpResponse('Authentication succesfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form':form})

@login_required
def dashboard(request):
    lis=[]
    user = request.user
    print('trying to take orders')
    orders = Order.objects.filter(user=user, active=True).order_by('created')
    count=orders.count()
    pint=0
    for order in orders:
        pint=pint+int(order.get_total_cost())
        print("pint: ", pint)
    # total = sum(float(order.get_total_cost) for order in orders)
    # total = [order.get_total_cost for order in orders]
    # print("total orders price:", total)
    # for t in total:
    #     lis.append(str(t))
    # print("lis:", lis)
    # lis=sum(int(lis))
    # print("sUccessfull")
    total=pint
    comments = Comment.objects.filter(user=user)
    comments=comments.count()
    contacts=Contact.objects.filter(user=user)
    contacts = contacts.count()
    print('took orders', orders)
    return render(request,
            'account/dashboard.html',
            {'section': 'dashboard',
            'orders': orders,
            'count':count,
            'total':total,
            'comments':comments,
            'contacts':contacts
            })

@login_required
def order_detail(request, id):
    user = request.user
    # print('trying to take orders')
    # all_orders = Order.objects.all()
    order = get_object_or_404(Order, id=id)
    if order.user != user:
        messages.error(request, 'You have not access to this order')
        return redirect('dashboard')

    # orders = Order.objects.filter(user=user).order_by('created')
    # print('took orders', orders)
    return render(request,
            'account/order_details.html',
            {'section': 'dashboard',
            'order': order})

@login_required
def order_delete(request, id):
    user = request.user
    order = get_object_or_404(Order, id=id, active=True, user=user)
    order.active=False
    order.save()
    return redirect('dashboard')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user but avoid saving it
            new_user=user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            cd =user_form.cleaned_data
            # Create the user profile
            Profile.objects.create(user=new_user, phone_number=cd['phone_number'])
            return render(request, 
                        'account/register_done.html',
                        {'new_user':new_user})
    else:
        user_form=UserRegistrationForm()
    return render(request, 
                'account/register.html',
                {'user_form':user_form})           


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                data=request.POST)
        profile_form = ProfileEditForm(
                                    instance = request.user.profile,
                                    data=request.POST,
                                    files = request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)
    return render(request,
                'account/edit.html',
                {'user_form':user_form,
                'profile_form':profile_form})