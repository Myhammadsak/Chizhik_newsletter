from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

app_name = 'puddle'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='puddle/login.html', authentication_form=LoginForm),
         name='login'),
    path('logout/', views.logout_v, name='logout'),
    path('telegram/request-code/', views.send_telegram_code_view, name='send_telegram_code'),
    path('telegram/confirm-code/', views.confirm_telegram_code_view, name='confirm_telegram_code'),
    path('group/add/', views.add_chats, name='add_group'),
    path('newsletter/create/', views.newsletter_create, name='newsletter_create'),
    path("newsletter/start/<int:pk>/", views.start_newsletter_view, name='start_newsletter_view'),
    path('newsletter/logs/', views.newsletter_logs_view, name='newsletter-logs'),
    path('get-logs/', views.get_logs, name='get-logs'),
    path('newsletter/list/', views.list_newsletter, name='newsletter_list'),
    path('newsletter/<int:pk>/', views.detail_newsletter, name='detail_newsletter'),
    path('newsletter/delete/<int:pk>/', views.delete_newsletter, name='delete_newsletter'),
    path('groups/', views.list_chats, name='list_chats'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='puddle/password_reset_form.html',
                                                                 email_template_name='puddle/password_reset_email.html',
                                                                 success_url=reverse_lazy(
                                                                     'puddle:password_reset_done')),
         name='password_reset'),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='puddle/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='puddle/password_reset_confirm.html',
                                                     success_url=reverse_lazy('puddle:password_reset_complete')),
         name='password_reset_confirm'),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='puddle/password_reset_complete.html'),
         name='password_reset_complete'),
]
