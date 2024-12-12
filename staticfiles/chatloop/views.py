from django.shortcuts import render
from django.contrib.auth.hashers import make_password
import os
import uuid
from django.http import Http404
from django.http import JsonResponse
from datetime import datetime  # إضافة الاستيراد هنا
from django.contrib.sessions.models import Session
from django.shortcuts import render ,get_object_or_404, redirect
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib import messages
from chatloop.forms import UserRegistrationForm, GuestForm, MessageForm, StyleForm, CustomerProfileForm
from chatloop.models import DecorativeText, Room, Guest, Customer, Message, Emoji, Style, DirectMessage,Like, UserProfile, ProfileLike,Notification, PrivateMessageNotification
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # تعديل حسب اسم صفحة تسجيل الدخول لديك
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def ConectUs(request):
    return render(request,'conect.html')

def viwer(request):
    return render(request,'viwes.html')

def chat(request):
    return render(request,'chat.html')

def chatkhaleg(request):
    return render(request,'chatkhaleg.html')
    


def dashboard(request):
    return render(request, 'dashborad/index.html')


# عرض قائمة الغرف
def home(request):
    rooms = Room.objects.all()  # جلب كل الغرف
    counts = rooms.count()  # حساب عدد الغرف
    return render(request, 'home.html', {'rooms': rooms, 'count': counts})

# عرض تفاصيل الغرفة
def room_detail(request, slug):
    room = get_object_or_404(Room, slug=slug)  # جلب الغرفة باستخدام الـ slug
    return render(request, 'chatloop.html', {'room': room})

# صفحة اختيار الدخول كعضو أو زائر
def room_enter(request, slug):
    room = get_object_or_404(Room, slug=slug) 
    rooms=Room.objects.all() # جلب الغرفة باستخدام الـ slug
    customr= Customer.objects.all()
    return render(request, 'chatkhaleg.html', {'room': room,'rooms':rooms, 'custom':customr})




def guest_login(request, slug):
    room = get_object_or_404(Room, slug=slug)

    # إذا كان المستخدم مسجلًا، نقوم بتسجيله كزائر
    if request.user.is_authenticated:
        # تسجيل الخروج من الحساب الحالي
        logout(request)

    # إذا كانت الطريقة هي POST (الزائر قام بإرسال الاسم)
    if request.method == 'POST':
        guest_name = request.POST.get('guest_name')

        # إذا تم توفير الاسم، قم بإنشاء جلسة للزائر
        if guest_name:
            # إذا كان الـ session_key غير موجود، نساعد في إنشائه
            if not request.session.session_key:
                request.session.create()  # إنشاء session_key

            # إنشاء ضيف جديد
            guest = Guest.objects.create(
                name=guest_name,  # الاسم الذي أرسله الزائر
                session_id=request.session.session_key,
                room=room
            )

            # تخزين معلومات الزائر في الجلسة
            request.session['guest_id'] = guest.id

            # التوجيه إلى صفحة الشات
            return redirect('chatloop', slug=slug)

    # إذا كانت الطريقة هي GET (الزائر لم يملأ الاسم بعد)
    return render(request, 'guest_login.html', {'room': room})



def user_login(request, slug):
    room = get_object_or_404(Room, slug=slug)  # جلب الغرفة بناءً على slug

    # إذا كان المستخدم مسجلًا مسبقًا
    if request.user.is_authenticated:
        # جلب العميل المرتبط بالمستخدم
        customer, created = Customer.objects.get_or_create(user=request.user)

        # إضافة العميل إلى الغرفة إذا لم يكن جزءًا منها
        if not room.customers.filter(id=customer.id).exists():
            room.customers.add(customer)
        
        if created:
            messages.success(request, 'تم إضافتك إلى الغرفة بنجاح!')
        
        return redirect('chatloop', slug=slug)

    else:
        # إذا كان المستخدم غير مسجل دخول، نعرض نموذج الدخول
        form = AuthenticationForm(request)
        
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)

                # بعد تسجيل الدخول، إضافة المستخدم إلى الغرفة
                customer, created = Customer.objects.get_or_create(user=user)

                if not room.customers.filter(id=customer.id).exists():
                    room.customers.add(customer)
                    messages.success(request, 'تم إضافتك إلى الغرفة بنجاح!')

                # إذا كان يوجد رابط next في الطلب، إعادة توجيه المستخدم إليه
                next_page = request.GET.get('next', None)  # إذا لم يكن هناك next، سيعيد توجيه إلى الغرفة
                if next_page:
                    return redirect(next_page)  # توجيه إلى الصفحة المحددة
                else:
                    return redirect('chatloop', slug=slug)  # توجيه إلى صفحة الغرفة الرئيسية

        return render(request, 'user_login.html', {'form': form, 'room': room})



