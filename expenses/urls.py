from django.urls import path
from . import views
from .views import dashboard_data

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
     # path('', views.new_view, name="new_view"),

    path('expenses', views.index, name="expenses"),
    path('add-expense', views.add_expense, name="add-expenses"),
    path('edit-expense/<int:id>', views.expense_edit, name="expense-edit"),
    path('expense-delete/<int:id>', views.delete_expense, name="expense-delete"),
#     path('search-expenses', csrf_exempt(views.search_expenses),
#          name="search_expenses"),
    path('expense_category_summary', views.expense_category_summary,
         name="expense_category_summary"),
    path('', views.stats_view,
         name="stats"),
     path('new/', views.new_view,
         name="new"),
     path('dashboard/', dashboard_data, name="dashboard-data"),
     path('sales_trends/', views.sales_trends, name="sales_trends"),  # Added trailing slash here


]
