from django.http import HttpRequest
from wagtail import hooks
from wagtail.snippets.models import register_snippet

from apps.education.models import Exercise
from apps.education.views import ExerciseViewSet


@hooks.register("after_create_snippet")
def add_user_to_exercise_snippet(request: HttpRequest, instance: Exercise):
    if isinstance(instance, Exercise):
        if not instance.created_by:
            if request.user.is_authenticated:
                instance.created_by = request.user
                instance.save()


register_snippet(ExerciseViewSet)
