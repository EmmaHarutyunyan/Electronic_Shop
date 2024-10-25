from django.shortcuts import render, redirect
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import ProductImageForm
from django.contrib.auth import login, authenticate, logout
from .models import Category, Product, Wishlist,HotDeal,Store, Store_img,Pay,Cart,TopSelling,Product_detail,Product_images,Product_description,Accessories,CookieConsent,Slide,Video,Color,Size
from django.http import JsonResponse
from django.contrib import messages
from.forms import PayForm, AddToWishlistForm, UserMessageForm,NewUserForm,AccessoriesFilterForm,AccessoriesImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import jwt
from jwt.exceptions import PyJWTError
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .forms import ContactForm
from django.http import  JsonResponse
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.views import RedirectURLMixin
from django.core.exceptions import SuspiciousOperation
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.middleware.csrf import get_token as get_csrf_token
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import ListView, View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import CookieGroup
from .util import (
    accept_cookies,
    decline_cookies,
    get_accepted_cookie_groups,
    get_declined_cookie_groups,
    get_not_accepted_or_declined_cookie_groups,
)
import warnings

from django import template
from django.urls import reverse
from django.utils.html import json_script

from .cache import all_cookie_groups as get_all_cookie_groups
from .conf import settings
from .util import (
    are_all_cookies_accepted,
    get_accepted_cookies,
    get_cookie_dict_from_request,
    get_cookie_string,
    get_cookie_value_from_request,
    get_not_accepted_or_declined_cookie_groups,
    is_cookie_consent_enabled,
)

def is_ajax_like(request: HttpRequest) -> bool:
    ajax_header = request.headers.get("X-Requested-With")
    if ajax_header == "XMLHttpRequest":
        return True

    return bool(request.headers.get("X-Cookie-Consent-Fetch"))


class CookieGroupListView(ListView):
    """
    Display all cookies.
    """

    model = CookieGroup


class CookieGroupBaseProcessView(RedirectURLMixin, View):
    def get_success_url(self):
        """
        If user adds a 'next' as URL parameter or hidden input,
        redirect to the value of 'next'. Otherwise, redirect to
        cookie consent group list
        """
        redirect_to = self.request.POST.get("next", self.request.GET.get("next"))
        if redirect_to and not url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        ):
            raise SuspiciousOperation("Unsafe open redirect suspected.")
        return redirect_to or reverse("cookie_consent_cookie_group_list")

    def process(self, request, response, varname):  # pragma: no cover
        raise NotImplementedError()

    def post(self, request, *args, **kwargs):
        varname = kwargs.get("varname", None)
        if is_ajax_like(request):
            response = HttpResponse()
        else:
            response = HttpResponseRedirect(self.get_success_url())
        self.process(request, response, varname)
        return response


class CookieGroupAcceptView(CookieGroupBaseProcessView):
    """
    View to accept CookieGroup.
    """

    def process(self, request, response, varname):
        accept_cookies(request, response, varname)


class CookieGroupDeclineView(CookieGroupBaseProcessView):
    """
    View to decline CookieGroup.
    """

    def process(self, request, response, varname):
        decline_cookies(request, response, varname)

    def delete(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CookieStatusView(View):
    """
    Check the current accept/decline status for cookies.

    The returned accept and decline URLs are specific to this user and include the
    cookie groups that weren't accepted or declined yet.

    Note that this endpoint also returns a CSRF Token to be used by the frontend,
    as baking a CSRFToken into a cached page will not reliably work.
    """

    def get(self, request: HttpRequest) -> JsonResponse:
        accepted = get_accepted_cookie_groups(request)
        declined = get_declined_cookie_groups(request)
        not_accepted_or_declined = get_not_accepted_or_declined_cookie_groups(request)
        # TODO: 
        varnames = ",".join([group.varname for group in not_accepted_or_declined])
        data = {
            "csrftoken": get_csrf_token(request),
            "acceptUrl": reverse("cookie_consent_accept", kwargs={"varname": varnames}),
            "declineUrl": reverse(
                "cookie_consent_decline", kwargs={"varname": varnames}
            ),
            "acceptedCookieGroups": [group.varname for group in accepted],
            "declinedCookieGroups": [group.varname for group in declined],
            "notAcceptedOrDeclinedCookieGroups": [
                group.varname for group in not_accepted_or_declined
            ],
        }
        return JsonResponse(data)


def checkout(request):
    items = request.session.get('cart_items', [])
    total_quantity = sum(item['quantity'] for item in items)
    total_sum = sum(item['quantity'] * item['price'] for item in items)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            user_info = form.save()
            return redirect('index')
    else:
        form = ContactForm()
    context = {
        'form': form,
        'total_quantity': total_quantity,
        'total_sum': total_sum,
        'items': items
    }

    return render(request, 'main/checkout.html', context=context)



def product(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if search_query:
        products = products.filter(pr_name__icontains=search_query)
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'main/product.html', context)
def store(request):
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    brand = request.GET.get('brand', '')
    color_code = request.GET.get('color', '')

    products = Product.objects.all()

    if search_query:
        products = products.filter(pr_name__icontains=search_query)
    
    if category_id:
        products = products.filter(category_id=category_id)

    if brand:
        products = products.filter(brand=brand)

    if color_code:
        try:
            color = Color.objects.get(color_code=color_code)
            products = products.filter(colors=color)
        except Color.DoesNotExist:
            products = products.none()  

    paginator = Paginator(products, 9)
    page = request.GET.get('page', 1)
    products = paginator.get_page(page)

    all_colors = Color.objects.filter(product__in=products)
    unique_colors = {color.color_code: color for color in all_colors}.values()

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'brands': Product.objects.values_list('brand', flat=True).distinct(),
        'colors': unique_colors,
        'search_query': search_query,
        'category_id': category_id,
        'brand': brand,
        'color_code': color_code,
    }

    return render(request, 'main/store.html', context)

