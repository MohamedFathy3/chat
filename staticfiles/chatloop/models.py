from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify 
from django.utils.translation import gettext_lazy as _  # لاستخدام الترجمة متعددة اللغات
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save




class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer", verbose_name="المستخدم")
    is_admin = models.BooleanField(default=False, verbose_name="مسؤول")
    is_hidden = models.BooleanField(default=False, verbose_name="عضو مخفي")
    is_ghost = models.BooleanField(default=False, verbose_name="عضو شبح")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, default='static/images/log.png', verbose_name="الصورة الشخصية")
    notification_enabled = models.BooleanField(default=True, verbose_name="تفعيل الإشعارات")
    join_date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الانضمام")
    last_login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="عنوان IP الأخير")

    def clean(self):
        # تأكد من أنه يمكن تحديد حالة واحدة فقط لكل مستخدم
        if sum([self.is_admin, self.is_hidden, self.is_ghost]) > 1:
            raise ValidationError("لا يمكن للمستخدم أن يكون أكثر من حالة في نفس الوقت (مسؤول، مخفي، أو شبح).")

    def __str__(self):
        return f"{self.user.username}"

@receiver(post_save, sender=Customer)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # إذا تم إنشاء مستخدم جديد من نوع Customer، نقوم بإنشاء UserProfile له
        UserProfile.objects.create(user=instance)




class BlockedBrowser(models.Model):
    # قائمة المتصفحات المتاحة
    BROWSER_CHOICES = [
        ('chrome', 'Chrome'),
        ('firefox', 'Firefox'),
        ('safari', 'Safari'),
        ('edge', 'Edge'),
        ('opera', 'Opera'),
        ('internet_explorer', 'Internet Explorer'),
    ]
    
    # الحقل لاختيار المتصفح
    browser_name = models.CharField(
        max_length=100, 
        choices=BROWSER_CHOICES,  # تحديد الخيارات من القائمة
        verbose_name="اسم المتصفح المحظور"
    )
    
    blocked_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الحظر")

    def __str__(self):
        return self.browser_name

    class Meta:
        verbose_name = "متصفح محظور"
        verbose_name_plural = "المتصفحات المحظورة"




def create_user_profile_for_customer(customer):
    UserProfile.objects.create(user=customer)


class UserProfile(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE, verbose_name="عضو")
    can_see_hidden = models.BooleanField(default=False, verbose_name="من يمكنه رؤية العضو  المخفي")  # هل يمكنه رؤية المخفيين؟
    can_see_ghost = models.BooleanField(default=False, verbose_name="من ممكن ان يرا العضو الشبح")  # هل يمكنه رؤية الشبح؟
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, default='images/log.png', verbose_name="الصورة الشخصية")
    bio = models.TextField(blank=True, null=True, verbose_name="السيرة الذاتية")
    
    def __str__(self):
        return f"Profile for {self.user.user.username}"
    
    class Meta:
        verbose_name = "صلاحيه الاعضاء"
        verbose_name_plural = "صلاحية الاعضاء"


    def can_see(self, other_Customer):
        """
        دالة للتحقق إذا كان المستخدم يمكنه رؤية الآخر بناءً على صلاحياته
        """
        if self.is_hidden and not self.can_see_hidden:
            return False  # إذا كان الآخر مخفيًا ولم يُسمح له برؤيته
        if self.is_ghost and not self.can_see_ghost:
            return False  # إذا كان الآخر شبحًا ولم يُسمح له برؤيته
        return True  # يمكنه رؤية المستخدم الآخر
        



class Guest(models.Model):
    name = models.CharField(max_length=44, verbose_name="اسم الزائر")
    session_id = models.CharField(max_length=255, unique=True, verbose_name="معرف الجلسة")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, default='images/log.png', verbose_name="الصورة الشخصية")
    join_date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الانضمام")
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='guests', verbose_name="الغرفة")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "زائر"
        verbose_name_plural = "الزوار"

class ProfileLike(models.Model):
    user = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, null=True, blank=True, on_delete=models.CASCADE)
    liked_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإعجاب")

    def __str__(self):
        return f"{self.user.user.username} liked profile of {self.liked_profile.user.user.username}"

    class Meta:
        verbose_name = "إعجاب بالملف الشخصي"
        verbose_name_plural = "إعجابات الملفات الشخصية"
        unique_together = ('user', 'liked_profile')




class Room(models.Model):
    name = models.CharField(max_length=100, default="غرفة الدردشة", verbose_name="اسم الغرفة")
    image = models.ImageField(upload_to="chat_images/", blank=True, null=True, verbose_name="صورة مرفقة")
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    customers = models.ManyToManyField(Customer, related_name="rooms", verbose_name="المستخدمين")  # إضافة المستخدمين الذين يشاركون في الغرفة
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="رابط الغرفة")  # حقل slug

    def save(self, *args, **kwargs):
        # إذا لم يكن الـ slug فارغًا، نقوم بتوليده بناءً على اسم الغرفة
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)  # حفظ الكائن

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "غرفة"
        verbose_name_plural = "الغرف"



class Emoji(models.Model):
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    

