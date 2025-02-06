

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense,product_name
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from userpreferences.models import UserPreference
import datetime
import json
from django.db.models import Q
from .models import Expense
from rest_framework.decorators import api_view
from django.utils.timezone import now
from django.db.models import Sum, Count
from rest_framework.response import Response
from .serializers import SalesRecordSerializer
from rest_framework import viewsets
from django.db.models.functions import TruncDay, TruncWeek

class SalesRecordViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = SalesRecordSerializer
    
@api_view(['GET'])
def dashboard_data(request):
    current_month = now().month
    total_revenue = Expense.objects.filter(date__month=current_month).aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_sales = Expense.objects.filter(date__month=current_month).count()

    top_products = Expense.objects.values('product_name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
    sales_trends = Expense.objects.filter(date__month=current_month).values('date').annotate(revenue=Sum('total_price')).order_by('date')

    revenue_by_salesperson = Expense.objects.values('category').annotate(total_revenue=Sum('total_price')).order_by('-total_revenue')
    low_stock_products = (
        Expense.objects
        .values('product_name')
        .annotate(total_quantity=Sum('quantity'))
        .filter(total_quantity__lt=5)
        .order_by('total_quantity')
    )
    return Response({
        "total_revenue": total_revenue,
        "total_sales": total_sales,
        "top_products": list(top_products),
        "sales_trends": list(sales_trends),
        "revenue_by_salesperson": list(revenue_by_salesperson),
        "low_stock_products": list(low_stock_products),
    })


def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    products = product_name.objects.all() 

    context = {'expense': expense, 'values': expense, 'categories': categories, 'products': products}

    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        date = request.POST.get('expense_date')
        category = request.POST.get('category')
        customer_name = request.POST.get('customer_name')
        selected_product_name = request.POST.get('product_name')
        total_price = request.POST.get('total_price')
        quantity = request.POST.get('quantity')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)

        # Update expense details
        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.customer_name = customer_name
        expense.product_name = selected_product_name
        expense.total_price = total_price
        expense.quantity = quantity

        expense.save()
        messages.success(request, 'Expense updated successfully')
        return redirect('expenses')



@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    product_names = product_name.objects.all()

    expenses = Expense.objects.filter(owner=request.user).order_by('-date') 
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = 'USD' 

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)



@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    product_names = Expense.objects.values_list('product_name', flat=True).distinct()

    context = {'categories': categories,'product_names':product_names, 'values': request.POST}

    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST.get('amount')  
        date = request.POST.get('expense_date')
        category = request.POST.get('category')
        customer_name = request.POST.get('customer_name')
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)

        if not quantity:
            messages.error(request, 'Quantity is required')
            return render(request, 'expenses/add_expense.html', context)

        try:
            amount = float(amount)
            quantity = int(quantity)
            total_price = amount * quantity  
        except ValueError:
            messages.error(request, 'Invalid input: Amount should be a number and Quantity should be an integer.')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(
            owner=request.user,
            customer_name=customer_name,
            product_name=product_name,
            amount=amount,
            date=date,
            category=category,
            quantity=quantity,
            total_price=total_price
        )

        messages.success(request, 'Expense saved successfully')
        return redirect('expenses')



@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    products = product_name.objects.all()  # Query using 'product_name'

    context = {'expense': expense, 'values': expense, 'categories': categories, 'products': products}

    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        date = request.POST.get('expense_date')
        category = request.POST.get('category')
        customer_name = request.POST.get('customer_name')
        selected_product_name = request.POST.get('product_name')
        total_price = request.POST.get('total_price')
        quantity = request.POST.get('quantity')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)

        # Update expense details
        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.customer_name = customer_name
        expense.product_name = selected_product_name
        expense.total_price = total_price
        expense.quantity = quantity

        expense.save()
        messages.success(request, 'Expense updated successfully')
        return redirect('expenses')


@login_required(login_url='/authentication/login')
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')


@login_required(login_url='/authentication/login')
def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte=todays_date)

    final_report = {}

    def get_expense_category_amount(category):
        return sum(exp.amount for exp in expenses.filter(category=category))

    for category in set(exp.category for exp in expenses):
        final_report[category] = get_expense_category_amount(category)

    return JsonResponse({'expense_category_data': final_report}, safe=False)

@login_required(login_url='/authentication/login')
def sales_trends(request):
    today = now().date()
    first_day_of_month = today.replace(day=1)
    
    interval = request.GET.get('interval', 'daily').lower()

    sales = Expense.objects.filter(owner=request.user, date__gte=first_day_of_month, date__lte=today)

    if not sales.exists():
        return JsonResponse({'sales_trends': []}, safe=False)

    if interval == 'weekly':
        sales_data = sales.annotate(week=TruncWeek('date')).values('week').annotate(revenue=Sum('total_price')).order_by('week')
        trends = [{'date': sale['week'].strftime('%Y-%m-%d'), 'revenue': float(sale['revenue'])} for sale in sales_data]
    else: 
        sales_data = sales.annotate(day=TruncDay('date')).values('day').annotate(revenue=Sum('total_price')).order_by('day')
        trends = [{'date': sale['day'].strftime('%Y-%m-%d'), 'revenue': float(sale['revenue'])} for sale in sales_data]

    return JsonResponse({'sales_trends': trends}, safe=False)




def sales_records(request):
    expenses = Expense.objects.filter(owner=request.user).order_by("-date")
    categories = Category.objects.all()

    # **Filtering Logic**
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    category_id = request.GET.get("category")
    search_query = request.GET.get("search")

    if start_date and end_date:
        expenses = expenses.filter(date__range=[start_date, end_date])

    if category_id:
        try:
            category_id = int(category_id)
            expenses = expenses.filter(category_id=category_id)
        except ValueError:
            pass  # Ignore if conversion fails

    if search_query:
        expenses = expenses.filter(
            Q(product_name__icontains=search_query) |
            Q(customer_name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    # **Pagination**
    paginator = Paginator(expenses, 10)  # Show 10 records per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "expenses": page_obj,  # Use paginated results
        "categories": categories,
        "start_date": start_date,
        "end_date": end_date,
        "selected_category": category_id,
        "search_query": search_query,
    }
    return render(request, "sales/sales_records.html", context)


@login_required(login_url='/authentication/login')
def stats_view(request):
    return render(request, 'expenses/stats.html')

def new_view(request):
    return render(request, 'expenses/new.html')