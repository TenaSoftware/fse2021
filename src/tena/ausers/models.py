"""
`ausers` models for tena project.

Generated by 'python3 manage.py startapp' using Django 3.1.7.
 * NAME: Wendirad Demelash
 * DATE: April 3, 2021
"""
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DefaultUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from smart_selects.db_fields import ChainedForeignKey

class Region(models.Model):
    """ a model to register regions in Ethiopia. """
    name = models.CharField(_("Name"), max_length=255)

    def __str__(self):
        return self.name

class Zone(models.Model):
    """a model to register zone with appropriate
    region in Ethiopia."""

    region = models.ForeignKey(
        Region, verbose_name=_("Region"), on_delete=models.CASCADE
    )
    name = models.CharField(_("Name"), max_length=255)

    def __str__(self):
        return f"{self.name} | {self.region.name}"

class Woreda(models.Model):
    """a model to register woreda with appropriate
    zone and region in Ethiopia."""

    region = models.ForeignKey(
        Region, verbose_name=_("Region"), on_delete=models.CASCADE
    )
    zone = ChainedForeignKey(
        Zone,
        verbose_name=_("Zone"),
        chained_field="region",
        chained_model_field="region",
        show_all=False,
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} | {self.region.name}"

class Address(models.Model):
    """Implement common address attributes
    - Region
    - Zone
    - Woreda
    - House Number
    """

    region = models.ForeignKey(
        Region, verbose_name=_("Region"), on_delete=models.SET_NULL, null=True
    )
    zone = ChainedForeignKey(
        Zone,
        verbose_name=_("Zone"),
        chained_field="region",
        chained_model_field="region",
        show_all=False,
    )
    woreda = ChainedForeignKey(
        Woreda,
        verbose_name=_("Woreda"),
        chained_field="zone",
        chained_model_field="zone",
        show_all=False,
    )
    house_number = models.CharField(
        _("House number"), max_length=6, blank=True, null=True
    )

    class Meta:
        abstract = True

class UserManager(DefaultUserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        superuser = super().create_superuser(
            username, email=email, password=password, **extra_fields
        )
        superuser.work_on.set([1, 2])
        return superuser

class User(AbstractUser):
    """ This class represent all users in the system."""

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    SEX = (("M", _("Male")), ("F", _("Female")))
    sex = models.CharField(_("Sex"), max_length=2, choices=SEX)
    date_of_birth = models.DateField(null=True, blank=True)
    USERNAME_FIELD = "username"
    work_on = models.ManyToManyField(Site)
    objects = UserManager()
    on_site = CurrentSiteManager("work_on")

    class Meta:
        verbose_name = _("user")

class Customer(User, Address):
    """
    Representation of customer in the platform.

    Attributes
    ----------
    phone_regex: str
        regex to handle customers phone number.
    phone_number: CharField
        model field to handle customers phone number.
    is_verified: BooleanField
        model fields to check wether user is verified or not.

    """

    phone_regex = RegexValidator(
        r"(\+2519|09)\d{8}$",
        message="Please enter your phone number in +2519********"
        " or 09******** format.",
    )
    phone_number = models.CharField(
        _("Phone number"),
        max_length=13,
        validators=[phone_regex],
        primary_key=True,
        help_text=_("Use to verify and notify user."),
    )
    is_verified = models.BooleanField(
        default=False, help_text=_("Identify wether user is verified or not.")
    )
    USERNAME_FIELD = "phone_number"

    class Meta:
        """ Customer model options"""
        verbose_name = _("customer")

    def __str__(self):
        """ return customer short name as string represention."""
        return self.get_short_name()

class TicketOfficer(User):
    class Meta:
        verbose_name = "Ticket Officer"

class RouteOfficer(User):
    class Meta:
        verbose_name = "Route Officer"

class RouteEmployee(User):
    class Meta:
        verbose_name = "Route Employee"

class TicketEmployee(User):
    class Meta:
        verbose_name = "Ticket Employee"
