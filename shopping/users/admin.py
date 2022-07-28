from pyexpat.errors import messages
from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline # tabularinline for generic relationship
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html, urlencode
from django.urls import reverse

from shopping.booking import models
from shopping.users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<20', 'Low'),
            ('>=20', 'OK')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<20':
           return queryset.filter(total_product__lt = 20)
        elif self.value() == '>=20':
            return queryset.filter(total_product__gte = 20)

        # return super().queryset(request, queryset)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug' : ['name']
    }
    actions = ['clear_inventory']
    list_display = ['name', 'price', 'total_product', 'inventory_status'] 
    search_fields = ['name']
    list_filter = ['name', 'create_date', InventoryFilter]

    @admin.display(ordering = 'total_product')
    def inventory_status(self, product):
        if product.total_product < 20:
            return 'Low'
        return 'OK'
    
    def clear_inventory(self, request, queryset):
        updated_inventory = queryset.update(total_product = 0)
        self.message_user(
            request,
            f'{updated_inventory} products were successfully deleted',
        )


@admin.register(models.Address)
class Addressdmin(admin.ModelAdmin):
    list_display = ['full_address', 'customer_name']
    ordering = ['address']
    list_select_related = ['customer']

    def full_address(self,address):
        return address.address + ', ' + f'{address.postcode}' + ' ' + address.city + ', ' + address.state #can use str() for converting to string

    @admin.display(ordering = 'customer')
    def customer_name(self,address):
        return address.customer.user.username


@admin.register(models.OrderItem)
class OrderItemdmin(admin.ModelAdmin):
    #autocomplete_fields = ['product_id','order_status']
    list_display = ['product_name', 'quantity', 'customer_name', 'order_status']
    ordering = ['product_id']
    list_select_related = ['customer_id','product_id']
    search_fields = ['product_id__name__istartswith', 'customer_id__user__username__istartswith']
 

    def product_name(self,order):
        return order.product_id.name
    
    def customer_name(self,order):
        urls = (
            reverse('admin:booking_customer_changelist')
            + '?'
            +urlencode({
                'id': str(order.customer_id.id)
            })
            )
        return format_html('<a href = {} >{}</a>',urls,order.customer_id.user.username)
        #return order.customer_id.name

    #overiding base queryset
    # def get_queryset(self, request:):
    #     return super().get_queryset(request)

#class OrderInline(admin.TabularInline):
# admin.site.register(models.Product)
admin.site.register(models.Customer)

