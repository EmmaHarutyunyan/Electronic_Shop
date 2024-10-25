from django import forms
from .models import Wishlist
from .models import UserInfo, Accessories

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from.models import Pay,UserMessage,Product_images



class AddToWishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['product']




class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
	

class PayForm(forms.ModelForm):
    class Meta:
        model = Pay
        fields = ('name', 'card_number', 'hetevi_tver', 'phone_number', 'email')



class UserMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ('name','phone', 'email', 'address', 'message')
        


class ContactForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['name', 'email', 'phone', 'address']



class ProductImageForm(forms.ModelForm):
    class Meta:
        model = Product_images
        fields = ['product', 'pictures',]


class ProductFilterForm(forms.Form):
    category = forms.CharField(required=False)



class AccessoriesImageForm(forms.ModelForm):
    class Meta:
        model = Product_images
        fields = ['product', 'pictures',]


class AccessoriesFilterForm(forms.Form):
    category = forms.CharField(required=False)


from .models import Product_detail,Color,Size

class ProductDetailAdminForm(forms.ModelForm):
    class Meta:
        model = Product_detail
        fields = '__all__'
        widgets = {
            'color': forms.Select()  
        }

class ProductDetailAdminForm(forms.ModelForm):
    class Meta:
        model = Product_detail
        fields = '__all__'
        widgets = {
            'size': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super(ProductDetailAdminForm, self).__init__(*args, **kwargs)
        if 'product' in self.data:
            try:
                product_id = int(self.data.get('product'))
                self.fields['size'].queryset = Size.objects.filter(product_id=product_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['size'].queryset = Size.objects.filter(product=self.instance.product)

            
class ColorAdminForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = '__all__'
        widgets = {
            'color_code': forms.TextInput(attrs={'type': 'color'}) 
        }




from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'custom-class'})