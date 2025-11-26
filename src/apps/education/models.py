from django.contrib.auth import get_user_model
from django.db import models
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.snippets.models import register_snippet
from django_extensions.db.models import TimeStampedModel

from apps.core.utils import long_id
from apps.education.blocks import UnitStreamBlock

User = get_user_model()


CEFR = models.IntegerChoices("CEFR", "A1 A2 B1 B2 C1 C2")


@register_snippet
class Exercise(TimeStampedModel, Orderable):
    """Testu exercises.Exercise

    Removed fields: tags, reactions, searchable
    """

    CEFR = CEFR

    lid = models.CharField(
        "lid", unique=True, max_length=8, default=long_id, blank=True
    )
    name = models.CharField("name", max_length=100)
    description = models.TextField("description", blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    data = models.JSONField("data", default=dict, blank=True)
    lang_learn = models.BooleanField("about language", default=True)
    src_lang = models.CharField("source language", max_length=10, blank=True)
    lang_learn_lang = models.CharField("target language", max_length=10, blank=True)
    lang_learn_cefr_level_min = models.PositiveSmallIntegerField(
        "CEFR min",
        choices=CEFR.choices,
        null=True,
        blank=True,
    )
    lang_learn_cefr_level_max = models.PositiveSmallIntegerField(
        "CEFR max",
        choices=CEFR.choices,
        null=True,
        blank=True,
    )
    age_min = models.PositiveSmallIntegerField("minimum age", null=True, blank=True)
    age_max = models.PositiveSmallIntegerField("maximum age", null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["lid"], name="exercise_lid_idx"),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:
            while self.__class__.objects.filter(lid=self.lid).exists():
                self.lid = long_id()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/exercise/{self.lid}"


class ModulePage(Page):
    name = models.CharField(max_length=255)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    parent_page_types = ["home.HomePage"]
    content_panels = Page.content_panels + ["name", "image"]


class UnitPage(Page):
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(UnitStreamBlock(), blank=True, verbose_name="Content")

    parent_page_types = ["education.ModulePage"]
    subpage_types = []
    content_panels = Page.content_panels + ["name", "description", "image", "body"]
