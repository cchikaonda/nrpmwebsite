from time import timezone
from .decorators import role_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import VendorRegistrationForm
from django.contrib.auth.decorators import login_required 
from django.views import View
from django.shortcuts import redirect, render
from .models import PersonalDetail, DistrictOfOrigin, ResidentialAddress, BusinessDetail, LoginActivity, Approval
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

# vendormis/views.py
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from formtools.wizard.views import SessionWizardView
from .forms import (
    VendorRegistrationForm,
    PersonalDetailForm,
    DistrictOfOriginForm,
    ResidentialAddressForm,
    BusinessDetailForm,
    VendorLoginForm,
)
from django.contrib.auth.forms import AuthenticationForm
from .models import PersonalDetail, DistrictOfOrigin, ResidentialAddress, BusinessDetail, VendorStatus

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Nation, District, TraditionalAuthority, Village, PersonalDetail, BusinessDetail, Market
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.dispatch import receiver
from .decorators import role_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

FORMS = [
    ("user", VendorRegistrationForm),
    ("personal", PersonalDetailForm),
    ("district", DistrictOfOriginForm),
    ("residential", ResidentialAddressForm),
    ("business", BusinessDetailForm),
]

TEMPLATES = {
    "user": "vendormis/vendor_register_step.html",
    "personal": "vendormis/vendor_register_step.html",
    "district": "vendormis/vendor_register_step.html",
    "residential": "vendormis/vendor_register_step.html",
    "business": "vendormis/vendor_register_step.html",
}

class VendorIndexView(TemplateView):
    template_name = "vendormis/vendor_index.html"


class VendorRegistrationWizard(SessionWizardView):
    form_list = FORMS
    template_name = "vendormis/vendor_register_step.html"

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        # Step 1: Create user
        user_form = form_list[0].save(commit=True)

        # Step 2: Personal Detail
        personal_form = form_list[1].save(commit=False)
        personal_form.user = user_form
        personal_form.save()

        # Step 3: District of Origin
        district_form = form_list[2].save(commit=False)
        district_form.personal_detail = personal_form
        district_form.save()

        # Step 4: Residential Address
        residential_form = form_list[3].save(commit=False)
        residential_form.personal_detail = personal_form
        residential_form.save()

        # Step 5: Business Detail
        business_form = form_list[4].save(commit=False)
        business_form.personal_detail = personal_form
        business_form.save()

        return redirect(reverse_lazy("vendormis:vendor_login"))

class VendorListView(LoginRequiredMixin, ListView):
    model = PersonalDetail
    template_name = "vendormis/vendor/vendor_list.html"
    context_object_name = "vendors"
    ordering = ["-id"]

class VendorDetailView(LoginRequiredMixin, DetailView):
    model = PersonalDetail
    template_name = 'vendormis/vendor/vendor_detail.html'
    context_object_name = 'vendor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        personal = self.object

        context["district"] = DistrictOfOrigin.objects.filter(
            personal_detail=personal
        ).first()

        context["residential"] = ResidentialAddress.objects.filter(
            personal_detail=personal
        ).first()

        context["business"] = BusinessDetail.objects.filter(
            personal_detail=personal
        ).first()

        return context
    
class VendorUpdateView(LoginRequiredMixin, View):
    template_name = "vendormis/vendor/vendor_form.html"

    def get(self, request, pk):
        personal = PersonalDetail.objects.get(pk=pk)

        form1 = VendorRegistrationForm(instance=personal.user)
        form2 = PersonalDetailForm(instance=personal)
        form3 = DistrictOfOriginForm(instance=personal.districtoforigin)
        form4 = ResidentialAddressForm(instance=personal.residentialaddress)
        form5 = BusinessDetailForm(instance=personal.businessdetail)

        return render(request, self.template_name, {
            "form1": form1,
            "form2": form2,
            "form3": form3,
            "form4": form4,
            "form5": form5,
        })

    def post(self, request, pk):
        personal = PersonalDetail.objects.get(pk=pk)

        form1 = VendorRegistrationForm(request.POST, instance=personal.user)
        form2 = PersonalDetailForm(request.POST, instance=personal)
        form3 = DistrictOfOriginForm(request.POST, instance=personal.districtoforigin)
        form4 = ResidentialAddressForm(request.POST, instance=personal.residentialaddress)
        form5 = BusinessDetailForm(request.POST, instance=personal.businessdetail)

        if all([
            form1.is_valid(),
            form2.is_valid(),
            form3.is_valid(),
            form4.is_valid(),
            form5.is_valid()
        ]):
            form1.save()
            form2.save()
            form3.save()
            form4.save()
            form5.save()

            return redirect("vendormis:vendor_list")

        return render(request, self.template_name, {
            "form1": form1,
            "form2": form2,
            "form3": form3,
            "form4": form4,
            "form5": form5,
        })

