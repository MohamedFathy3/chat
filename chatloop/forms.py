from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Customer, Guest, Message, Style

class UserRegistrationForm(UserCreationForm):
   

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        

        # ربط المستخدم بعميل
        Customer.objects.create(user=user)
        return user



class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['name']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'image', 'emoji']



    


    
    
class StyleForm(forms.ModelForm):
    class Meta:
        model = Style
        fields = ['font_family', 'font_size', 'font_color', 'background_color']

        widgets = {
            'font_family': forms.TextInput(attrs={'placeholder': 'أدخل نوع الخط'}),
            'font_size': forms.NumberInput(attrs={'min': '1', 'max': '100'}),
            'font_color': forms.TextInput(attrs={'type': 'color'}),  # حقل اختيار اللون
            'background_color': forms.TextInput(attrs={'type': 'color'}),  # حقل اختيار اللون
        }

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [ 'avatar', 'notification_enabled']
        # لا تضع 'user' في الحقول هنا لأنك ستربطه في الـ views.py

class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="محتوى الرسالة")

# forms.py
class ReplyForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="محتوى الرد")
