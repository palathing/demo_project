from django.shortcuts import render,redirect
from . models import Category,Product
from cart.models import Cart
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'home.html')

def category(request):
    item=Category.objects.all()
    return render(request,'category.html',{'item':item})

def products(request,id):
    # p=Product.objects.filter(category__id=i)  #this method can also be used
    c=Category.objects.get(id=id)
    p=Product.objects.filter(category=id)
    return render(request,'product.html',{'c':c,'p':p})

def product_details(request,id):
    product=Product.objects.get(id=id)
    return render(request,'product_details.html',{'product':product})

def register(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']
        c = request.POST['c']
        f = request.POST['f']
        l = request.POST['l']
        e = request.POST['e']
        if (c == p):
            s = User.objects.create_user(username=u, password=p, first_name=f, last_name=l,email=e)
            s.save()
            return redirect('shop:home')
    return render(request,'register.html')

def user_login(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect('shop:home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request,'user_login.html')

def user_logout(request):
    logout(request)
    return redirect('shop:user_login')

def buy(request,id):
    p = Product.objects.get(id=id)
    u = request.user
    try:
        p.stock -= 1
        p.save()
    except:
        pass
    return redirect('cart:place_order')