class VendorDeleteView(LoginRequiredMixin, DeleteView):
    model = PersonalDetail
    template_name = 'vendormis/vendor/vendor_confirm_delete.html'
    success_url = reverse_lazy('vendormis:vendor_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        # delete related records manually (safe cleanup)
        user = self.object.user

        BusinessDetail.objects.filter(personal_detail=self.object).delete()
        DistrictOfOrigin.objects.filter(personal_detail=self.object).delete()
        ResidentialAddress.objects.filter(personal_detail=self.object).delete()

        self.object.delete()
        user.delete()

        return redirect(self.success_url)

# Vendor registration view
class VendorRegisterView(FormView):
    template_name = 'vendormis/vendor_register.html'
    form_class = VendorRegistrationForm
    success_url = reverse_lazy('vendormis:vendor_dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Automatically log in the user after registration
        return super().form_valid(form)

def get_user_redirect(user):
    print("USER:", user.username)
    print("GROUPS:", list(user.groups.values_list("name", flat=True)))

    # Superuser → Django admin
    if user.is_superuser:
        print("→ ADMIN (superuser)")
        return reverse_lazy("admin:index")  # /django-admin/

    # Group-based redirects
    if user.groups.filter(name="Admin").exists():
        print("→ ADMIN (group)")
        return reverse_lazy("vendormis:admin_dashboard")

    if user.groups.filter(name="Officer").exists():
        print("→ OFFICER")
        return reverse_lazy("vendormis:officer_dashboard")

    if user.groups.filter(name="Vendor").exists():
        print("→ VENDOR")
        return reverse_lazy("vendormis:vendor_dashboard")

    # Default fallback
    print("→ DEFAULT (no group)")
    return reverse_lazy("vendormis:vendor_login")

class VendorLoginView(LoginView):
    template_name = "vendormis/vendor_index.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        print("🔥 LOGIN VIEW IS ACTIVE")
        return super().form_valid(form)

    def get_success_url(self):
        print("🔥 get_success_url CALLED")
        return get_user_redirect(self.request.user)

class VendorLogoutView(View):
    def get(self, request):
        logout(request)
        request.session.flush()  # extra security cleanup
        return redirect("/vendormis/login/")

# Vendor index page (landing page, optional public)
@role_required("Vendor")
class VendorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'vendormis/vendor_dashboard.html'
    login_url = reverse_lazy('vendormis:vendor_login')

@method_decorator(role_required("Officer"), name="dispatch")
class OfficerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "vendormis/officer/officer_dashboard.html"
    login_url = "/vendormis/login/"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name="Officer").exists():
            return redirect("/vendormis/login/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Officer Dashboard"

        # Example MIS stats (replace with real queries)
        context["total_vendors"] = PersonalDetail.objects.count()
        context["pending_approvals"] = 0
        context["approved_vendors"] = Approval.objects.count()

        return context


@method_decorator(role_required("Admin"), name="dispatch")
class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "vendormis/admin/admin_dashboard.html"
    login_url = "/vendormis/login/"

    def dispatch(self, request, *args, **kwargs):
        # Allow BOTH superuser AND Admin group
        if not (
            request.user.is_superuser or
            request.user.groups.filter(name="Admin").exists()
        ):
            return redirect("/vendormis/login/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Admin Dashboard"

        # Example MIS stats (replace with real queries later)
        context["total_users"] = 0
        context["total_vendors"] = 0
        context["pending_approvals"] = 0
        context["approved_vendors"] = 0
        context["total_officers"] = 0

        return context


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    LoginActivity.objects.create(
        user=user,
        ip_address=request.META.get('REMOTE_ADDR')
    )

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    LoginActivity.objects.filter(
        user=user,
        logout_time__isnull=True
    ).update(logout_time=timezone.now())

# Vendor logout
class VendorLogoutView(LogoutView):
    next_page = reverse_lazy('vendormis:vendor_login')


# Vendor dashboard (protected)
class VendorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'vendormis/vendor_dashboard.html'
    login_url = reverse_lazy('vendormis:vendor_login')

# -------------------------------
# Nation CRUD
# -------------------------------
class NationListView(ListView):
    model = Nation
    template_name = 'vendormis/nation/nation_list.html'
    context_object_name = 'nations'

class NationCreateView(CreateView):
    model = Nation
    fields = ['name']
    template_name = 'vendormis/nation/nation_form.html'
    success_url = reverse_lazy('vendormis:nation_list')

class NationUpdateView(UpdateView):
    model = Nation
    fields = ['name']
    template_name = 'vendormis/nation/nation_form.html'
    success_url = reverse_lazy('vendormis:nation_list')

class NationDeleteView(DeleteView):
    model = Nation
    template_name = 'vendormis/nation/nation_confirm_delete.html'
    success_url = reverse_lazy('vendormis:nation_list')


# -------------------------------
# District CRUD
# -------------------------------
class DistrictListView(ListView):
    model = District
    template_name = 'vendormis/district/district_list.html'
    context_object_name = 'districts'

class DistrictCreateView(CreateView):
    model = District
    fields = ['name', 'nation']
    template_name = 'vendormis/district/district_form.html'
    success_url = reverse_lazy('vendormis:district_list')

class DistrictUpdateView(UpdateView):
    model = District
    fields = ['name', 'nation']
    template_name = 'vendormis/district/district_form.html'
    success_url = reverse_lazy('vendormis:district_list')

class DistrictDeleteView(DeleteView):
    model = District
    template_name = 'vendormis/district/district_confirm_delete.html'
    success_url = reverse_lazy('vendormis:district_list')


# -------------------------------
# Traditional Authority CRUD
# -------------------------------
class TraditionalAuthorityListView(ListView):
    model = TraditionalAuthority
    template_name = 'vendormis/ta/traditionalauthority_list.html'
    context_object_name = 'tas'

class TraditionalAuthorityCreateView(CreateView):
    model = TraditionalAuthority
    fields = ['name', 'district']
    template_name = 'vendormis/ta/traditionalauthority_form.html'
    success_url = reverse_lazy('vendormis:traditionalauthority_list')

class TraditionalAuthorityUpdateView(UpdateView):
    model = TraditionalAuthority
    fields = ['name', 'district']
    template_name = 'vendormis/ta/traditionalauthority_form.html'
    success_url = reverse_lazy('vendormis:traditionalauthority_list')

class TraditionalAuthorityDeleteView(DeleteView):
    model = TraditionalAuthority
    template_name = 'vendormis/ta/traditionalauthority_confirm_delete.html'
    success_url = reverse_lazy('vendormis:traditionalauthority_list')


# -------------------------------
# Village CRUD
# -------------------------------
class VillageListView(ListView):
    model = Village
    template_name = 'vendormis/village/village_list.html'
    context_object_name = 'villages'

class VillageCreateView(CreateView):
    model = Village
    fields = ['name', 'traditional_authority']
    template_name = 'vendormis/village/village_form.html'
    success_url = reverse_lazy('vendormis:village_list')

class VillageUpdateView(UpdateView):
    model = Village
    fields = ['name', 'traditional_authority']
    template_name = 'vendormis/village/village_form.html'
    success_url = reverse_lazy('vendormis:village_list')

class VillageDeleteView(DeleteView):
    model = Village
    template_name = 'vendormis/village/village_confirm_delete.html'
    success_url = reverse_lazy('vendormis:village_list')
