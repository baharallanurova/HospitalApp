from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from hospital.models import Patient
from pharmacy.models import Medicine, Cart, Order
from .utils import searchMedicines


@login_required(login_url="login")
def pharmacy_single_product(request, pk):
    if not request.User.is_patient:
        messages.error(request, 'Not Authorized')
        return redirect('login')

    patient = get_object_or_404(Patient, user=request.user)
    medicine = get_object_or_404(Medicine, pk=pk)
    orders = Order.objects.filter(user=request.user, ordered=False)
    carts = Cart.objects.filter(user=request.user, purchased=False)

    context = {
        'patient': patient,
        'medicine': medicine,
        'carts': carts,
        'orders': orders
    }
    return render(request, 'pharmacy/product-single.html', context)


@login_required(login_url="login")
def pharmacy_shop(request):
    if not request.User.is_patient:
        messages.error(request, 'Not Authorized')
        return redirect('login')

    patient = get_object_or_404(Patient, user=request.user)
    medicines = Medicine.objects.all()
    orders = Order.objects.filter(user=request.user, ordered=False)
    carts = Cart.objects.filter(user=request.user, purchased=False)
    medicines, search_query = searchMedicines(request)

    context = {
        'patient': patient,
        'medicines': medicines,
        'carts': carts,
        'orders': orders,
        'search_query': search_query
    }
    return render(request, 'pharmacy/shop.html', context)


@login_required(login_url="login")
def checkout(request):
    if not request.User.is_patient:
        messages.error(request, 'Not Authorized')
        return redirect('login')
    return render(request, 'pharmacy/checkout.html')


@login_required(login_url="login")
def add_to_cart(request, pk):
    if not request.User.is_patient:
        messages.error(request, 'Not Authorized')
        return redirect('login')

    item = get_object_or_404(Medicine, pk=pk)
    order_item, created = Cart.objects.get_or_create(
        item=item,
        user=request.user,
        purchased=False
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, f"Updated {item.name} quantity")
        else:
            order.orderitems.add(order_item)
            messages.info(request, f"Added {item.name} to your cart")
    else:
        order = Order.objects.create(user=request.user)
        order.orderitems.add(order_item)
        messages.info(request, f"Added {item.name} to your cart")

    return redirect('pharmacy_shop')


@login_required(login_url="login")
def cart_view(request):
    if not request.User.is_patient:
        messages.error(request, 'Not Authorized')
        return redirect('login')

    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)

    if carts.exists() and orders.exists():
        order = orders[0]
        context = {'carts': carts, 'order': order}
        return render(request, 'pharmacy/cart.html', context)
    else:
        messages.info(request, "You don't have any items in your cart")
        return redirect('pharmacy_shop')


@login_required(login_url="login")
def remove_from_cart(request, pk):
    if not request.User.is_patient:
        messages.error(request, 'Not Authorized')
        return redirect('login')

    item = get_object_or_404(Medicine, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user,
                purchased=False
            )[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.info(request, f"{item.name} was removed from your cart")
            return redirect('cart')
        else:
            messages.info(request, f"{item.name} was not in your cart")
            return redirect('pharmacy_shop')
    else:
        messages.info(request, "You don't have an active order")
        return redirect('pharmacy_shop')


@login_required(login_url="login")
def increase_cart(request, pk):
    if not request.User.is_patient:
        messages.error(request, 'Not Authorized')
        return redirect('login')

    item = get_object_or_404(Medicine, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user,
                purchased=False
            )[0]
            order_item.quantity += 1
            order_item.save()
            messages.info(request, f"Updated {item.name} quantity")
            return redirect('cart')
        else:
            messages.info(request, f"{item.name} is not in your cart")
            return redirect('pharmacy_shop')
    else:
        messages.info(request, "You don't have an active order")
        return redirect('pharmacy_shop')


@login_required(login_url="login")
def decrease_cart(request, pk):
    if not request.User.is_patient:
        messages.error(request, 'Not Authorized')
        return redirect('login')

    item = get_object_or_404(Medicine, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(
                item=item,
                user=request.user,
                purchased=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"Updated {item.name} quantity")
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.info(request, f"{item.name} was removed from your cart")
            return redirect('cart')
        else:
            messages.info(request, f"{item.name} is not in your cart")
            return redirect('pharmacy_shop')
    else:
        messages.info(request, "You don't have an active order")
        return redirect('pharmacy_shop')