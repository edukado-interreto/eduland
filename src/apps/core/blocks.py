from wagtail.blocks import StructBlock, CharBlock, ChoiceBlock
from wagtail.embeds.blocks import EmbedBlock


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
