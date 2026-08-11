from django.urls import path
from . import views

from .views import (
    VendorDeleteView,
    VendorLoginView,
    VendorDetailView,
    VendorLogoutView,
    VendorDashboardView,
    VendorListView,
    VendorRegistrationWizard,
    VendorIndexView,
    OfficerDashboardView,
    AdminDashboardView,
    VendorUpdateView,

)

app_name = "vendormis"

urlpatterns = [

    # =====================================================
    # AUTH / LANDING
    # =====================================================
    path("", VendorIndexView.as_view(), name="vendor_index"),
    path("login/", VendorLoginView.as_view(), name="vendor_login"),
    path("logout/", VendorLogoutView.as_view(next_page="/vendormis/login/"), name="vendor_logout"),

    # Registration (Multi-step Wizard)
    path("register/", VendorRegistrationWizard.as_view(), name="vendor_register"),

    # =====================================================
    # VENDOR CRUD
    # =====================================================
    path("vendors/", VendorListView.as_view(), name="vendor_list"),
    path("vendors/<int:pk>/", VendorDetailView.as_view(), name="vendor_detail"),
    path("vendors/<int:pk>/update/", VendorUpdateView.as_view(), name="vendor_update"),
    path("vendors/<int:pk>/delete/", VendorDeleteView.as_view(), name="vendor_delete"),

    # =====================================================
    # DASHBOARDS
    # =====================================================
    path("vendor/dashboard/", VendorDashboardView.as_view(), name="vendor_dashboard"),
    path("officer/dashboard/", OfficerDashboardView.as_view(), name="officer_dashboard"),
    path("admin/dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),

    # =====================================================
    # NATION CRUD
    # =====================================================
    path("nations/", views.NationListView.as_view(), name="nation_list"),
    path("nations/add/", views.NationCreateView.as_view(), name="nation_create"),
    path("nations/<int:pk>/edit/", views.NationUpdateView.as_view(), name="nation_update"),
    path("nations/<int:pk>/delete/", views.NationDeleteView.as_view(), name="nation_delete"),

    # =====================================================
    # DISTRICT CRUD
    # =====================================================
    path("districts/", views.DistrictListView.as_view(), name="district_list"),
    path("districts/add/", views.DistrictCreateView.as_view(), name="district_create"),
    path("districts/<int:pk>/edit/", views.DistrictUpdateView.as_view(), name="district_update"),
    path("districts/<int:pk>/delete/", views.DistrictDeleteView.as_view(), name="district_delete"),

    # =====================================================
    # TRADITIONAL AUTHORITY CRUD
    # =====================================================
    path("authorities/", views.TraditionalAuthorityListView.as_view(), name="ta_list"),
    path("authorities/add/", views.TraditionalAuthorityCreateView.as_view(), name="ta_create"),
    path("authorities/<int:pk>/edit/", views.TraditionalAuthorityUpdateView.as_view(), name="ta_update"),
    path("authorities/<int:pk>/delete/", views.TraditionalAuthorityDeleteView.as_view(), name="ta_delete"),

    # =====================================================
    # VILLAGE CRUD
    # =====================================================
    path("villages/", views.VillageListView.as_view(), name="village_list"),
    path("villages/add/", views.VillageCreateView.as_view(), name="village_create"),
    path("villages/<int:pk>/edit/", views.VillageUpdateView.as_view(), name="village_update"),
    path("villages/<int:pk>/delete/", views.VillageDeleteView.as_view(), name="village_delete"),


]