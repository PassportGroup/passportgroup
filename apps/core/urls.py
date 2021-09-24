from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index_view, name='home'),
    path('login/', login_view, name="login"),
    # path('verify/email/', verify_email_form_view, name="verify.phone"),
    # path('verify/email/<uidb64>/<token>/', verify_email_view, name="verify.email"),
    path('logout/', logout_view, name="logout"),

    # ======== PASSWORD RESET WITH EMAIL AND PHONE NUMBER ===========
    # path('password-forgot/reset/', forgot_password_view, name="password.forgot"),
    # path('password/reset/<uidb64>/<token>/', password_reset_view, name="password.reset"),
    # path('password/reset/', set_password_view, name="password.set"),
    #
    # path('listing/<slug:slug>/', listing_detail_view, name = "listing"),
    # path('profile/', include('apps.userprofile.urls')),
    # # path('notifications/', include('apps.notifications.urls')),


    #=========== Multi Language / Auth Routes ===========
    path('setlang/', set_locale_view, name="locale.set"),

    path('privacy-policy/', privacy_policy, name="privacy.policy"),
    path('terms-of-service/', terms_of_service, name="terms.of.service"),
]


