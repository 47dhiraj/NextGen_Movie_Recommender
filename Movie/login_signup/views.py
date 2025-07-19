from django.shortcuts import render, redirect

from login_signup.forms import CreateClientForm, CreateAdminForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .decorators import admin_required, client_required

from django.contrib.auth import authenticate, login,logout

import requests
import sweetify


from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token

from django.utils.encoding import force_text
from django.utils.encoding import force_bytes
from .models import User



# Views here ...



def clientregisterPage(request):

    if request.method == 'POST':
        form = CreateClientForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')

            api_key = '8d7e1b7f-022b-4bf5-8661-ac2f949a1a1c'
     
            response = requests.get("https://isitarealemail.com/api/email/validate",            # API ko end point
                params={'email': email},                                                        # hamro email as a params pathauna parcha
                headers={
                    'Authorization': "Bearer " + api_key})                                      # API key lai chai headers vanni field ma 'Authorization' as a headers send garna parcha

            status = response.json()['status']                                                  # response ma ayeko kura lai json ma lageko
                                                                                                # email valid cha vani status ma 'valid' response auncha else 'invalid' auncha ..
                                                                                                # yedi user le jpt domain vako email eg: aaaa@bbb.com yesto diyo vani 'unknown' response auncha becz yo email bata kei tha hunaa becz mail server ko name nai jpt diyeko cha

            if status == "valid":

                user = form.save()                                                              # yo code run hune bittikai  signals.py page ma user as Sender le signa pathauxa , for calling customer_profile function




                current_site = get_current_site(request)
                subject = 'Please Activate Your Account'
                message = render_to_string('login_signup/activation_request.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)  # email_user() djanog le diyeko inbuilt method ho ...  # email send garna django le arko method pani deko cha i.e send_mail()




                sweetify.success(request, 'Account Successfully Registered!', text='Please ! Check your email address to activate account.', persistent='Ok', icon='success')



                return redirect('login')                                                         # login page redirect garda, messages lai redirect garnu pardaina... jun sukkai page ma tyo messages.success xa vane pani matlab hudaina... tmlai jun page ma chaiyo tei page ma display garauna sakxau... hamilai register gari sake paxi, login page ma gai sake paxi display garauna xa ... so login page ma message display garauna sakinxa without redirecting messages to login page

            else:
                sweetify.error(request, 'Invalid Email !', text='Please ! Insert Valid Email Address.', persistent='Close', icon='error')
                return redirect('clientregister')
        else:
            context = {'form': form}
            return render(request, 'login_signup/register.html', context)

    else:
        form = CreateClientForm()

        def get_context_data(self, **kwargs):
            kwargs['user_type'] = 'client'
            return super().get_context_data(**kwargs)

        context = {'form': form}
        return render(request, 'login_signup/register.html', context)






def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save()
        # login(request, user)

        sweetify.success(request, 'Account Activated Successfully!',
                         text='Please! Login with your credentials', persistent='Ok', icon='success')
        return redirect('login')
    else:
        return render(request, 'login_signup/activation_invalid.html')








@login_required
@admin_required
def adminregisterPage(request):
    form = CreateAdminForm()

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    if request.method == 'POST':
        form = CreateAdminForm(request.POST)

        if form.is_valid():
            user = form.save()  # yo code run hune bittikai  signals.py page ma user as Sender le signa pathauxa , for calling customer_profile function
            username = form.cleaned_data.get('username')  # form.cleaned_data.get ko kaam vaneko form ko kunnai attribute ko value alaggai nikalnu paryo vani yesari nikalinxa

            messages.success(request, username + ' is also added as a new Admin.')  # SYNTAX:  messages.success(request,'Custom message')

            return redirect('adminhome')  # login page redirect garda, messages lai redirect garnu pardaina... jun sukkai page ma tyo messages.success xa vane pani matlab hudaina... tmlai jun page ma chaiyo tei page ma display garauna sakxau... hamilai register gari sake paxi, login page ma gai sake paxi display garauna xa ... so login page ma message display garauna sakinxa without redirecting messages to login page

    context = {'form': form}
    return render(request, 'login_signup/register.html', context)





def loginPage(request):
    # yo talako code Chai POST method ko lagi ho
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:  # user ko value TRUE xa i.e FALSE chaina vani vaneko... khas ma mathi ko authenticate le Boolean Value return garxa i.e user authenticate vayo vani TRUE return garxa & vayena vani chai FALSE return garxa
            login(request,user)  # login(request, user) django ko inbuilt keyword jastai ho jasle login vaye ko user ko session lai database ko django_session table ma hold garera rakhcha.
            # return redirect('home')	#login vai sake paxi home page ko access dinxa

            if request.user.is_client:
                return redirect('clienthome')
            else:
                return redirect('adminhome')


        else:
            messages.error(request,'Username OR password is incorrect')  # SYNTAX: messages.info(request, 'Custom Message').......django le provide gareko informative message lai display garaune kaam garxa

    # yo talako code GET method ko lagi ho
    context = {}
    if not request.user.is_authenticated:
        return render(request, 'login_signup/login.html', context)
    else:
        return redirect('home')





@login_required
def logoutall(request, reason=''):
    if request.method == "POST":
        logout(request)  # logout(request) chai django le diyeko inbuilt features ho
        return redirect('login')  # logout garepaxi  feri login page ma redirect gardinxa
    return redirect('home')
