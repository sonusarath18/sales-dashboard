from django.contrib import admin
from .models import Expense, Category,product_name
# Register your models here.


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'owner', 'category', 'date','customer_name','product_name','total_price','quantity')
    search_fields = ( 'category', 'date',)
    list_per_page = 5


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)
admin.site.register(product_name)

