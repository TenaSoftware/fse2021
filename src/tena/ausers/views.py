"""
`ausers` views for tena project.

Generated by 'python3 manage.py startapp' using Django 3.1.7.
 * NAME: Wendirad Demelash
 * DATE: April 3, 2021
"""
import logging
import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as AuthLogin
from django.contrib.auth.views import PasswordResetView as AuthPasswordRest
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, FormView
from twilio.base.exceptions import TwilioRestException

from ausers.forms import PasswordResetForm, SignUpForm, VerficationForm
from ausers.mixins import SiteRequiredMixin
from ausers.models import Customer
from ausers.utils import twilio_message

class SignUpView(SiteRequiredMixin, CreateView):
    """ SignUp view to implement user registration. """

    model = Customer
    form_class = SignUpForm
    site_id = 1
    template_name = "ausers/signup_form.html"
    success_url = reverse_lazy("verify-customer")

    def form_valid(self, form):
        """ send verification code to registered user. """
        super().form_valid(form)
        self.object.username = self.object.phone_number
        self.object.work_on.add(1)
        self.request.session["phone_number"] = self.object.phone_number
        self.object.save()
        try:
            twilio_message.send_verification(self.request.session["phone_number"])
        except TwilioRestException as error:
            logging.error(error)
            return None
        return HttpResponseRedirect(self.get_success_url())


class VerifyCustomer(SiteRequiredMixin, FormView):
    """ View to handle user verification. """

    form_class = VerficationForm
    site_id = 1
    template_name = "ausers/verfication_form.html"
    success_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        """ send verification code for customer not verified while registering."""
        if (
            request.user.is_authenticated
            and not request.user.__class__.__name__ == "User"
        ):
            self.request.session["phone_number"] = request.user.phone_number
            twilio_message.send_verification(self.request.session["phone_number"])
        return super().get(request)

    def get_form(self, form_class=None):
        """ replace super get_form method to pass request argument to form."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        """ Check and change user verification status."""
        phone_number = self.request.session["phone_number"]
        status = self.make_verified(phone_number)
        if status:
            form.request.session.pop("phone_number")
            return super().form_valid(form)
        form.add_error(None, "Something wrong, please try again!")
        return self.form_invalid(form)

    def make_verified(self, phone_number):  # pylint disable=no-self-
        """
        Change customer verification status active.
        return False if customer is not valid else return True
        """
        try:
            customer = Customer._default_manager.get_by_natural_key(
                phone_number
            )  # pylint: disable=no-member, protected-access
        except Customer.DoesNotExist:
            return False
        customer.is_verified = True
        customer.save()
        return True


class LoginView(AuthLogin):
    """Extend default LoginView to redirect authenticated user automatically."""

    redirect_authenticated_user = True


class PasswordResetView(AuthPasswordRest):
    """
    Extended PasswordResetView to send password reset link
    via email for users and via SMS for customers.
    """

    form_class = PasswordResetForm

    def get_link(self, user):
        """ Generate verification token and return password reset link. """
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        current_site = get_current_site(self.request)
        domain = current_site.domain
        protocol = "https" if settings.SECURE_SSL_REDIRECT else "http"
        return (
            f"{protocol}://{domain}"
            f'{reverse_lazy("password_reset_confirm", args=(uid, token)).__str__()}'
        )

    def form_valid(self, form):
        """ send password reset link, if user is customer."""
        data = form.data.get("email")
        if re.match(r"(\+2519|09)\d{8}$", data):
            try:
                user = get_user_model()._default_manager.get_by_natural_key(
                    data
                )  # pylint: disable=protected-access
                link = self.get_link(user)
                body = (
                    f"Hello {user.first_name}, here is your link to your reset your"
                    f" password. follow the link for further instruction \n\n{link}"
                    f"\n\nThank You.\nTena Transport."
                )
                twilio_message.send_message(user.customer.phone_number, body)
            except Customer.DoesNotExist:
                pass
            except TwilioRestException as error:
                logging.error(error)
                url = reverse_lazy(
                    "send-message", args=("Something went wrong. Try again!")
                )
                return HttpResponseRedirect(url)
            return HttpResponseRedirect(self.get_success_url())
        return super().form_valid(form)