def add_to_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login') 
    try:
        product = Product.objects.get(pk=product_id)
    
        
    except Product.DoesNotExist:
        messages.error(request, "Product does not exist.")
        return redirect('index')
    if request.user.is_authenticated:
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product,
        )
        if created:
            messages.success(request, "Product added to wishlist.")
        else:
            messages.info(request, "Product is already in your wishlist.")
    else:
        messages.error(request, "Please log in to add items to your wishlist.")
    return redirect('index')
@login_required
def add_to_cart_from_wishlist(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product does not exist.")
        return redirect('wishlist')
    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, "Quantity updated in cart.")
        else:
            cart_item.quantity = 1
            cart_item.save()
            messages.success(request, "Product added to cart.")
        Wishlist.objects.filter(user=request.user, product=product).delete()
    else:
        messages.error(request, "Please log in to add items to cart.")
    return redirect('wishlist')


@login_required(login_url='login')
def wishlist(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        wishlist_items = []
    context = {
        'categories': categories,
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_items.count(),
    }
    return render(request, 'main/wishlist.html', context)
@login_required
def delete_from_wishlist(request, product_id):
    wishlist_item = get_object_or_404(Wishlist, user=request.user, product_id=product_id)
    if request.method == 'POST':
        wishlist_item.delete()
        messages.success(request, "Item removed from wishlist.")
    return redirect('wishlist')

import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj) 
        return super().default(obj)

def product_detail(request, product_id):
    product = get_object_or_404(Product.objects.select_related('category'), pk=product_id)
    product_details = Product_detail.objects.filter(product=product).select_related('size')
    sizes = Size.objects.filter(product=product)
    colors = Color.objects.filter(product=product)
    pictures = Product_images.objects.filter(product=product)
    description = Product_description.objects.filter(product=product).first()
    
    related_products = []
    other_colors = []

    if product.category.category_name == "Accessories":
        related_products = Product.objects.filter(series=product.series).exclude(id=product.id)
        other_colors = Color.objects.filter(product__in=related_products).distinct()
    else:
        series_products = Product.objects.filter(series=product.series).exclude(id=product.id)
        other_colors = Color.objects.filter(product__in=series_products).distinct()

    context = {
        'product': product,
        'product_details': product_details,
        'sizes': sizes,
        'colors': colors,
        'pictures': pictures,
        'description': description,
        'related_products': related_products,
        'other_colors': other_colors,
    }
    return render(request, 'main/product.html', context)


def color_based_product(request, color_id):
    color = get_object_or_404(Color, id=color_id)
    product = color.product  
    return redirect('product_detail', product_id=product.id)


def update_sizes(request, product_id):
    sizes = Size.objects.filter(product_id=product_id)
    size_data = [{'id': size.id, 'size': str(size)} for size in sizes]
    return JsonResponse({'sizes': size_data})

def all_products(request):

    try:
        accessory_category = Category.objects.get(category_name='Accessories')  
    except Category.DoesNotExist:
        accessory_category = None
    
    if accessory_category:
        products = Product.objects.exclude(category=accessory_category)
    else:
        products = Product.objects.all() 
    
    context = {
        'products': products
    }
    
    return render(request, 'main/all_products.html', context)