class DecorativeText(models.Model):
    content = models.TextField(verbose_name="النص المزخرف")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    
    def __str__(self):
        return self.content 


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages", verbose_name="الغرفة")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, verbose_name="المستخدم")
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, null=True, blank=True, verbose_name="الزائر")
    content = models.TextField(blank=True, null=True, verbose_name="محتوى الرسالة")
    image = models.ImageField(upload_to="chat_images/", blank=True, null=True, verbose_name="صورة مرفقة")
    emoji = models.ForeignKey(Emoji,  on_delete=models.SET_NULL ,blank=True, null=True, verbose_name="رمز تعبيري")
    text = models.ForeignKey(DecorativeText,  on_delete=models.SET_NULL ,blank=True, null=True, verbose_name="نص مزخرف")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإرسال")

    def __str__(self):
        return f"{self.customer or self.guest} "

    class Meta:
        verbose_name = "رسالة"
        verbose_name_plural = "الرسائل"


class Like(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="likes", verbose_name="المستخدم")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="likes", verbose_name="الرسالة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإعجاب")

    def __str__(self):
        return f"{self.user.user.username} liked message {self.message.id}"

    class Meta:
        verbose_name = "إعجاب"
        verbose_name_plural = "الإعجابات"
        unique_together = ('user', 'message')  # منع إعجاب نفس المستخدم بنفس الرسالة أكثر من مرة



class Notification(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="notifications", verbose_name="المستخدم")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="notifications", verbose_name="الغرفة")
    message = models.TextField(verbose_name="محتوى الإشعار")
    like = models.ForeignKey(Like, null=True, blank=True, on_delete=models.CASCADE, related_name="notifications", verbose_name="الإعجاب")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإشعار")
    is_read = models.BooleanField(default=False, verbose_name="تمت قراءته؟")
    seen = models.BooleanField(default=False)  # إضافة حقل "مشاهدة" جديد

    def __str__(self):
        return f"إشعار لـ {self.customer.user.username} في {self.room.name}"

    class Meta:
        verbose_name = "إشعار"
        verbose_name_plural = "الإشعارات"


class Ban(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, verbose_name="المستخدم المحظور")
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, null=True, blank=True, verbose_name="الزائر المحظور")
    reason = models.TextField(blank=True, null=True, verbose_name="سبب الحظر")
    banned_by = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bans", verbose_name="تم الحظر بواسطة")
    banned_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الحظر")
    is_banned = models.BooleanField(default=True, verbose_name="محظور")  # هذا الحقل
    unban_at = models.DateTimeField(null=True, blank=True, verbose_name="تاريخ الإلغاء")

    def clean(self):
        if not self.customer and not self.guest:
            raise ValidationError('Either a customer or a guest must be banned.')
        if self.customer and self.guest:
            raise ValidationError('Only one of customer or guest can be banned.')

    def __str__(self):
        return f"محظور: {self.customer or self.guest}"

    class Meta:
        verbose_name = "حظر"
        verbose_name_plural = "الحظرات"


class Shildimages(models.Model):
    images = models.ImageField(upload_to="avatars/", verbose_name="الصور")

    def __str__(self):
        return self.images.url if self.images else "لا توجد صورة"

    class Meta:
        verbose_name = "صورة الدرع"
        verbose_name_plural = "صور الدروع"


class Shield(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="shields", verbose_name="المستخدم")
    name = models.CharField(max_length=50, verbose_name="اسم الدرع", null=True, blank=True)
    Shield = models.ForeignKey(Shildimages, on_delete=models.CASCADE, verbose_name="صورة الدرع")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    def __str__(self):
        return f"درع: {self.name} لـ {self.customer.user.username}"

    class Meta:
        verbose_name = "درع"
        verbose_name_plural = "الدروع"


class Style(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="style", verbose_name="المستخدم")
    font_family = models.CharField(max_length=50, default="Arial", verbose_name="نوع الخط")
    font_size = models.IntegerField(default=14, verbose_name="حجم الخط")
    font_color = models.CharField(max_length=7, default="#000000", verbose_name="لون الخط")
    background_color = models.CharField(max_length=7, default="#FFFFFF", verbose_name="لون الخلفية")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, default='images/log.png', verbose_name="الصورة الشخصية")

    def __str__(self):
        return f"الأنماط لـ {self.customer.user.username}"

    class Meta:
        verbose_name = "نمط"
        verbose_name_plural = "الأنماط"


class DirectMessage(models.Model):
    guest_sender = models.ForeignKey(Guest, null=True, blank=True, on_delete=models.SET_NULL, related_name='sent_messages')
    sender = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE, related_name="sent_messages", verbose_name=_("المرسل"))
    receiver = models.ForeignKey(Customer, null=False, on_delete=models.CASCADE, related_name="received_messages", verbose_name=_("المستقبل"))
    content = models.TextField(verbose_name=_("محتوى الرسالة"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاريخ الإرسال"))
    is_read = models.BooleanField(default=False, verbose_name=_("تم قراءتها؟"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("تم حذفها؟"))

  
    def mark_as_read(self):
        """ لتغيير حالة الرسالة إلى تم قراءتها """
        self.is_read = True
        self.save()

    def mark_as_unread(self):
        """ لتغيير حالة الرسالة إلى غير مقروءة """
        self.is_read = False
        self.save()

    class Meta:
        verbose_name = _("رسالة مباشرة")
        verbose_name_plural = _("الرسائل المباشرة")
        ordering = ['created_at']



class PrivateMessageNotification(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # الشخص الذي سيتلقى الإشعار
    message = models.ForeignKey(DirectMessage, on_delete=models.CASCADE)  # الرسالة التي تتعلق بالإشعار
    is_read = models.BooleanField(default=False)  # حالة قراءة الإشعار
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ إرسال الإشعار

    def __str__(self):
       return self.customer.user.username
