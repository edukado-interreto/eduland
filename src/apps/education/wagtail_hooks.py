from django.http import HttpRequest
from django.urls import path

from wagtail import hooks
from wagtail.snippets.models import register_snippet

from apps.education.models import Exercise
from apps.education.views import ExerciseFormView, ExerciseViewSet


@hooks.register("register_admin_urls")
def register_exercise_list_url():
    return [
        path(
            "exercises/edit/<int:pk>/editor/",
            ExerciseFormView.as_view(),
            name="exercise_editor",
        ),
    ]


@hooks.register("after_create_snippet")
def fill_empty_field_on_exercise_snippet(request: HttpRequest, instance: Exercise):
    match instance:
        case Exercise(created_by_id=None) if request.user.is_authenticated:
            instance.created_by = request.user
            instance.save(update_fields=["created_by"])


register_snippet(ExerciseViewSet)