def index(request):
    videos = Video.objects.all()
    slide = Slide.objects.all()
    top_selling_products = Product.objects.order_by('-num_sales')[:10]
    
    categories = Category.objects.all()
    
    all_category = {'id': 'all', 'category_name': 'All Products'}
    categories = [all_category] + list(categories)
    
    user_products = get_user_model().objects.all()
    hot_deal = HotDeal.objects.first()
    stores = Store.objects.all()
    products = Product.objects.all()
    pay = Pay.objects.first()
    wishlist_items = Wishlist.objects.all()
    
    if request.user.is_authenticated:
        cart_items = Wishlist.objects.filter(user=request.user)
    else:
        cart_items = []
    
    context = {
      
        'products': products,
        'cart': cart_items,
        'user_products': user_products,
        'pay': pay,
        'wishlist_items': wishlist_items,
        'stores': stores,
        'categories': categories,
        'hot_deal': hot_deal,
        'top_selling_products': top_selling_products,  
        'slide': slide,
        'videos': videos
    }
    return render(request, 'main/index.html', context=context)


@login_required(login_url='login')
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        size_id = request.POST.get('size')
        size = Size.objects.filter(id=size_id).first() if size_id else None

        price = size.price if size else product.new_price

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            size=size
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, "Product quantity updated in cart.")
        else:
            cart_item.quantity = 1
            cart_item.price = price
            cart_item.save()
            messages.success(request, "Product added to cart.")
        return redirect('index')
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('index')
    
@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_quantity = sum(item.quantity for item in cart_items)
    total_amount = sum(item.item_total() for item in cart_items) 

    context = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_amount': total_amount,
    }
    return render(request, 'main/cart.html', context)
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_quantity = sum(item.quantity for item in cart_items)
    total_amount = sum(item.item_total for item in cart_items) 
    context = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_amount': total_amount,
    }
    return render(request, 'main/cart.html', context)
@login_required
def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    size_id = request.POST.get('size')
    action = request.POST.get('action')

    size = None
    if size_id:
        size = Size.objects.filter(id=size_id).first()

    try:
        cart_item = Cart.objects.get(user=request.user, product=product, size=size)
    except Cart.DoesNotExist:
        if action == 'increment':
            price = size.price if size else product.new_price
            Cart.objects.create(user=request.user, product=product, size=size, quantity=1, price=price)
        return redirect('cart')

    if action == 'increment':
        cart_item.quantity += 1
    elif action == 'decrement':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        elif cart_item.quantity == 1:
            cart_item.delete()
            messages.success(request, "Item removed from cart.")
            return redirect('cart')
    cart_item.save()

    return redirect('cart')
@login_required
@login_required
def delete_from_cart(request, product_id):
    cart_items = Cart.objects.filter(user=request.user, product_id=product_id)
    
    if cart_items.exists():
        cart_items.delete()
        messages.success(request, "Product removed from cart.")
    else:
        messages.error(request, "Product not found in cart.")
    
    return redirect('cart')

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            backend = 'django.contrib.auth.backends.ModelBackend'
            user.backend = backend
            login(request, user, backend=backend)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("index")
    else:
        form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"register_form": form})
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("index")
                else:
                    messages.error(request, "Invalid username or password.")
            except PyJWTError:
                messages.error(request, "Error processing authentication token.")
                return redirect("login")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")
   
def pay(request):
    if not request.user.is_authenticated:
        return redirect('login')  
    quantity = 0
    summ = 0
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        quantity += item.quantity
        summ += item.product.new_price * item.quantity
    if request.method == 'POST':
        form = PayForm(request.POST)
        if form.is_valid():
            pay = form.save(commit=False)
            pay.user = request.user
            if 'cart_id' in request.session:
                try:
                    pay.cart = Cart.objects.get(id=request.session['cart_id'], user=request.user)
                    pay.save()
                    messages.info(request, "You have successfully paid.")
                    return redirect('index')
                except Cart.DoesNotExist:
                    messages.error(request, "Invalid cart ID.")
                    return redirect('index')
            else:
                messages.error(request, "Cart ID not found in session.")
                return redirect('index')
    else:
        form = PayForm()
    return render(request, 'main/payment.html', context={
        'form': form,
        'summ': summ,
        'quantity': quantity,
        'cart_items': cart_items
    })
def user_details(request):
    if request.method == "POST":
        form = UserMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Details submitted successfully.")
            return redirect('index')
    else:
        form = UserMessageForm()
    return render(request, 'main/address_after_payment.html', context={'form': form})

def all_accessories(request):
    try:
        accessories_category = Category.objects.get(category_name='Accessories')
        accessories = Product.objects.filter(category=accessories_category)
    except Category.DoesNotExist:
        accessories = Product.objects.none()
    
    context = {
        'accessories': accessories
    }

    return render(request, 'main/all_accessories.html', context)





@login_required
def accept_cookies(request):
    if request.method == "POST":
        CookieConsent.objects.update_or_create(user=request.user, defaults={'accepted_cookies': True})
        return redirect("index")  
    return render(request, "cookiegroup_list.html")

