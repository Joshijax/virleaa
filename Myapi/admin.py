from django.contrib import admin
from .models import Certificate, Course, Course_Uploads, Category, Course_content, payments_verify, section_material
# Register your models here.
admin.site.register(payments_verify)

admin.site.register(Course_Uploads)



class CourseAdmin(admin.ModelAdmin):

    list_display = ['pk','Course_name']
    list_filter = ('publish', 'created_date',)
    search_fields = ('Course_name', 'description',)
    prepopulated_fields = {'slug': ('Course_name',)}
    date_hierarchy = 'created_date'
    
    
admin.site.register(Course, CourseAdmin)

admin.site.register(Certificate)

admin.site.register(section_material)


admin.site.register(Category)

admin.site.register(Course_content)
