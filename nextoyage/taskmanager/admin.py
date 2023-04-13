from django.contrib import admin

# Register your models here.

from .models import Tache, SessionMenage


class SessionInline(admin.TabularInline):
    model = SessionMenage
    extra = 1


class TacheAdmin(admin.ModelAdmin):
    model = Tache
    ordering = ['tache_text']
    inlines = [SessionInline]

    list_display = ('tache_text', 'frequence_int', 'duration')
    # class QuestionAdmin(admin.ModelAdmin):


admin.site.register(Tache, TacheAdmin)
admin.site.register(SessionMenage)

# admin.site.register(Choice)
# Register your models here.