def chatloop(request, slug):
    room = get_object_or_404(Room, slug=slug)
    text=DecorativeText.objects.all()

    emojis = Emoji.objects.all()  # جلب جميع الرموز التعبيرية
    style = None
    can_see_hidden = False  # الافتراضي أن المستخدم لا يستطيع رؤية الأعضاء المخفيين
    can_see_ghost = False  # الافتراضي أن المستخدم لا يستطيع رؤية الأعضاء الشبح
    customer = None
    guest = None
    visible_members = []

    # تحقق إذا كان المستخدم مسجلًا
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            style = Style.objects.get(customer=customer)
        except Style.DoesNotExist:
            pass

        # جلب بيانات المستخدم
        user_profile = UserProfile.objects.get(user=request.user.customer)  # تأكد من استخدام customer هنا
        can_see_hidden = user_profile.can_see_hidden
        can_see_ghost = user_profile.can_see_ghost

        # طباعة الأعضاء في الغرفة بدون تصفية الصلاحيات
        all_members = room.customers.all()  # عرض جميع الأعضاء في الغرفة
        print("All members in the room:", all_members)

        # إضافة طباعة تفصيلية لكل عضو لفحص صلاحياته
        for member in all_members:
            print(f"Member: {member.user.username}, is_ghost: {member.is_ghost}, is_hidden: {member.is_hidden}, is_admin: {member.is_admin}")

        # إذا كان المستخدم مشرفًا، نعرض جميع الأعضاء في الغرفة
        if request.user.is_superuser:
            visible_members = all_members  # عرض جميع الأعضاء
        else:
            # تصفية الأعضاء بناءً على صلاحيات الرؤية
            visible_members = all_members.filter(
                Q(is_ghost=False, is_hidden=False) |  # الأعضاء العاديين
                Q(is_ghost=True, userprofile__can_see_ghost=True) |  # الأشباح مع صلاحية رؤية الأشباح
                Q(is_hidden=True, userprofile__can_see_hidden=True)  # الأعضاء المخفيين مع صلاحية رؤية المخفيين
            )

            # تصفية المسؤولين بحيث يظهرون فقط لبعضهم البعض
            if not request.user.is_superuser:  # إذا لم يكن المستخدم مشرفًا
                visible_members = visible_members.exclude(is_admin=True)  # لا يظهر المسؤولون للمستخدمين العاديين

    # تحقق إذا كان المستخدم زائرًا
    else:
        guest = None
        if request.session.get('guest_id'):
            try:
                guest = Guest.objects.get(id=request.session['guest_id'])
            except Guest.DoesNotExist:
                del request.session['guest_id']  # حذف guest_id من الجلسة
                guest = None
                messages.error(request, 'تم طرد الزائر من الغرفة، لم يعد موجودًا.')  # عرض رسالة خطأ
                return redirect('home')  # إعادة التوجيه إلى الصفحة الرئيسية

        # عرض الأعضاء العاديين فقط للزائر
        all_members = room.customers.all()  # عرض جميع الأعضاء في الغرفة
        visible_members = all_members.filter(is_ghost=False, is_hidden=False, is_admin=False)  # تصفية الأعضاء العاديين فقط (بدون أشباح أو مخفيين)

    # طباعة الأعضاء الذين سيتم عرضهم
    print("Visible members:", visible_members)

    # جلب جميع الرسائل الخاصة بالغرفة مرتبة
    messages_list = Message.objects.filter(room=room).order_by('-created_at')[:10]
    
    # إضافة رسالة جديدة
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        emoji_id = request.POST.get('emoji', '')
        text_id = request.POST.get('text', '')
        
        
        text=None

        emoji = None
        if emoji_id:
            emoji = Emoji.objects.get(id=emoji_id)
        if text_id:
            text = DecorativeText.objects.get(id=text_id)
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            message = Message.objects.create(
                room=room,
                customer=customer,
                content=content,
                image=image,
                emoji=emoji,
                text=text
            )
        elif guest:
            message = Message.objects.create(
                room=room,
                guest=guest,
                content=content,
                image=image,
                emoji=emoji,
                text=text
            )

        return redirect('chatloop', slug=slug)

    # جلب الأعضاء والزوار في الغرفة
    guests = room.guests.all()
    
    # تحقق إذا كان المستخدم قد تم طرده
    if customer and customer not in room.customers.all():
        messages.error(request, 'تم طردك من الغرفة.')  # عرض رسالة أنه تم طرده
        return redirect('home')  # إعادة توجيه العميل إلى الصفحة الرئيسية بعد الطرد

    return render(request, 'chatloop.html', {
        'room': room, 
        'members': visible_members, 
        'guests': guests,
        'guest': guest, 
        'customer': customer,
        'messages': messages_list,
        'emojis': emojis,
        'style': style,
        'can_see_hidden': can_see_hidden,
        'can_see_ghost': can_see_ghost,
        'customer': customer,
        'emojis': emojis,
        'text':text,  # تم إرسال الرموز التعبيرية إلى القالب

    })



   

