from django.shortcuts import render
from django import forms
from django.db import IntegrityError
from .models import * 
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from PIL import Image, ImageOps
import json
from django.views.decorators.csrf import csrf_exempt

#def change_background(image):
#    img = Image.open(image)
#    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
#        img=img.convert('RGB')
#    new_img = Image.new('RGB', img.size, (255, 255, 255))
#    new_img.paste(img, (0, 0), img)
#    inverted_img = ImageOps.invert(new_img)
#    return inverted_img

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Last Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))
    password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter Password'}))

class CompanyRegistrationForm(forms.Form):
    company_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Company Name'}))
    company_email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Company Email Address'}))

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

class AddBusinessForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Store Name'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 30, 'placeholder': 'Description'}))
    image = forms.ImageField(required=False)

class BusinessGoodsForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Item Name'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 30, 'placeholder': 'Description'}))
    image = forms.ImageField(required=False)
    price = forms.IntegerField()

def home_page(request):
    return render(request, 'emcom/home.html', {
        'form': RegistrationForm(),
        'login_form': LoginForm(),
        #'company_form': CompanyRegistrationForm()
    })

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            password_confirmation = form.cleaned_data['password_confirmation']
            if password != password_confirmation:
                return render(request, "emcom/register.html", {
                    "message": "Passwords must match.",
                    'registration_form': RegistrationForm(request.POST)
                })
            try:
                user = User.objects.create_user(username, email, password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                #token = get_random_string(length=32)
                #user.email_verification_token = token
                #user.save()

                # Send verification email
                #verification_url = request.build_absolute_uri(reverse('verify_email', args=[token]))
                #send_verification_email(email, verification_url)

            except IntegrityError:
                return render(request, "emcom/register.html", {
                    "message": "Username already taken.",
                    'registration_form': RegistrationForm(request.POST)
                })
            return HttpResponseRedirect(reverse("login"))
    else:
        return render(request, "emcom/home.html", {
            'form': RegistrationForm(),
            'login_form': LoginForm(),
        })

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None: #and user.email_verified == True:
                login(request, user)
                return HttpResponseRedirect(reverse("home_page"))
        #elif user is not None and user.email_verified == False:
        #    return render(request, "betapp/login.html", {
        #        "message": "You need to verify your email before you can login. Check the email you used to register for the link."
        #    })
            else:
                return render(request, "emcom/home.html", {
                    "message": "Invalid username or password.",
                    'form': RegistrationForm(),
                    'company_form': CompanyRegistrationForm(),
                    'login_form': LoginForm()
                })
    else:
        return HttpResponseRedirect(reverse('home_page'))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home_page"))

@login_required
def my_business(request):
    user = User.objects.get(username=request.user)
    return render(request, 'emcom/my_business.html', {
        'businesses': Business.objects.filter(user=user),
        'business_form': AddBusinessForm,
    })

def add_business(request):
    if request.method == 'POST':
        form = AddBusinessForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']
            Business.objects.create(user=request.user, name=name, description=description, image=image)
            return HttpResponseRedirect(reverse('business'))
    else:
        pass

def business_detail(request, id):
    business = Business.objects.get(id=id)
    if request.method == 'POST':
        form = BusinessGoodsForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            image = form.cleaned_data['image']
            BusinessGoods.objects.create(business=business, item_name=name, description=description, image=image, price=price)
            return HttpResponseRedirect(reverse(business_detail, args=[business.id]))
        #put an Http404 here with response, form isnt valid
    else:
        return render(request, 'emcom/business_detail.html',{
            'business': business,
            'item_form': BusinessGoodsForm(),
            'business_items': BusinessGoods.objects.filter(business=business),
        })

@login_required
def marketplace(request):
    businesses = Business.objects.all()
    return render(request, 'emcom/marketplace.html', {
        'businesses': businesses,
        'business_items': BusinessGoods.objects.all(),
    })

@csrf_exempt
def delete_item(request, item_id):
    if request.method == 'POST':
        data = request.body.decode()
        data = json.loads(data)
        id = data['item_id']
        BusinessGoods.objects.get(id=id).delete()
        return HttpResponse('OK')

def update_item(request, item_id):
    if request.method == 'POST':
        data = request.body.decode()
        data = json.loads(data)
        id = data['item_id']
        name = data['item_name']
        description = data['item_description']
        price = data['item_price']
        price = price.split('#')
        price = price[1]
        business_item = BusinessGoods.objects.get(id=item_id)
        business_item.item_name = name
        business_item.description = description
        business_item.price = price
        business_item.save()
        return HttpResponse('OK')