def my_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  
    
    if not CookieConsent.objects.filter(user=request.user, accepted_cookies=True).exists():
        return render(request, "accept_cookies.html")
    
    return render(request, "index.html")

register = template.Library()


@register.filter
def cookie_group_accepted(request, arg):
    """
    Filter returns if cookie group is accepted.

    Examples:
    ::

        {{ request|cookie_group_accepted:"analytics" }}
        {{ request|cookie_group_accepted:"analytics=*:.google.com" }}
    """
    value = get_cookie_value_from_request(request, *arg.split("="))
    return value is True


@register.filter
def cookie_group_declined(request, arg):
    """
    Filter returns if cookie group is declined.
    """
    value = get_cookie_value_from_request(request, *arg.split("="))
    return value is False


@register.filter
def all_cookies_accepted(request):
    """
    Filter returns if all cookies are accepted.
    """
    return are_all_cookies_accepted(request)


@register.simple_tag
def not_accepted_or_declined_cookie_groups(request):
    """
    Assignement tag returns cookie groups that does not yet given consent
    or decline.
    """
    return get_not_accepted_or_declined_cookie_groups(request)


@register.filter
def cookie_consent_enabled(request):
    """
    Filter returns if cookie consent enabled for this request.
    """
    return is_cookie_consent_enabled(request)


@register.simple_tag
def cookie_consent_accept_url(cookie_groups):
    """
    Assignement tag returns url for accepting given concept groups.
    """
    varnames = ",".join([g.varname for g in cookie_groups])
    url = reverse("cookie_consent_accept", kwargs={"varname": varnames})
    return url


@register.simple_tag
def cookie_consent_decline_url(cookie_groups):
    """
    Assignement tag returns url for declining given concept groups.
    """
    varnames = ",".join([g.varname for g in cookie_groups])
    url = reverse("cookie_consent_decline", kwargs={"varname": varnames})
    return url


@register.simple_tag
def get_accept_cookie_groups_cookie_string(request, cookie_groups):  
    """
    Tag returns accept cookie string suitable to use in javascript.
    """
    warnings.warn(
        "Cookie string template tags for JS are deprecated and will be removed "
        "in django-cookie-consent 1.0",
        DeprecationWarning,
    )
    cookie_dic = get_cookie_dict_from_request(request)
    for cookie_group in cookie_groups:
        cookie_dic[cookie_group.varname] = cookie_group.get_version()
    return get_cookie_string(cookie_dic)


@register.simple_tag
def get_decline_cookie_groups_cookie_string(request, cookie_groups):
    """
    Tag returns decline cookie string suitable to use in javascript.
    """
    warnings.warn(
        "Cookie string template tags for JS are deprecated and will be removed "
        "in django-cookie-consent 1.0",
        DeprecationWarning,
    )
    cookie_dic = get_cookie_dict_from_request(request)
    for cookie_group in cookie_groups:
        cookie_dic[cookie_group.varname] = settings.COOKIE_CONSENT_DECLINE
    return get_cookie_string(cookie_dic)


@register.simple_tag
def js_type_for_cookie_consent(request, varname, cookie=None):
    """
    Tag returns "x/cookie_consent" when processing javascript
    will create an cookie and consent does not exists yet.

    Example::

      <script type="{% js_type_for_cookie_consent request "social" %}"
      data-varname="social">
        alert("Social cookie accepted");
      </script>
    """
    warnings.warn(
        "Template tags for use in/with JS are deprecated and will be removed "
        "in django-cookie-consent 1.0",
        DeprecationWarning,
    )
    enabled = is_cookie_consent_enabled(request)
    if not enabled:
        res = True
    else:
        value = get_cookie_value_from_request(request, varname, cookie)
        if value is None:
            res = settings.COOKIE_CONSENT_OPT_OUT
        else:
            res = value
    return "text/javascript" if res else "x/cookie_consent"


@register.filter
def accepted_cookies(request):
    """
    Filter returns accepted cookies varnames.

    .. code-block:: django

        {{ request|accepted_cookies }}

    """
    return [c.varname for c in get_accepted_cookies(request)]


@register.simple_tag
def all_cookie_groups(element_id: str):
    """
    Serialize all cookie groups to JSON and output them in a script tag.

    :param element_id: The ID for the script tag so you can look it up in JS later.

    This uses Django's core json_script filter under the hood.
    """
    groups = get_all_cookie_groups()
    value = [group.for_json() for group in groups.values()]
    return json_script(value, element_id)




from allauth.account.views import LoginView

class CustomLoginView(LoginView):
    def form_valid(self, form):
        return super().form_valid(form)