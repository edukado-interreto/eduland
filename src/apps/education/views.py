from wagtail.admin.ui.tables import UpdatedAtColumn, UserColumn
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.admin.viewsets.model import ModelViewSet

from apps.education.models import Exercise


class ExerciseViewSet(SnippetViewSet):
    model = Exercise
    icon = "tick-inverse"
    menu_label = "Exercises"
    menu_name = "exercise"
    url_prefix = "exercises"
    list_filter = ["src_lang"]
    list_display = ["name", "language", UserColumn("created_by"), UpdatedAtColumn()]
    list_per_page = 100
    add_to_admin_menu = True
    exclude_form_fields = ["lid", "created_by", "lang_learn"]
