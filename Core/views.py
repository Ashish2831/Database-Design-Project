from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from .forms import *
from .models import *

# Create your views here.
def Home(request):
    categories_obj = Categories.objects.all()
    products_obj = Product.objects.all()
    return render(request, "Core/index.html", {'categories' : categories_obj, 'products' : products_obj})

def About(request):
    return render(request, "Core/about.html")

def Brand(request):
    categories = Categories.objects.all()
    products = Product.objects.all()
    return render(request, "Core/brand.html", {'categories' : categories, 'products' : products})

def Specials(request):
    return render(request, "Core/specials.html")

def Contact(request):
    return render(request, "Core/contact.html")

def Register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    emp_register = Registration_Form()
    if request.method == "POST":
        register = Registration_Form(request.POST) 
        if register.is_valid():
            register.save()
            return render(request, "Core/registration.html", {'register' : emp_register, 'success' : 'Registered Successfully!!'})
        else:
            return render(request, "Core/registration.html", {'register' : register})
    return render(request, "Core/registration.html", {'register' : emp_register})

def ShowProduct(request, cate_id,  prod_id):
    category = Categories.objects.get(pk=cate_id)
    product = Product.objects.get(pk=prod_id)
    return render(request, 'Core/showproduct.html', {'category' : category, 'product' : product})

@login_required()
def AddToCart(request, cate_id,  prod_id):
    current_cart = request.session.get('Cart', None)
    if current_cart == None:
        request.session['Cart'] = {cate_id : [prod_id]}
        messages.success(request, "Product Successfully Added to Cart!!")
    elif str(cate_id) not in current_cart:
        request.session['Cart'].update({f"{cate_id}" : [f"{prod_id}"]})
        request.session.modified = True
        messages.success(request, "Product Successfully Added to Cart!!")
    elif prod_id not in request.session.get('Cart').get(str(cate_id)):
        request.session.get('Cart').get(str(cate_id)).append(prod_id)
        request.session.modified = True
        messages.success(request, "Product Successfully Added to Cart!!")
    else:
        messages.success(request, "Product is Already There in Cart!!")
    return HttpResponseRedirect(f"/show/{cate_id}/{prod_id}/")

@login_required()
def ViewCart(request):
    cart = request.session.get('Cart')
    categories = []
    products = []
    if cart != None:
        for cate_id in cart:
            categories.append(Categories.objects.get(pk=int(cate_id)))
            for prod_id in cart[cate_id]:
                products.append(Product.objects.get(pk=prod_id))
    return render(request, 'Core/viewcart.html', {'categories' : categories, 'products' : products})

@login_required()
def EmptyCart(request):
    if 'Cart' in request.session:
        del request.session['Cart']
    return HttpResponseRedirect('/view-cart/')

@login_required()
def DeleteProduct(request, cate_id,  prod_id):
    cart = request.session.get('Cart')
    if cart != None:
        for cate in cart:
            if int(cate) == cate_id:
                for prod in cart[cate]:
                    if prod == prod_id:
                        cart[cate].remove(prod_id)
                        request.session.modified = True

    return HttpResponseRedirect('/view-cart/')

@login_required()
def CheckOut(request, cate_id, prod_id):
    category = Categories.objects.get(pk=cate_id)
    product = Product.objects.get(pk=prod_id)
    emp_order_form = Order_Form()
    sizes = Size.objects.filter(category_id=cate_id)
    if request.method == "POST":
        order_form = Order_Form(request.POST)
        if order_form.is_valid():
            total_amount = product.price * int(order_form.cleaned_data.get('quantity'))

            order = Order()
            order.contact_person = order_form.cleaned_data.get('contact_person')
            order.contact_number = order_form.cleaned_data.get('contact_number')
            order.email = order_form.cleaned_data.get('email')
            order.quantity = order_form.cleaned_data.get('quantity')
            order.shipping_address = order_form.cleaned_data.get('shipping_address')
            order.date = order_form.cleaned_data.get('date')
            order.total_payment = total_amount
            order.save()

            latest_order_id = Order.objects.latest('id')
            order_details = Orders_Detail()
            order_details.order_id = latest_order_id
            order_details.product_id = product
            order_details.quantity = order_form.cleaned_data.get('quantity')
            size_val = request.POST['size']
            size_obj = None
            for obj in sizes:
                if int(size_val) == obj.size:
                    size_obj = obj
            order_details.size_id = size_obj
            order_details.unit_price = product.price
            order_details.product_total = total_amount
            order_details.save()

            request.session['Order-id'] = latest_order_id.id
            return HttpResponseRedirect(f"/process-payment/{cate_id}/{prod_id}/")
        else:
            return render(request, 'Core/checkout.html', {'order_form' : order_form, 'sizes' : sizes, 'category' : category, 'product' : product})
    return render(request, 'Core/checkout.html', {'order_form' : emp_order_form, 'sizes' : sizes, 'category' : category, 'product' : product})

def Process_Payment(request, cate_id, prod_id):
    host = request.get_host()
    order = Orders_Detail.objects.get(order_id=request.session['Order-id'])
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': order.product_total,
        'item_name': order.product_id,
        'invoice': str(request.session['Order-id']),
        'currency_code': 'INR',
        'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,reverse('Payment_Done', kwargs={'cate_id': cate_id, 'prod_id' : prod_id})),
        'cancel_return': 'http://{}{}'.format(host,reverse('Payment_Cancelled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'Core/process_payment.html', {'form': form, 'amount' : order.product_total})

@csrf_exempt
def Payment_Done(request, cate_id, prod_id):
    messages.success(request, "Order Placed Successfully!!")
    cart = request.session.get('Cart')
    if cart != None:
        for cate in cart:
            if int(cate) == cate_id:
                for prod in cart[cate]:
                    if prod == prod_id:
                        cart[cate].remove(prod_id)
                        request.session.modified = True
    order = Order.objects.get(pk=request.session['Order-id'])
    order.payment_status = True
    return HttpResponseRedirect('/view-cart/')

@csrf_exempt
def Payment_Cancelled(request):
    messages.error(request, "Payment Cancelled!!")
    return HttpResponseRedirect('/view-cart/')
