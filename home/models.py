from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.snippets.models import register_snippet
from wagtail.images import get_image_model_string
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils import timezone


@register_snippet
class Menu(ClusterableModel):
    title = models.CharField(
        max_length=100,
        help_text="Menu name e.g. Main Menu"
    )

    panels = [
        FieldPanel("title"),
        InlinePanel("items", label="Menu items"),
    ]

    def __str__(self):
        return self.title

class MenuItem(Orderable):
    menu = ParentalKey(
        Menu,
        related_name="items",
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100)

    link_page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    external_url = models.URLField(
        blank=True,
        help_text="Optional external link"
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
        help_text="Select a parent to make this a submenu item"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("link_page"),
        FieldPanel("external_url"),
        FieldPanel("parent"),
    ]

    def url(self):
        if self.link_page:
            return self.link_page.url
        return self.external_url

    def __str__(self):
        return self.title


# -----------------------------
# Site Branding (Settings)
# -----------------------------
@register_setting
class SiteBranding(BaseSiteSetting):
    site_logo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    site_tagline = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('site_logo'),
        FieldPanel('site_tagline'),
    ]

    def __str__(self):
        return "Site Branding"


# -----------------------------
# Trustee Snippet
# -----------------------------
@register_snippet
class TrusteeMember(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    photo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    bio = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('position'),
        FieldPanel('photo'),
        FieldPanel('bio'),
        FieldPanel('linkedin'),
        FieldPanel('facebook'),
        FieldPanel('twitter'),
        FieldPanel('whatsapp'),
        FieldPanel('email'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Trustee Member"
        verbose_name_plural = "Board of Trustees"


# -----------------------------
# Staff Snippet
# -----------------------------
@register_snippet
class StaffMember(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    photo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    bio = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('position'),
        FieldPanel('photo'),
        FieldPanel('bio'),
        FieldPanel('linkedin'),
        FieldPanel('facebook'),
        FieldPanel('twitter'),
        FieldPanel('whatsapp'),
        FieldPanel('email'),
    ]

    def __str__(self):
        return self.name

# -----------------------------
# Our Staff Page
# -----------------------------
@register_snippet
class OurStaffPage(Page):
    intro = models.TextField(blank=True)
    staff = ParentalManyToManyField('StaffMember', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('staff'),
    ]

# -----------------------------
# Our Partners Snippet
# -----------------------------
@register_snippet
class Partner(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('logo'),
        FieldPanel('website'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.name

# -----------------------------
# Project Snippet
# -----------------------------
@register_snippet
class Project(ClusterableModel):
    title = models.CharField(max_length=255)
    description = RichTextField(blank=True)
    date = models.DateField(null=True, blank=True)
    
    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('date'),
        InlinePanel('images', label="Project Images"),
    ]

    def __str__(self):
        return self.title

class ProjectImage(Orderable):
    project = ParentalKey('Project', on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.CASCADE,
        related_name='+'
    )
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

# -----------------------------
# Program / Project Snippet
# -----------------------------
@register_snippet
class Program(ClusterableModel):
    title = models.CharField(max_length=255)
    description = RichTextField(blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        InlinePanel('images', label="Program Images"),
    ]

    def __str__(self):
        return self.title

# -----------------------------
# Program Images (Inline)
# -----------------------------
class ProgramImage(Orderable):
    program = ParentalKey('Program', on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.CASCADE,
        related_name='+'
    )
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


# The model to hold the individual slides
class HomePageSlider(Orderable):
    page = ParentalKey('HomePage', on_delete=models.CASCADE, related_name='slider_images')
    image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.CASCADE,
        related_name='+'
    )

# -----------------------------
# Home Page
# -----------------------------
class HomePage(Page):
    hero_title = models.CharField(max_length=255, blank=True, null=True)
    hero_subtitle = models.TextField(blank=True, null=True)
    hero_image = models.ForeignKey(
        get_image_model_string(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    hero_button_text = models.CharField(max_length=50, blank=True, null=True)
    hero_button_link = models.URLField(blank=True, null=True)

    about_title = models.CharField(max_length=255, default="About Us")
    about_text = RichTextField(blank=True)

    mission = RichTextField(blank=True, null=True)
    vision = RichTextField(blank=True, null=True)
    values = RichTextField(blank=True, null=True)
    

    key_programs = StreamField([
        ('program', blocks.CharBlock(required=True, max_length=255))
    ], blank=True)

    vendor_app_url = models.URLField(
        blank=True,
        help_text="Link to the Vendor MIS application"
    )

    partners = ParentalManyToManyField(
        'Partner',
        blank=True,
        help_text="Select partners to display on the homepage"
    )

    content_panels = Page.content_panels + [
        FieldPanel('hero_title'),
        FieldPanel('hero_subtitle'),
        FieldPanel('hero_button_text'),
        FieldPanel('hero_button_link'),
        FieldPanel('hero_image'),
        FieldPanel('about_title'),
        FieldPanel('about_text'),
        FieldPanel('mission'),
        FieldPanel('vision'),
        FieldPanel('values'),
        FieldPanel('key_programs'),
        FieldPanel('vendor_app_url'),
        FieldPanel('partners'),
        InlinePanel('slider_images', label="Hero Slider Images"),
    ]

    def get_context(self, request):
            context = super().get_context(request)
            context['programs'] = Program.objects.all()
            context['staff_members'] = StaffMember.objects.all()
            context['projects'] = Project.objects.all()
            context['trustee_members'] = TrusteeMember.objects.all()
            context['vacancies'] = Vacancy.objects.filter(is_open=True).order_by('-deadline')
            context['about_page_content'] = AboutPage.objects.live().first()
            context['partners'] = Partner.objects.all()
            context['today'] = timezone.now().date()
            return context
    
    def serve(self, request, *args, **kwargs):
        if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            name = request.POST.get('name')
            user_email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            recipient_email = request.POST.get('recipient_email', 'chiccochikaonda@gmail.com')

            full_body = f"Message from: {name} ({user_email})\n\n{message}"

            try:
                send_mail(
                    subject=f"[Contact Form] {subject}",
                    message=full_body,
                    from_email=None, # Uses DEFAULT_FROM_EMAIL config
                    recipient_list=[recipient_email],
                    fail_silently=False,
                )
                return JsonResponse({'status': 'success'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

        return super().serve(request, *args, **kwargs)
    
# -----------------------------
# About Page
# -----------------------------
class AboutPage(Page):
    introduction = RichTextField(blank=True)
    what_we_do = RichTextField(blank=True)
    # Add the image field
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        FieldPanel('what_we_do'),
        FieldPanel('image'), # Add this to the panels
    ]
# -----------------------------
# Program Page
# -----------------------------
class ProgramPage(Page):
    intro = RichTextField(blank=True)
    programs = ParentalManyToManyField('Program', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('programs'),
    ]

# -----------------------------
# News Page
# -----------------------------
class NewsPage(Page):
    body = RichTextField(blank=True)
    publication_date = models.DateField()

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('publication_date'),
    ]

# -----------------------------
# Vacancies Page
# -----------------------------
class VacanciesIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        InlinePanel('vacancies', label='Vacancies'),
    ]

    subpage_types = []  # prevent child pages
    def get_context(self, request):
        context = super().get_context(request)
        # This gets all live children of this page
        context['vacancies'] = self.vacancies.all()
        return context

class Vacancy(Orderable): # Change models.Model to Orderable
    page = ParentalKey(
        'VacanciesIndexPage', 
        related_name='vacancies', 
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = RichTextField()
    location = models.CharField(max_length=255, blank=True)
    deadline = models.DateField()
    is_open = models.BooleanField(default=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('location'),
        FieldPanel('deadline'),
        FieldPanel('is_open'),
    ]

    def __str__(self):
        return self.title

# -----------------------------
# Contact Page
# -----------------------------
class ContactUsPage(Page):
    body = RichTextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel('email'),
        FieldPanel('phone'),
        FieldPanel('address'),
    ]

# -----------------------------
# Donate Page
# -----------------------------
class DonatePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
