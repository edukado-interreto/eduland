from django.db import models
from wagtail.admin.panels import MultiFieldPanel
from wagtail.blocks import RichTextBlock, StreamBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageBlock
from wagtail.models import Page

from apps.core.blocks import CallToActionBlock, HeadingBlock
from apps.core.utils import field_panels
from apps.education.blocks import ModuleBlock, PdfBlock


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
    hero_cta = StreamField([("button", CallToActionBlock(blank=True))])

    comics = StreamField([("pdf", PdfBlock())], blank=True)

    about = RichTextField(blank=True)

    parent_page_types = ["wagtailcore.Page"]  # under Root only
    content_panels = field_panels(
        [
            MultiFieldPanel(
                [f"hero_{f}" for f in ["image", "text", "cta"]],
                heading="Hero section",
            ),
            MultiFieldPanel(["comics"], heading="Content"),
            MultiFieldPanel(["about"], heading="Footer section"),
        ]
    )

    def module_pages(self):
        from apps.education.models import ModulePage

        return self.get_children().type(ModulePage).live()

    def methodology_pages(self):
        from apps.education.models import MethodologyPage

        """Only translated pages, so not aliases of original English page"""
        return (
            self.get_children()
            .live()
            .type(MethodologyPage)
            .filter(alias_of__isnull=True)
        )


class SimplePage(Page):
    content = RichTextField(blank=True)

    show_in_menus_default = True
    parent_page_types = ["home.HomePage"]
    content_panels = field_panels(["content"])


class NewsIndexPage(Page):
    header = RichTextField(blank=True)

    show_in_menus_default = True
    parent_page_types = ["home.HomePage"]
    content_panels = field_panels(["header"])


class NewsPost(Page):
    standfirst = models.TextField(default="")
    content = StreamField(
        {"text": RichTextBlock(), "image": ImageBlock()}.items(),
        blank=True,
    )

    parent_page_types = ["home.NewsIndexPage"]
    content_panels = field_panels(["standfirst", "content"])
