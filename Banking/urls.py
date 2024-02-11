from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('onlinebanking/', views.onlinebanking, name='onlinebanking'),
    path('applyforloan/', views.applyforloan, name='applyforloan'),
    path('statement/', views.statement, name='statement'),
    path('contactus/', views.contactus, name='contactus'),
    path('register/', views.registration_form, name='register'),
    path('profile/', views.profile, name='profile'),
    path('updateprofile/',views.update_profile,name='updateprofile'),
    path('login/',views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('adminlogin/',views.login_admin,name='adminlogin'),
    path('adminlogout/',views.logout_admin,name='adminlogout'),
    path('applications/', views.applications, name='applications'),
    path('loanapplications/',views.loan_application,name='loanapplications'),
    path('aprovedloanapplications/<int:loan_id>',views.approve_loan_application,name='approvedloanapplications'),
    path('declinedloanapplications/<int:loan_id>',views.declined_loan_application,name='declinedloanapplications'),
    path('payemi/<int:loan_id>/',views.pay_emi, name='pay_emi'),
    path('approve/<int:registration_id>/', views.approve_registration, name='approve_registration'),
    path('decline/<int:registration_id>/', views.decline_registration, name='decline_registration'),
    path('money-transfer/', views.money_transfer, name='moneytransfer'),
    path('moneytransferconfirm/', views.transfer_confirmation, name='moneytransferconfirm'),
    path('confirmotp', views.confirm_otp_transfer, name='confirmotp'),
    path('deposit/', views.deposit, name='deposit'),
    path('manage_beneficiaries/', views.manage_beneficiaries, name='manage_beneficiaries'),
    path('delete_beneficiary/<int:beneficiary_id>/', views.delete_beneficiary, name='delete_beneficiary'),
    path('fetch_user_details/', views.fetch_user_details, name='fetch_user_details'),
    path('otpverification/',views.otp_verification,name='otpverification'),
    path('send_otp/', views.send_otp_email, name='send_otp_email'),
    path('users/',views.total_users,name='users'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('help/',views.help,name='help'),
    path('reports/',views.reports,name='reports'),
    path('logout-on-unload/', views.logout_on_unload, name='logout_on_unload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
