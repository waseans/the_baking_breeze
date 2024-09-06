from django.shortcuts import render, get_object_or_404
from .models import Product
# views.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem

def home(request):
    products = Product.objects.all()
    return render(request, 'homepage.html', {'products': products})


def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_details.html', {'product': product})

def contact(request):
    return render(request, 'contact.html')

def about_us(request):
    return render(request, 'about_us.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after successful login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords don't match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Signup successful. Please login.")
        return redirect('login')
    
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to login page after logout

# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Order, OrderItem




# views.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem

# views.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, CartItem, Cart

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()

        return JsonResponse({'status': 'success', 'message': 'Product added to cart'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})




@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate total price for each item
    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    return render(request, 'view_cart.html', {'cart_items': cart_items})


# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import CartItem

from django.http import JsonResponse
@login_required
def update_cart(request, cart_item_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            # Get the cart item
            cart_item = CartItem.objects.get(id=cart_item_id)

            # Get the quantity from the request
            quantity = int(request.POST.get('quantity'))

            if quantity > 0:
                # Update the cart item quantity
                cart_item.quantity = quantity
                cart_item.save()
                return JsonResponse({'success': True, 'new_quantity': cart_item.quantity})
            else:
                # If quantity is 0 or less, remove the item from the cart
                cart_item.delete()
                return JsonResponse({'success': True, 'removed': True})

        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart item does not exist.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)



from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Cart, Order
from django.conf import settings
import razorpay
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import razorpay
from .models import Cart, CartItem, Order

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
import razorpay
from .models import Cart, CartItem, Order, OrderItem
from django.shortcuts import render, redirect
from django.conf import settings
import razorpay

from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, OrderItem
import razorpay
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, OrderItem
# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, OrderItem
import razorpay
from django.conf import settings

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')

        if payment_method == 'cod':
            # Save the order and clear the cart
            order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                address=address,
                city=city,
                state=state,
                zip_code=zip_code,
                phone=phone,
                total_price=total_price,
                payment_method=payment_method,
                status='ordered'
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            cart_items.delete()  # Clear the cart
            return redirect('order_confirmation')  # Redirect to confirmation

        elif payment_method == 'razorpay':
            # Create a Razorpay order
            razorpay_order = client.order.create(dict(
                amount=int(total_price * 100),  # Amount in paise
                currency='INR',
                payment_capture='1'
            ))
            order_id = razorpay_order['id']
            
            # Save the order details and return the Razorpay order ID
            request.session['order_data'] = {
                'full_name': full_name,
                'address': address,
                'city': city,
                'state': state,
                'zip_code': zip_code,
                'phone': phone,
                'total_price': total_price,
                'payment_method': payment_method
            }
            return render(request, 'razorpay_checkout.html', {
                'order_id': order_id,
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'amount': total_price * 100  # Amount in paise
            })

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def verify_payment(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        # Verify the payment signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        try:
            client.utility.verify_payment_signature(params_dict)
            # Save the order
            order_data = request.session.pop('order_data', {})
            order = Order.objects.create(
                user=request.user,
                full_name=order_data['full_name'],
                address=order_data['address'],
                city=order_data['city'],
                state=order_data['state'],
                zip_code=order_data['zip_code'],
                phone=order_data['phone'],
                total_price=order_data['total_price'],
                payment_method='razorpay',
                status='ordered'
            )
            for item in CartItem.objects.filter(cart__user=request.user):
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            CartItem.objects.filter(cart__user=request.user).delete()
            return redirect('order_confirmation')

        except Exception as e:
            # Handle verification errors
            print(f"Verification error: {e}")
            return redirect('checkout')  # Redirect to checkout on failure
    return redirect('checkout')


def order_confirmation(request):
    return render(request, 'order_confirmation.html')

from django.shortcuts import render
from .models import Order

@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')

    return render(request, 'user_orders.html', {
        'orders': orders,
    })

from django.shortcuts import render, get_object_or_404
from .models import Order

@login_required
def order_details_full(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_details_full.html', {'order': order})


