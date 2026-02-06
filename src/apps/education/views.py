from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    ObjectList,
    TabbedInterface,
    PanelGroup,
)
from wagtail.admin.ui.tables import UpdatedAtColumn, UserColumn
from wagtail.snippets.views.snippets import CreateView, SnippetViewSet
from apps.education.models import Exercise


def wagtail_sidebar(response, collapsed):
    response.set_cookie("wagtail_sidebar_collapsed", int(collapsed), samesite="Lax")
    return response


class ExerciseCreateView(CreateView):
    def get_success_url(self):
        """Redirect to the Editor if the exercise data is empty"""
        if self.object.has_empty_data:
            return reverse_lazy("exercise_editor", kwargs={"pk": self.object.pk})
        return super().get_success_url()


class ExerciseFormView(UpdateView):
    model = Exercise
    template_name = "education/exercise_editor.html"
    fields = ["data"]

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(), **{"submit_button_label": "Save"}}

    def get(self, request, *args, **kwargs):
        return wagtail_sidebar(super().get(request, *args, **kwargs), collapsed=True)

    def form_valid(self, form):
        return wagtail_sidebar(super().form_valid(form), collapsed=False)


class ExerciseViewSet(SnippetViewSet):
    model = Exercise
    icon = "tick-inverse"
    menu_label = "Exercises"
    menu_name = "exercise"
    url_prefix = "exercises"
    edit_template_name = "education/exercise_admin_form.html"
    list_filter = ["src_lang", "lang_learn_lang"]
    list_display = [
        "name",
        "title",
        "language",
        "teaching",
        UserColumn("created_by"),
        UpdatedAtColumn(),
    ]
    list_per_page = 100
    inspect_view_enabled = True
    add_to_admin_menu = True
    add_view_class = ExerciseCreateView
    exclude_form_fields = ["lid", "created_by", "lang_learn"]
    edit_handler: PanelGroup = TabbedInterface(
        [
            ObjectList(
                [
                    ObjectList(
                        [
                            FieldPanel("name"),
                            FieldPanel("title"),
                            FieldPanel("description"),
                        ]
                    ),
                    FieldRowPanel(
                        [
                            FieldPanel("src_lang"),
                            FieldPanel("lang_learn_lang"),
                            FieldPanel("lang_learn_cefr_level_min"),
                            FieldPanel("lang_learn_cefr_level_max"),
                        ],
                        heading="Languages",
                    ),
                    FieldRowPanel(
                        [FieldPanel("age_min"), FieldPanel("age_max")],
                        heading="Best for",
                    ),
                ],
                heading="Basic information",
            ),
            ObjectList([FieldPanel("data", read_only=True)], heading="Raw data"),
        ]
    )
