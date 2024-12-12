from django.contrib import admin
from .models import Shield, Style, Ban, Notification, Message, Room, Guest, Customer ,Shildimages, UserProfile, BlockedBrowser, Emoji, ProfileLike, PrivateMessageNotification, DecorativeText
from django.core.exceptions import ValidationError

admin.site.site_header = "dashboard"




# Register your models here.


admin.site.register(ProfileLike)
admin.site.register(UserProfile)
admin.site.register(PrivateMessageNotification)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_admin', 'is_hidden', 'is_ghost', 'join_date', 'last_login_ip')
    list_filter = ('is_admin', 'is_hidden', 'is_ghost')
    search_fields = ('user__username',)

    def save_model(self, request, obj, form, change):
        # تأكد من أنه لا يمكن تحديد أكثر من حالة واحدة في نفس الوقت في واجهة الإدارة
        if sum([obj.is_admin, obj.is_hidden, obj.is_ghost]) > 1:
            raise ValidationError("لا يمكن للمستخدم أن يكون أكثر من حالة في نفس الوقت (مسؤول، مخفي، أو شبح).")
        super().save_model(request, obj, form, change)

admin.site.register(Customer, CustomerAdmin)


# تسجيل الضيوف في لوحة الإدارة
@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'session_id', 'join_date')
    search_fields = ('name', 'session_id')
    ordering = ('-join_date',)


class DecorativeTextAdmin(admin.ModelAdmin):
    
    list_display = ('content', 'created_at')
    search_fields = ('content',)

admin.site.register(DecorativeText, DecorativeTextAdmin)



# تسجيل الغرف في لوحة الإدارة
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)




admin.site.register(Emoji)



# تسجيل الرسائل في لوحة الإدارة
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'customer', 'guest', 'created_at')
    search_fields = ('content',)
    list_filter = ('room',)
    ordering = ('-created_at',)






# تسجيل الإشعارات في لوحة الإدارة
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'is_read', 'created_at')
    search_fields = ('customer',)
    list_filter = ('is_read',)
    ordering = ('-created_at',)






# تسجيل الحظر في لوحة الإدارة

class BanAdmin(admin.ModelAdmin):
    list_display = ('customer', 'guest', 'reason', 'banned_by', 'banned_at', 'unban_at', 'is_banned')
    search_fields = ('user__username', 'guest__name', 'reason')
    list_filter = ('is_banned', 'banned_by')  # استخدم الحقل هو الآن

    def is_banned(self, obj):
        return obj.is_banned
    is_banned.boolean = True
    is_banned.short_description = 'محظور؟'

admin.site.register(Ban, BanAdmin)





class BlockedBrowserAdmin(admin.ModelAdmin):
    list_display = ('browser_name', 'blocked_at')
    search_fields = ('browser_name',)

admin.site.register(BlockedBrowser, BlockedBrowserAdmin)




# تسجيل الدروع في لوحة الإدارة
@admin.register(Shield)
class ShieldAdmin(admin.ModelAdmin):
    list_display = ('customer', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

# تسجيل الأنماط في لوحة الإدارة
@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('customer', 'font_family', 'font_size', 'font_color', 'background_color')

# تسجيل الصور الخاصة بالدروع في لوحة الإدارة
@admin.register(Shildimages)
class ShildimagesAdmin(admin.ModelAdmin):
    list_display = ('images',)
