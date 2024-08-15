from django.contrib import admin
from .models import Hospital,Client,Robot,Operator,Edge,Location,OrderRequest,Patient,Account,PubsubKey
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class AccountAdmin(UserAdmin):


	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('contactNo', 'password1', 'password2'),
		}),
	)

	list_display = ('pk','contactNo','date_joined', 'last_login', 'is_admin','is_staff')
	search_fields = ('pk','contactNo',)
	readonly_fields=('pk','date_joined', 'last_login')
	ordering=('contactNo',)
	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()



admin.site.register(Client)#,ClientAdmin)
admin.site.register(Operator)#,OperatorAdmin)
admin.site.register(Hospital)
admin.site.register(Robot)
admin.site.register(Location)
admin.site.register(OrderRequest)
admin.site.register(Edge)
admin.site.register(Patient)
admin.site.register(Account,AccountAdmin)#,AccountAdmin)
admin.site.register(PubsubKey)
