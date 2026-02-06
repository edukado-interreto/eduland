import json

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from django_extensions.db.models import TimeStampedModel
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index

from apps.core.utils import long_id
from apps.education.blocks import ExerciseBlock, UnitStreamBlock

User = get_user_model()

CEFR = models.IntegerChoices("CEFR", "A1 A2 B1 B2 C1 C2")
AGES = [(i, str(i)) for i in range(18)] + [(18, "18+")]


def display_language(code: str) -> str:
    return dict(settings.LANGUAGES).get(code, "N/A")


def empty_data():
    return {"sheet": list()}


class Exercise(TimeStampedModel, index.Indexed, Orderable):
    """Testu exercises.Exercise

    Removed fields: tags, reactions, searchable
    """

    CEFR = CEFR

    lid = models.CharField(
        "lid", unique=True, max_length=8, default=long_id, blank=True
    )
    name = models.CharField("name", max_length=100)
    title = models.CharField(
        "title",
        help_text="The users will only see this name",
        max_length=100,
        blank=True,
    )
    description = models.TextField("description", blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    data = models.JSONField("data", default=empty_data, blank=True)
    lang_learn = models.BooleanField("about language", default=True)
    src_lang = models.CharField(
        "source language", choices=settings.LANGUAGES, max_length=10, blank=True
    )
    lang_learn_lang = models.CharField(
        "target language", choices=settings.LANGUAGES, max_length=10, blank=True
    )
    lang_learn_cefr_level_min = models.PositiveSmallIntegerField(
        "CEFR min",
        choices=CEFR.choices,
        default=CEFR.A1,
        null=True,
        blank=True,
    )
    lang_learn_cefr_level_max = models.PositiveSmallIntegerField(
        "CEFR max",
        choices=CEFR.choices,
        default=CEFR.C2,
        null=True,
        blank=True,
    )
    age_min = models.PositiveSmallIntegerField("minimum age", choices=AGES, default=0)
    age_max = models.PositiveSmallIntegerField("maximum age", choices=AGES, default=18)

    class Meta:
        indexes = [
            models.Index(fields=["lid"], name="exercise_lid_idx"),
        ]

    search_fields = [
        index.SearchField("name"),
        index.SearchField("title"),
        index.AutocompleteField("name"),
        index.AutocompleteField("title"),
    ]

    def __str__(self):
        fields = (self.name, self.language, self.title)
        return " • ".join(f for f in fields if f)

    @property
    @admin.display(ordering="src_lang")
    def language(self):
        return display_language(self.src_lang)

    @property
    @admin.display(ordering="lang_learn_lang")
    def teaching(self):
        return display_language(self.lang_learn_lang)

    def get_absolute_url(self):
        return reverse_lazy(
            "wagtailsnippets_education_exercise:edit", kwargs={"pk": self.pk}
        )

    def save(self, *args, **kwargs):
        if self._state.adding:
            while self.__class__.objects.filter(lid=self.lid).exists():
                self.lid = long_id()
        return super().save(*args, **kwargs)

    @property
    def has_empty_data(self):
        try:
            self.object.data["sheet"][0]
        except AttributeError, IndexError:
            return True
        return False


class ModulePage(Page):
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    parent_page_types = ["home.HomePage"]
    content_panels = Page.content_panels + ["image"]


class UnitPage(Page):
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(UnitStreamBlock(), blank=True, verbose_name="Content")

    parent_page_types = ["education.ModulePage"]
    subpage_types = ["education.ExercisePage"]
    content_panels = Page.content_panels + ["image", "body"]


class ExercisePage(Page):
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_NULL, null=True)

    parent_page_types = ["education.UnitPage"]
    subpage_types = []
    content_panels = Page.content_panels + ["exercise"]
