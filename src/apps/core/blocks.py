from wagtail.blocks import StructBlock, CharBlock, ChoiceBlock


class HeadingBlock(StructBlock):
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(choices=[("h2", "H2"), ("h3", "H3"), ("h4", "H4")], default="h2")

    class Meta:
        icon = "title"
        template = "core/blocks/heading_block.html"
