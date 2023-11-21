from django.contrib import admin

from user_profile.models import User, Region, Municipality, UserProfile, Service, Province

admin.site.register(User)
admin.site.register(Region)
admin.site.register(Municipality)
admin.site.register(UserProfile)
admin.site.register(Service)
admin.site.register(Province)
# from
# Register your models here.
