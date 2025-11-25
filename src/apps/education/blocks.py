from wagtail.blocks import PageChooserBlock, StructBlock


class ModuleBlock(StructBlock):
    module_page = PageChooserBlock(
        page_type="education.ModulePage", verbose_name="Module"
    )

    class Meta:
        icon = "table"
        template = "education/blocks/module_block.html"
