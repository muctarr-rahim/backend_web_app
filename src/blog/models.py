from django.db import models

# Create your models here.

from datetime import date

from django.db.models import (
    CharField,
    DateField,
    ManyToManyField,
    Model,
    SlugField,
    TextField,
)
from django.urls import reverse

from organiser.models import Startup, Tag


class Post(Model):
    """Blog post; news article about startups"""

    title = CharField(max_length=63)
    slug = SlugField(
        max_length=63,
        help_text="A label for URL config",
        unique_for_month="pub_date",
    )
    text = TextField()
    pub_date = DateField(
        "date published", default=date.today
    )
    tags = ManyToManyField(Tag, related_name="blog_posts")
    startups = ManyToManyField(
        Startup, related_name="blog_posts"
    )

    class Meta:
        get_latest_by = "pub_date"
        ordering = ["-pub_date", "title"]
        verbose_name = "blog post"

    def __str__(self):
        date_string = self.pub_date.strftime("%Y-%m-%d")
        return f"{self.title} on {date_string}"

    def get_absolute_url(self):
        """Return URL to detail page of Post"""
        return reverse(
            "post_detail",
            kwargs={
                "year": self.pub_date.year,
                "month": self.pub_date.month,
                "slug": self.slug,
            },
        )

    def get_update_url(self):
        """Return URL to update page of Post"""
        return reverse(
            "post_update",
            kwargs={
                "year": self.pub_date.year,
                "month": self.pub_date.month,
                "slug": self.slug,
            },
        )

    def get_delete_url(self):
        """Return URL to delete page of Post"""
        return reverse(
            "post_delete",
            kwargs={
                "year": self.pub_date.year,
                "month": self.pub_date.month,
                "slug": self.slug,
            },
        )