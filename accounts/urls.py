from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customer/<int:pk>', views.customer, name='customer'),  # <a href="{% url 'customer' customer.id %}
    path('user/', views.user_page, name='user_page'),
    path('settings/', views.account_settings, name='account'),

    path('create_order/<int:pk>', views.create_order, name='create_order'),
    path('update_order/<int:pk>', views.update_order, name='update_order'),
    path('delete_order/<int:pk>', views.delete_order, name='delete_order'),

    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),

    # submit email form
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    # Sent email message successfully
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    # Link to password reset form in email; uidb64(encoded user's id in base 64); token(check if password is valid)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Password successfully changed message
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

'''
accounts/ password_reset/ [name='password_reset']
accounts/ password_reset/done/ [name='password_reset_done']
accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/ reset/done/ [name='password_reset_complete']
1 - submit email form                           PasswordResetView.as_view()
2 - Sent email message successfully             PasswordResetDoneView.as_view()
3 - Link to password reset form in email        PasswordResetConfirmView.as_view()
4 - Password successfully changed message       PasswordResetCompleteView.as_view()
'''
