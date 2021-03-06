from django.shortcuts import redirect, render
from accounts.forms import LoginForm, UserRegistrationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import verified
from django.conf import settings

from wallets.api import WalletsClient
from wallets.models import Wallet

from cryptography.fernet import Fernet
from wallets.forms import BVNForm

wallet = WalletsClient(secret_key="hfucj5jatq8h", public_key="uvjqzm5xl6bw")
fernet = Fernet(settings.ENCRYPTION_KEY)
# Create your views here.

def register(request):
    form = UserRegistrationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            new_user = form.save()
            messages.success(request, 'Account succesfully created. You can now login')
            return redirect('accounts:login')
    return render(request, "accounts/register.html", context = {"form":form})



def login_user(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email = cd['email'], password = cd['password'])
            if user is not None:
                login(request, user)
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Account does not exist')
    return render(request, "accounts/login.html", context = {"form":form})



@login_required
@verified
def dashboard(request):
    return render(request, "dashboard.html", context={})


@login_required
def logout_user(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def create_wallet(request):
    form = BVNForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            bvn = cd["bvn"]
            new_wallet = wallet.create_user_wallet(
                    first_name= user.first_name,
                    last_name= user.last_name,
                    email=user.email,
                    date_of_birth= user.date_of_birth.strftime('%Y-%m-%d'),
                    bvn= str(bvn)
                )
            if new_wallet["response"]["responseCode"] == '200':
                user.verified = True
                user.save()
                Wallet.objects.create(
                    user = user,
                    balance = new_wallet["data"]["availableBalance"],
                    account_name = new_wallet["data"]["accountName"],
                    account_number = new_wallet["data"]["accountNumber"],
                    bank = new_wallet["data"]["bank"],
                    phone_number = new_wallet["data"]["phoneNumber"],
                    password = fernet.encrypt(new_wallet["data"]["password"].encode())
                )
                messages.success(request, "Account verified, wallet successfully created")
                return redirect("accounts:dashboard")
            else:
                messages.error(request, new_wallet["response"]["message"])
           
    return render(request, "accounts/bvn.html", context = {"form":form})