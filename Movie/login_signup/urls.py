from django.urls import path, include

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('register/', views.clientregisterPage, name="clientregister"),
    path('adminregister/', views.adminregisterPage, name="adminregister"),

    # 1st step - Password reset garna ko lagi, email id halnu parxa so tyo page ko URL ho
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="login_signup/password_reset.html"),
         name="reset_password"),
    # auth_views.PasswordResetView.as_view  -> yaha  .as_view kina gareko vanda PasswordResetView chai django ko default class view ho so testo view ko lagi  .as_view garna parxa  &  testo defualt django view le default django template nai render garauxa.. so yedi hamilai django ko default template man parena vani teslai override pani garna sakxau . So, to override that page ->  (template_name="accounts/password_reset.html)

    # 2nd step - Email ID hali sake paxi, paswword reset link send vai sakyo tapaiko mail ma vanera jun page display hunxa tyo page ko lagi URL ho
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="login_signup/password_reset_sent.html"),
         name="password_reset_done"),

    # 3rd Step - Naya Password halna ko lagi or Confirm garna ko lagi... yo page display garne URL ho
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="login_signup/password_reset_form.html"),
         name="password_reset_confirm"),
    # 4th Step - Password reset Sucess vai sake paxi,, password reset complete vayo aba tapai feri login garna saknu hunxa vanera jun Page display hunxa tesko URL ko lagi
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="login_signup/password_reset_done.html"),
         name="password_reset_complete"),

    path('logoutall/', views.logoutall, name="logoutall"),

    path('accounts/', include('allauth.urls')),     #allauth ko urls haru django le nai provide gareko huncha



    # Path For Email url when user clicks on email
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),

]
