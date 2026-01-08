from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from productsapp.models import Product
from cartapp.models import Cart,CartItem

def create_cartId(request):
    cart = request.session.session_key
    if not cart :
        cart=request.session.create()
    return cart

@login_required(login_url="/login")
def removeCart(request,product_id):   
  cart=Cart.objects.get(cart_id=create_cartId(request),customer=request.user)
  product=Product.objects.get(pk=product_id)
  cartItem=CartItem.objects.get(product=product,cart=cart) # Product for Delete
  cartItem.delete()
  return redirect("/cart")

# Create your views here.
@login_required(login_url="/login")
def cart(request):
    counter=0
    total=0
    try:
        # Pull Data Cart
        cart=Cart.objects.get(cart_id=create_cartId(request),customer=request.user)
        # Pull Data in Cart
        cartItem=CartItem.objects.filter(cart=cart)
        for item in cartItem:
            counter+=item.quantity 
            total+=(item.product.price * item.quantity)
    except (Cart.DoesNotExist,CartItem.DoesNotExist):
        cart=None
        cartItem=None
    return render(request,"cart.html",{"cartItem":cartItem,"total":total,"counter":counter})

@login_required(login_url="/login")
def addCart(request,product_id):
    product=Product.objects.get(pk=product_id)
    # Create Cart
    try:
        # Case 1: Have Cart
        cart=Cart.objects.get(cart_id=create_cartId(request))
    except Cart.DoesNotExist:
     # Case 1: Have't Cart
        cart=Cart.objects.create(
          cart_id=create_cartId(request),
          customer=request.user
    )
        cart.save()
     # Record Product list to Cart 
    try:
       # Buy Product Repeat
       cartitem=CartItem.objects.get(product=product,cart=cart)
       if cartitem.quantity<cartitem.product.stock:
           cartitem.quantity+=1
           cartitem.save()
    except CartItem.DoesNotExist:
       # Begin Buy Product
       cartitem=CartItem.objects.create(
          product=product,
          cart=cart,
          quantity=1
    )
       cartitem.save()
    return redirect("/cart")

