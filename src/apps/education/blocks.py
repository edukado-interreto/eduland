from django.core.exceptions import ValidationError
from wagtail.blocks import (
    CharBlock,
    PageChooserBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    URLBlock,
)
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from apps.core.blocks import VideoBlock


class PdfBlock(StructBlock):
    title = CharBlock()
    text = CharBlock()
    image = ImageBlock()
    pdf = DocumentChooserBlock()

    class Meta:
        icon = "doc-full-inverse"
        template = "education/blocks/pdf_block.html"


class ModuleBlock(StructBlock):
    module_page = PageChooserBlock(
        page_type="education.ModulePage", verbose_name="Module"
    )

    class Meta:
        icon = "table"
        template = "education/blocks/module_block.html"


class UnitStreamBlock(StreamBlock):
    text = RichTextBlock()
    video = VideoBlock()
    pdf = DocumentChooserBlock()


class ExerciseBlock(StructBlock):
    exercise = SnippetChooserBlock(
        "education.Exercise",
        required=False,
    )
    testu_link = URLBlock(
        help_text="E.g.: https://www.testu.eu/exercise/i2e4s6t",
        required=False,
    )

    def clean(self, value):
        result = super().clean(value)
        snippet, link = result["exercise"], result["testu_link"]
        if not (snippet or link):
            raise ValidationError("An Exercise snippet or a Testu link is required")
        if snippet and link:
            raise ValidationError(
                "Only one Exercise snippet OR a Testu link is accepted"
            )
        return result
