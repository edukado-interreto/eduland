from django.db import models
from wagtail.admin.panels import MultiFieldPanel
from wagtail.blocks import StreamBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from apps.core.blocks import HeadingBlock
from apps.education.blocks import ModuleBlock


class ModuleStreamBlock(StreamBlock):
    title = HeadingBlock()
    module = ModuleBlock()


class HomePage(Page):
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Background image",
    )
    hero_text = RichTextField(blank=True)
    hero_cta = models.CharField(
        blank=True,
        verbose_name="Hero CTA",
        max_length=255,
        help_text="Text to display on Call to Action",
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA link",
        help_text="Choose a page to link to for the Call to Action",
    )

    modules = StreamField(ModuleStreamBlock(), blank=True, verbose_name="Modules")

    about = RichTextField(blank=True)

    parent_page_types = ["wagtailcore.Page"]  # under Root only
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [f"hero_{f}" for f in ["image", "text", "cta", "cta_link"]],
            heading="Hero section",
        ),
        MultiFieldPanel(["modules"], heading="Content section"),
        MultiFieldPanel(["about"], heading="Footer section"),
    ]