@login_required
def remove_guest_from_room(request, slug, guest_id):
    # جلب الغرفة باستخدام `slug`
    room = get_object_or_404(Room, slug=slug)
    
    # جلب الزائر باستخدام `guest_id`
    guest = get_object_or_404(Guest, id=guest_id)
    
    # التأكد إذا كان المستخدم هو سوبر
    if request.user.is_superuser:
        # التحقق إذا كان الزائر ينتمي للغرفة
        if guest.room == room:
            guest.delete()  # حذف الزائر من الغرفة
            # يمكن إضافة رسالة أو أي ردود فعل أخرى بعد الطرد
        else:
            # الزائر غير موجود في الغرفة
            pass

        return redirect('chatloop', slug=slug)

    # إذا لم يكن سوبر، اعادة توجيه إلى الصفحة نفسها بدون تغيير
    return redirect('chatloop', slug=slug)

@login_required
def remove_member_from_room(request, slug, member_id):
    room = get_object_or_404(Room, slug=slug)
    member = get_object_or_404(Customer, id=member_id)

    # التأكد إذا كان المستخدم هو سوبر
    if request.user.is_superuser:
        # إزالة العضو من الغرفة
        room.customers.remove(member)
        # يمكن إضافة رسالة أو أي ردود فعل أخرى بعد الطرد
        # على سبيل المثال، إرسال رسالة تفيد بأنه تم طرد العضو بنجاح
        return redirect('chatloop', slug=slug)

    # إذا لم يكن سوبر، اعادة توجيه إلى الصفحة نفسها بدون تغيير
    return redirect('chatloop', slug=slug)



