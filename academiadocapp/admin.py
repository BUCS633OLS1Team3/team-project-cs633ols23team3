from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Requests, Events, Comments, Directory, Profile, Transcripts

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Requests)
admin.site.register(Events)
admin.site.register(Comments)
admin.site.register(Directory)
admin.site.register(Transcripts)


UserAdmin.fieldsets += ('Custom fields set', {'fields': ('bio', 'role', 'profile_pic', 'student_id', 'grad_year')}),
