from wagtail.blocks import (
    PageChooserBlock,
    StructBlock,
    StreamBlock,
    RichTextBlock,
    URLBlock,
)
from wagtail.snippets.blocks import SnippetChooserBlock

from apps.core.blocks import VideoBlock


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
    exercise = SnippetChooserBlock("education.Exercise")
    testu = URLBlock(help_text="E.g.: https://www.testu.eu/exercise/i2E4S6T")
