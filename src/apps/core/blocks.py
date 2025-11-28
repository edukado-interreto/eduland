from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    PageChooserBlock,
    StructBlock,
)
from wagtail.embeds.blocks import EmbedBlock

url_validator = URLValidator()


def fragment_validator(value: str):
    if not value.startswith("#"):
        url_validator(value)


class HeadingBlock(StructBlock):
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(choices=[("h2", "H2"), ("h3", "H3"), ("h4", "H4")], default="h2")

    class Meta:
        icon = "title"
        template = "core/blocks/heading_block.html"


class VideoBlock(EmbedBlock):
    help_text = (
        "Insert an URL to embed. For example, https://www.youtube.com/watch?v=xm4qTLcXKc4",
    )
    icon = "media"
    max_width = 640
    max_height = 360


class CallToActionBlock(StructBlock):
    text = CharBlock(required=True, help_text="Text to display in the button")
    url = CharBlock(
        required=False,
        help_text="Anchor or link to another website page",
        validators=[fragment_validator],
    )
    page = PageChooserBlock(required=False, help_text="Link to a page")

    def clean(self, value):
        result = super().clean(value)
        if not (result["page"] or result["url"]):
            raise ValidationError(
                "You must specify either an internal page or an external URL"
            )
        return result
