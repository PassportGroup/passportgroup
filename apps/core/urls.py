from django.urls import path
from .views import *

urlpatterns = [
    path('', index_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name="logout"),

    # =========== Multi Language / Auth Routes ===========
    path('setlang/', set_locale_view, name="locale.set"),

    path('privacy-policy/', privacy_policy, name="privacy.policy"),
    path('terms-of-service/', terms_of_service, name="terms.of.service"),

]


