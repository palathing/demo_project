from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . models import Cart,Payment,Order_table
from shop.models import Product
from django.contrib.auth.decorators import login_required
import razorpay
from django.contrib.auth import login

# Create your views here.

@login_required
def add_to_cart(request,id):
    p=Product.objects.get(id=id)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(p.stock>0):
            cart.quantity += 1
            cart.save()
            p.stock -= 1
            p.save()
    except:
        if(p.stock):
            cart=Cart.objects.create(product=p,user=u,quantity=1)
            cart.save()
            p.stock -= 1
            p.save()
    return redirect('cart:cart_views')

@login_required
def cart_views(request):
    u=request.user
    cart=Cart.objects.filter(user=u)
    total=0
    for i in cart:
        total=total+i.quantity*i.product.price
    return render(request,'cart.html',{'cart':cart,'total':total})

def cart_remove(request,id):
    p = Product.objects.get(id=id)
    u = request.user
    # cart = Cart.objects.get(user=u, product=p)
    # cart.quantity -= 1
    # cart.save()
    # p.stock += 1
    # p.save()
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(cart.quantity>1):
            cart.quantity -=1
            cart.save()
            p.stock +=1
            p.save()
        else:
            cart.delete()
            p.stock +=1
            p.save()
    except:
        pass
    return redirect('cart:cart_views')

def cart_trash(request,id,c_id):
    user=request.user
    p=Product.objects.get(id=id)
    cart=Cart.objects.get(user=user,product=p)
    q=cart.quantity
    p.stock=p.stock+q
    p.save()
    c=Cart.objects.get(id=c_id)
    c.delete()
    return redirect('cart:cart_views')

# can also pass 1 id. refer below code
# def cart_trash(request,id):
#     p=Product.objects.get(id=id)
#     u=request.user
#     try:
#         cart=Cart.objects.get(user=u,product=p)
#         cart.delete()
#         p.stock=p.stock+cart.quantity
#         p.stock()
#     except:
#         pass
#     return redirect('cart:cart_views')

def place_order(request):
    if(request.method=='POST'):
        ph=request.POST.get('p')
        a=request.POST.get('a')
        n=request.POST.get('n')
        u=request.user
        c=Cart.objects.filter(user=u)   #cart for current user
        total=0
        for i in c:
            total=total+(i.quantity*i.product.price)    #to get total amount
        total=int(total*100)

        #create Razorpay client using our API credentials
                                          #keyid                      #secretkey
        client=razorpay.Client(auth=('rzp_test_IeuNEvE2rTYxQD','sqsdZCinYPjhr7qnW5dm26li'))

        #Create order in Razorpay
        response_payment=client.order.create(dict(amount=total,currency='INR'))
        print(response_payment)
        order_id=response_payment['id']     #retrive the order_id returned from razorpay response
        order_status=response_payment['status']     #retrive the status returned from razorpay response
        if order_status=="created":     #if status is order created then we save order id in payment table
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()
            for i in c:
                o=Order_table.objects.create(user=u,product=i.product,address=a,phone=ph,pin=n,no_of_items=i.quantity,order_id=order_id)
                o.save()
        response_payment['name']=u.username
        return render(request,'payment.html',{'payment':response_payment})
    return render(request,'place_order.html')

@csrf_exempt        #if csrf related error should not come while running
def status(request,u):
    print(request.user.is_authenticated)    #it should be false
    if not request.user.is_authenticated:   #this 3 lines is for making it in log_in page itself after payment. Coz before it was loggin_out after payment
        u = User.objects.get(username=u)
        login(request,u)
        print(u.is_authenticated)   #when it is true
    if(request.method=="POST"):
        response=request.POST          #Razorpay response after completion of payment
        print(response)
        print(u)
        param_dict={
            'razorpay_order_id':response['razorpay_order_id'],      #this cam from terminal after print(response) is given
            'razorpay_payment_id':response['razorpay_payment_id'],
            'razorpay_signature':response['razorpay_signature']
        }
        client = razorpay.Client(auth=('rzp_test_IeuNEvE2rTYxQD', 'sqsdZCinYPjhr7qnW5dm26li'))
        try:
            status=client.utility.verify_payment_signature(param_dict)  #to check the authentication of razorpay signature
            print(status)
            #retrive a payment record with particular order_id
            ord=Payment.objects.get(order_id=response['razorpay_order_id'])
            ord.razorpay_payment_id=response['razorpay_payment_id'] #edits payment id response['razorpay_payment_id']
            ord.paid=True   #edit to paid
            ord.save()

            u=User.objects.get(username=u)
            c=Cart.objects.filter(user=u)
            #filter the order_table details for particular user with order_id=response['razorpay_order_id']
            o=Order_table.objects.filter(user=u,order_id=response['razorpay_order_id'])
            for i in o:
                i.payment_status="paid" #edit payment_status="paid"
                i.save()
            c.delete()
            return render(request,'status.html',{'status':True})
        except:
            return render(request,'status.html',{'status':False})
    return render(request,'status.html')

@login_required
def your_orders(request):
    u=request.user
    customer=Order_table.objects.filter(user=u,payment_status="paid")
    return render(request,'your_orders.html',{'customer':customer,'u':u.username})