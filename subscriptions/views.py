from collections import defaultdict

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SubscriptionForm, RegisterForm
from .models import Subscription, Payment


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('sub_list')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def sub_list(request):
    subs = Subscription.objects.filter(user=request.user)

    query = request.GET.get('q', '').strip()
    if query:
        subs = subs.filter(title__icontains=query)

    category = request.GET.get('category')
    if category:
        subs = subs.filter(category=category)

    sort = request.GET.get('sort') or 'urgent'
    if sort == 'price_asc':
        subs = subs.order_by('price')
    elif sort == 'price_desc':
        subs = subs.order_by('-price')
    elif sort == 'urgent':
        subs = subs.order_by('billing_date')

    total_cost = sum(sub.price for sub in subs if sub.is_active)

    category_totals = defaultdict(int)
    for sub in subs:
        if sub.is_active:
            category_totals[sub.get_category_display()] += sub.price

    categories_with_icons = [
        (value, f"{Subscription.CATEGORY_ICONS[value]} {label}")
        for value, label in Subscription.CATEGORY_CHOICES
    ]

    context = {
        'subs': subs,
        'total_cost': total_cost,
        'category_totals': dict(category_totals),
        'categories': categories_with_icons,
        'current_category': category or '',
        'current_sort': sort,
        'current_query': query,
    }
    return render(request, 'subscriptions/sub_list.html', context)


@login_required
def sub_create(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            return redirect('sub_list')
    else:
        form = SubscriptionForm()

    return render(request, 'subscriptions/sub_form.html', {'form': form, 'title': 'Добавить подписку'})


@login_required
def sub_edit(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)

    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('sub_list')
    else:
        form = SubscriptionForm(instance=subscription)

    return render(request, 'subscriptions/sub_form.html', {'form': form, 'title': 'Редактировать подписку'})


@login_required
def sub_delete(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)

    if request.method == 'POST':
        subscription.delete()
        return redirect('sub_list')

    return render(request, 'subscriptions/sub_confirm_delete.html', {'subscription': subscription})


@login_required
def sub_pay(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)

    if request.method == 'POST':
        subscription.mark_as_paid()

    return redirect('sub_list')


@login_required
def payment_history(request):
    payments = Payment.objects.filter(subscription__user=request.user)
    total_paid = sum(p.amount for p in payments)

    return render(request, 'subscriptions/payment_history.html', {
        'payments': payments,
        'total_paid': total_paid,
    })


@login_required
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk, subscription__user=request.user)

    if request.method == 'POST':
        payment.delete()
        return redirect('payment_history')

    return render(request, 'subscriptions/payment_confirm_delete.html', {'payment': payment})


@login_required
def account_delete(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('login')

    return render(request, 'registration/account_confirm_delete.html')
