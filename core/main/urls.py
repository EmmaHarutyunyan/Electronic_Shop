from django.urls import path, re_path,include
from django.views.decorators.csrf import csrf_exempt
from . import views
from .views import (
    CookieGroupAcceptView,
    CookieGroupDeclineView,
    CookieGroupListView,
    CookieStatusView,
)
from django.views.generic import TemplateView 
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='index'),
    path('product/', views.product, name='product'),
    path('products/', views.all_products, name='all_products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('color/<int:color_id>/', views.color_based_product, name='color_based_product'),
    path('admin/update_sizes/<int:product_id>/', views.update_sizes, name='update_sizes'),
    path('checkout/', views.checkout, name='checkout'),
    path('store/', views.store, name='store'),
    path('login/', views.login_request, name='login'),
    path('register/', views.register_request, name='register'),
    path('logout/', views.logout_request, name='logout'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('add_to_cart_from_wishlist/<int:product_id>/', views.add_to_cart_from_wishlist, name='add_to_cart_from_wishlist'),
    path('delete_from_wishlist/<int:product_id>/', views.delete_from_wishlist, name='delete_from_wishlist'),
    path('pay/', views.pay, name='pay'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('delete_from_cart/<int:product_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('accessories/', views.all_accessories, name='all_accessories'),
    path('accept-cookies/', views.accept_cookies, name='accept_cookies'),
    path('sign-in/', TemplateView.as_view(template_name='sign_in.html'), name='sign_in'),
    path('sign-up/', TemplateView.as_view(template_name='sign_up.html'), name='sign_up'),
    path('sign-in-via-google/', TemplateView.as_view(template_name='sign_in_via_google.html'), name='sign_in_via_google'),
    path('accounts/', include('allauth.urls')), 
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path("accept/", csrf_exempt(CookieGroupAcceptView.as_view()), name="cookie_consent_accept_all"),
    re_path(r"^accept/(?P<varname>.*)/$", csrf_exempt(CookieGroupAcceptView.as_view()), name="cookie_consent_accept"),
    re_path(r"^decline/(?P<varname>.*)/$", csrf_exempt(CookieGroupDeclineView.as_view()), name="cookie_consent_decline"),
    path("decline/", csrf_exempt(CookieGroupDeclineView.as_view()), name="cookie_consent_decline_all"),
    path("status/", CookieStatusView.as_view(), name="cookie_consent_status"),
    path("", CookieGroupListView.as_view(), name="cookie_consent_cookie_group_list"),
]