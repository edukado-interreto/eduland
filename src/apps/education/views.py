import calendar

from django.shortcuts import render
from django.utils import timezone
from django.views.generic import FormView, ListView
from django.views.generic.edit import UpdateView
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
    ObjectList,
    PanelGroup,
    TabbedInterface,
)
from wagtail.admin.ui.tables import UpdatedAtColumn, UserColumn
from wagtail.snippets.views.snippets import SnippetViewSet

from apps.education.models import Exercise


class ExerciseFormView(UpdateView):
    model = Exercise
    template_name = "education/exercise_editor.html"
    fields = ["data"]

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(), **{"submit_button_label": "Save"}}


class ExerciseViewSet(SnippetViewSet):
    model = Exercise
    icon = "tick-inverse"
    menu_label = "Exercises"
    menu_name = "exercise"
    url_prefix = "exercises"
    edit_template_name = "education/exercise_admin_form.html"
    list_filter = ["src_lang"]
    list_display = ["name", "language", UserColumn("created_by"), UpdatedAtColumn()]
    list_per_page = 100
    inspect_view_enabled = True
    add_to_admin_menu = True
    exclude_form_fields = ["lid", "created_by", "lang_learn"]
    edit_handler: PanelGroup = TabbedInterface(
        [
            FieldRowPanel(
                [
                    ObjectList(
                        [
                            FieldPanel("lid"),
                            FieldPanel("name"),
                            FieldPanel("description"),
                            FieldPanel("created_by"),
                        ],
                    ),
                    ObjectList(
                        [
                            FieldPanel("src_lang"),
                            FieldPanel("lang_learn_lang"),
                            FieldPanel("lang_learn_cefr_level_min"),
                            FieldPanel("lang_learn_cefr_level_max"),
                        ],
                    ),
                    ObjectList(
                        [FieldPanel("age_min"), FieldPanel("age_max")],
                    ),
                ],
                heading="Basic information",
            ),
            ObjectList([FieldPanel("data")], heading="Raw Data"),
        ]
    )
