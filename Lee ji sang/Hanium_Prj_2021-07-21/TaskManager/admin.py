from django.contrib import admin
# Register your models here.
from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']  #검색기능

admin.site.register(Question, QuestionAdmin)



