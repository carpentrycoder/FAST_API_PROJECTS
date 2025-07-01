from django.contrib import admin
from .models import Student

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id','name','age','email','enrolled')
    search_fields = ('name','email')
    list_filter = ('enrolled','age')