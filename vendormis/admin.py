from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    t_display = ('business_detail', 'approved_by_full_name', "approved_by_organisation","signature", "approval_date")
    search_fields = ('approved_by_full_name',)
    list_filter = ('approval_date',)

@admin.register(PersonalDetail)
class PersonalDetailAdmin(admin.ModelAdmin):
    list_display = ('image', 'first_name', 'surname', 'gender', 'nationality', 'national_id_number')
    search_fields = ('first_name', 'surname', 'national_id_number')
    list_filter = ('gender', 'nationality')



