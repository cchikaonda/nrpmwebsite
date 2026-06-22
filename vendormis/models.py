from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel


# =========================================================
# VENDOR STATUS
# =========================================================
class VendorStatus(models.TextChoices):
    PENDING = "Pending", "Pending"
    APPROVED = "Approved", "Approved"
    REJECTED = "Rejected", "Rejected"


# =========================================================
# VENDOR PROFILE
# =========================================================
class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    personal_detail = models.OneToOneField(
        "PersonalDetail",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=VendorStatus.choices,
        default=VendorStatus.PENDING
    )

    vendor_code = models.CharField(max_length=30, unique=True, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.vendor_code:
            last_id = VendorProfile.objects.count() + 1
            self.vendor_code = f"VMIS-{last_id:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} ({self.status})"


# =========================================================
# LOGIN ACTIVITY LOG
# =========================================================
class LoginActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"


# =========================================================
# LOCATION MODELS
# =========================================================
@register_snippet
class Nation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Nations"


@register_snippet
class District(models.Model):
    name = models.CharField(max_length=100)
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Districts"


@register_snippet
class TraditionalAuthority(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Traditional Authorities"


@register_snippet
class Village(models.Model):
    name = models.CharField(max_length=100)
    traditional_authority = models.ForeignKey(TraditionalAuthority, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Villages"

# =========================================================
# PERSONAL DETAILS
# =========================================================
@register_snippet
class PersonalDetail(models.Model):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    first_name = models.CharField(max_length=30)
    other_names = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    nationality = models.ForeignKey(Nation, on_delete=models.SET_NULL, null=True)
    national_id_number = models.CharField(max_length=20, unique=True)

    phone_validator = RegexValidator(
        regex=r"^\+?265?\d{8,12}$",
        message="Enter valid Malawi number e.g. +265991234567"
    )

    phone_number = models.CharField(
        max_length=20,
        validators=[phone_validator],
        unique=True
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        FieldPanel("first_name"),
        FieldPanel("other_names"),
        FieldPanel("surname"),
        FieldPanel("gender"),
        FieldPanel("nationality"),
        FieldPanel("national_id_number"),
        FieldPanel("phone_number"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return f"{self.first_name} {self.surname}"


# =========================================================
# ORIGIN DETAILS
# =========================================================
@register_snippet
class DistrictOfOrigin(models.Model):
    personal_detail = models.ForeignKey(PersonalDetail, on_delete=models.CASCADE)

    district = models.ForeignKey(District, on_delete=models.CASCADE)
    traditional_authority = models.ForeignKey(TraditionalAuthority, on_delete=models.CASCADE)
    village = models.ForeignKey(Village, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.district} - {self.village}"


# =========================================================
# RESIDENTIAL ADDRESS
# =========================================================
class ResidentialAddress(models.Model):
    personal_detail = models.ForeignKey(PersonalDetail, on_delete=models.CASCADE)

    street_address = models.CharField(max_length=255)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    traditional_authority = models.ForeignKey(TraditionalAuthority, on_delete=models.CASCADE)
    village = models.ForeignKey(Village, on_delete=models.CASCADE)

    def __str__(self):
        return self.street_address


# =========================================================
# MARKET
# =========================================================
@register_snippet
class Market(models.Model):
    name = models.CharField(max_length=100, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    market_code = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


# =========================================================
# BUSINESS DETAILS
# =========================================================
@register_snippet
class BusinessDetail(models.Model):
    CATEGORY_CHOICES = [
        ("hardware", "Hardware"),
        ("food", "Food"),
        ("stationery", "Stationery"),
        ("textile", "Textile"),
        ("barbershop", "Barbershop/Salon"),
        ("electronics", "Electronics"),
        ("other", "Other"),
    ]

    MEMBERSHIP_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
    ]

    # CHANGE TO ForeignKey if multiple businesses allowed
    personal_detail = models.ForeignKey(
        PersonalDetail,
        on_delete=models.CASCADE,
        related_name="businesses"
    )

    sub_unit_number = models.CharField(max_length=20)
    shop_bench = models.CharField(max_length=50)
    business_name = models.CharField(max_length=100, blank=True, null=True)

    registration_certificate = models.CharField(max_length=100, blank=True, null=True)
    registration_date = models.DateField(blank=True, null=True)

    category_of_business = models.CharField(max_length=30, choices=CATEGORY_CHOICES)

    tpin = models.CharField(max_length=15, blank=True, null=True)

    market = models.ForeignKey(Market, on_delete=models.SET_NULL, null=True)

    membership_of_association = models.CharField(max_length=3, choices=MEMBERSHIP_CHOICES)
    date_joined = models.DateField()

    panels = [
        FieldPanel("personal_detail"),
        FieldPanel("sub_unit_number"),
        FieldPanel("shop_bench"),
        FieldPanel("business_name"),
        FieldPanel("registration_certificate"),
        FieldPanel("registration_date"),
        FieldPanel("category_of_business"),
        FieldPanel("tpin"),
        FieldPanel("market"),
        FieldPanel("membership_of_association"),
        FieldPanel("date_joined"),
    ]

    def __str__(self):
        return self.business_name or "Unnamed Business"


# =========================================================
# APPROVAL
# =========================================================
@register_snippet
class Approval(models.Model):
    business_detail = models.OneToOneField(BusinessDetail, on_delete=models.CASCADE)

    approved_by_full_name = models.CharField(max_length=100)
    approved_by_organisation = models.CharField(max_length=100)

    signature = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    approval_date = models.DateField()

    def __str__(self):
        return f"Approval - {self.business_detail}"


# =========================================================
# FORM COLLECTION
# =========================================================
@register_snippet
class FormCollection(models.Model):
    approval = models.OneToOneField(Approval, on_delete=models.CASCADE)

    collected_by_full_name = models.CharField(max_length=100)
    collected_by_organisation = models.CharField(max_length=100)

    title = models.CharField(max_length=50)

    signature = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    collection_date = models.DateField()

    def __str__(self):
        return f"Collected by {self.collected_by_full_name}"