def load_new_messages(request, slug):
    room = get_object_or_404(Room, slug=slug)

    # جلب الرسائل الجديدة فقط
    messages = Message.objects.filter(room=room).order_by('-created_at')[:10]  # جلب أحدث 10 رسائل

    # تحضير الرسائل لعرضها في الـ JSON
    messages_data = []
    for message in messages:
        message_data = {
            'content': message.content,
            'sender': message.customer.user.username if message.customer else message.guest.name,
            'is_customer': True if message.customer else False,
            'image': message.image.url if message.image else None,
            'emoji': message.emoji,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        messages_data.append(message_data)

    return JsonResponse({'messages': messages_data})


def load_messages(request, slug):
    room = get_object_or_404(Room, slug=slug)
    messages = Message.objects.filter(room=room).order_by('-created_at')[:10]

    # إنشاء قائمة للرسائل
    messages_data = []
    for message in messages:
        messages_data.append({
            'sender': message.customer.user.username if message.customer else message.guest.name,
            'content': message.content,
            'image': message.image.url if message.image else None,
            'emoji': message.emoji.symbol if message.emoji else None,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_customer': bool(message.customer),
        })

    return JsonResponse({'messages': messages_data})




# الخروج من الغرفة للزوار
def guest_logout(request, slug):
    if request.session.get('guest_id'):
        guest = Guest.objects.get(id=request.session['guest_id'])
        room = guest.room
        guest.delete()  # حذف الزائر عند الخروج
        del request.session['guest_id']  # إزالة بيانات الجلسة الخاصة بالزائر
        return redirect('home')  # العودة إلى الصفحة الرئيسية


# الخروج من الغرفة للأعضاء
@login_required
def user_logout(request, slug):
    room = get_object_or_404(Room, slug=slug)
    customer = Customer.objects.get(user=request.user)
    room.customers.remove(customer)  # إزالة العضو من الغرفة
    return redirect('home')



def edit_style(request):
    customer = request.user.customer  # الحصول على العميل المرتبط بالمستخدم الحالي
    
    # محاولة جلب النمط الحالي للمستخدم أو إنشاء جديد إذا لم يكن موجودًا
    try:
        style = Style.objects.get(customer=customer)  # جلب النمط الحالي
    except Style.DoesNotExist:
        style = None  # إذا لم يكن هناك نمط، سيتم إنشاء واحد جديد

    if request.method == 'POST':
        form = StyleForm(request.POST, request.FILES, instance=style)  # تمرير النمط الحالي إذا كان موجودًا

        if form.is_valid():
            # حفظ النموذج مع التأكد من ربطه بالعميل
            style = form.save(commit=False)
            style.customer = customer  # ربط النمط بالمستخدم الحالي
            style.save()  # حفظ التغييرات
            # بعد الحفظ، إعادة التوجيه إلى صفحة الدردشة
            room_slug = request.GET.get('room_slug', '')  # جلب `slug` الغرفة من الـ URL
            if room_slug:
                return redirect('chatloop', slug=room_slug)  # إعادة التوجيه إلى صفحة الدردشة
            return redirect('home')  # إذا لم يكن هناك غرفة معينة، يتم توجيه المستخدم إلى الصفحة الرئيسية
    else:
        form = StyleForm(instance=style)  # تمرير النمط الحالي للنموذج

    return render(request, 'edit_style.html', {'form': form})



def edit_profile(request):
    try:
        customer = request.user.customer  # الحصول على العميل المرتبط بالمستخدم الحالي
    except Customer.DoesNotExist:
        raise Http404("Customer does not exist")

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=customer)

        if form.is_valid():
            # التأكد من ربط العميل بـ user
            customer = form.save(commit=False)
            customer.user = request.user  # ربط العميل بالمستخدم الحالي
            customer.save()  # حفظ التغييرات
            # بعد الحفظ، إعادة التوجيه إلى صفحة الدردشة
            room_slug = request.GET.get('room_slug', '')  # جلب `slug` الغرفة من الـ URL
            if room_slug:
                return redirect('chatloop', slug=room_slug)  # إعادة التوجيه إلى صفحة الدردشة
            return redirect('home')  # إذا لم يكن هناك غرفة معينة، يتم توجيه المستخدم إلى الصفحة الرئيسية
    else:
        form = CustomerProfileForm(instance=customer)

    return render(request, 'edit_profile.html', {'form': form})


# إزالة @login_required من هنا إذا كنت لا ترغب في فرض تسجيل الدخول
@login_required()
def send_message(request, user_id):
    # التأكد من وجود الـ Customer باستخدام user_id
    customer = request.user.customer  # استخدم customer من user

    # التأكد من أن الـ Customer لديه UserProfile
    try:
        liked_profile = UserProfile.objects.get(user__id=user_id)
    except UserProfile.DoesNotExist:
        return redirect('home')  # إعادة التوجيه إذا لم يكن يوجد UserProfile

    if request.method == "POST":
        content = request.POST.get("content")

        # إرسال الرسالة
        if request.user.is_authenticated:
            sender = request.user.customer  # استخدم customer بدلاً من أي شيء آخر
            # إرسال الرسالة
            DirectMessage.objects.create(
                sender=sender,
                receiver=liked_profile.user,  # استخدام الـ user المرتبط بـ UserProfile
                content=content,
            )
        else:
            # إذا كان الزائر
            guest = Guest.objects.filter(session_id=request.session.session_key).first()
            if guest:
                DirectMessage.objects.create(
                    guest_sender=guest,  # استخدم guest_sender بدلاً من guest
                    receiver=liked_profile.user,
                    content=content,
                )

        # إعادة توجيه المستخدم إلى صفحة الملف الشخصي للمستقبل
        return redirect('user_profile', user_id=user_id)

    return render(request, 'messages/send_message.html', {
        'liked_profile': liked_profile  # تمرير الملف الشخصي للمستخدم
    })




