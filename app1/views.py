from django.shortcuts import render , redirect
from .models import *
import bcrypt
from django.contrib import messages

def main(request):
    return render(request, 'main.html')

def login(request):
    return render(request, "login.html")


def login_form(request):
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.filter(email=email).first()
    if user:
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session['user_id'] = user.id
            return redirect('/')
    messages.error(request, 'Invalid Credentials')
    return redirect('/login')


def register(request):
    return render(request, "register.html")


def registration(request):
    errors = User.objects.basic_validator(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/register')
    else:
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=fname, last_name=lname,email=email, password=hashed)
        user = User.objects.last()
        request.session['user_id'] = user.id
    return redirect('/')

def boys(request):
    boys_clothes=Cloth.objects.all()
    context={
        'boys_clothes':boys_clothes,
    }
    return render(request,'boy.html',context)

def girls(request):
    girls_clothes=Cloth.objects.all()
    context={
        'girls_clothes':girls_clothes,
    }
    return render(request,'girl.html',context)

def view_cloth(request,id):
    context={
        'cloth':Cloth.objects.get(id=id),
    }
    return render(request,'view.html',context)

def checkout(request):
    # errors = Address.objects.basic_validator(request.POST)
    # # check if the errors dictionary has anything in it
    # if len(errors) > 0:
    #     # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
    #     for key, value in errors.items():
    #         messages.error(request, value)
    #     # redirect the user back to the form to fix the errors
    #     return redirect('/')
    return render(request, "checkout.html")


def admin(request):
    return render(request,'admin.html')



def create_cloth(request):
    errors = Cloth.objects.basic_validator(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        size=request.POST['size']
        gender=request.POST['gender']
        pic_src=request.POST['pic_source']
        description=request.POST['description']
        price=request.POST['price']
        quantity=request.POST['quantity']
        Cloth.objects.create(size=size, gender=gender, pic_src=pic_src,description=description, price=price, quantity=quantity)
        cloth=Cloth.objects.last()
        if cloth.gender == 'boys':
            return redirect('/boys')
        else:
            return redirect('/girls')

def add_to_cart(request,id):
    user=User.objects.get(id=request.session['user_id'])
    Order.objects.create(user=user)
    OrderCloth.objects.create(order=Order.objects.last(),cloth=Cloth.objects.get(id=id),quantity=int(request.POST['quantity']))
    return redirect('/cart')

# def cart(request):
#     user=User.objects.get(id=request.session['user_id'])
#     order=Order.objects.filter(user=user)
#     total_items=sum([oc.quanity for oc in order.ordercloth_set.all()])
#     total_price=sum([oc.quanity * oc.cloth.price  for oc in order.ordercloth_set.all()])
#     context={
#         'all_cloth_orders':order.orderclothes.all(),
#         'total_items':total_items,
#         'total_price':total_price
#     }
#     return render(request,'cart.html',context)

def cart(request):
    user = User.objects.get(id=request.session['user_id'])
    order = Order.objects.filter(user=user).first() # get the first order for the user
    order_clothes = OrderCloth.objects.filter(order=order) # filter OrderCloth objects by order id
    total_items = sum([oc.quantity for oc in order_clothes])
    total_price = sum([oc.quantity * oc.cloth.price for oc in order_clothes])
    context = {
        'all_cloth_orders': order_clothes,
        'total_items': total_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)