def user_profile(request, user_id):
    # التأكد من أن المستخدم مسجل وتحديد العميل المرتبط به
    if request.user.is_authenticated:
        customer = request.user.customer  # هذا يعني أن المستخدم مسجل ولديه Customer مرتبط به
    else:
        customer = None  # إذا كان المستخدم غير مسجل

    # الحصول على الملف الشخصي للمستخدم المعين باستخدام الـ customer بدلاً من user
    try:
        # البحث عن الملف الشخصي باستخدام معرف الـ Customer
        liked_profile = UserProfile.objects.get(user__id=user_id)  # المستخدم من نوع Customer
    except UserProfile.DoesNotExist:
        return redirect('home')  # إذا لم يتم العثور على الـ UserProfile

    # جلب الرسائل بين المستخدم الحالي والمستخدم المعين
    if customer:  # إذا كان المستخدم مسجلًا
        direct_messages = DirectMessage.objects.filter(
            sender=customer, receiver=liked_profile.user
        ) | DirectMessage.objects.filter(
            sender=liked_profile.user, receiver=customer
        )
        direct_messages = direct_messages.order_by('-created_at')

        # جلب الإشعارات الخاصة بالمستخدم
        notifications = PrivateMessageNotification.objects.filter(customer=request.user.customer, is_read=False)
    else:
        direct_messages = []  # إذا كان المستخدم غير مسجل
        notifications = []

    if request.method == 'POST' and 'like_profile' in request.POST:
        if customer:  # إذا كان المستخدم مسجلًا
            like_exists = ProfileLike.objects.filter(user=customer, liked_profile=liked_profile).exists()
            if like_exists:
                ProfileLike.objects.filter(user=customer, liked_profile=liked_profile).delete()
            else:
                ProfileLike.objects.create(user=customer, liked_profile=liked_profile)
                # إضافة إشعار عند الإعجاب
                direct_message = DirectMessage.objects.create(
                    sender=customer,
                    receiver=liked_profile.user,
                    content=f'{customer.user.username} أعجب بملفك الشخصي!'
                )
                PrivateMessageNotification.objects.create(
                    message=direct_message,  # استخدم الـ DirectMessage هنا
                    customer=liked_profile.user,  # إشعار للمستخدم
                    is_read=False
                )
        else:  # إذا كان المستخدم زائرًا
            guest = Guest.objects.filter(session_id=request.session.session_key).first()
            if guest:
                like_exists = ProfileLike.objects.filter(guest=guest, liked_profile=liked_profile).exists()
                if like_exists:
                    ProfileLike.objects.filter(guest=guest, liked_profile=liked_profile).delete()
                else:
                    ProfileLike.objects.create(guest=guest, liked_profile=liked_profile)
                    # إضافة إشعار عند الإعجاب من الزائر
                    # إنشاء رسالة تخبر أن الزائر أعجب بالملف الشخصي
                    direct_message = DirectMessage.objects.create(
                        sender=None,  # لا نستخدم sender لأن الزائر ليس لديه Customer
                        receiver=liked_profile.user,
                        content=f'زائر أعجب بملفك الشخصي!'
                    )
                    PrivateMessageNotification.objects.create(
                        message=direct_message,  # استخدم الـ DirectMessage هنا
                        customer=liked_profile.user,  # إشعار للمستخدم
                        is_read=False
                    )

        return redirect('user_profile', user_id=user_id)

    return render(request, 'user_profile.html', {
       'liked_profile': liked_profile,
       'is_liked': ProfileLike.objects.filter(user=customer, liked_profile=liked_profile).exists() if customer else
                   ProfileLike.objects.filter(guest__session_id=request.session.session_key, liked_profile=liked_profile).exists() if request.session.session_key else False,
       'direct_messages': direct_messages,  # إرسال الرسائل الخاصة إلى القالب
       'notifications': notifications,  # إرسال الإشعارات إلى القالب
   })



@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(PrivateMessageNotification, id=notification_id)

    if notification.customer == request.user.customer:
        notification.is_read = True
        notification.save()

    return redirect('user_profile', user_id=request.user.id)

