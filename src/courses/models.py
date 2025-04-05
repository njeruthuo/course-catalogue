from django.db import models


class PublishStatus(models.TextChoices):
    PUBLISHED = "pub", "Published"
    DRAFT = 'draft', "Draft"
    COMING_SOON = 'soon', "Coming soon"


class AccessRequirement(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED = 'email_required', "Email required"


class Course(models.Model):
    title = models.CharField(max_length=120)
    descriptions = models.TextField(blank=True, null=True)
    # publish_date =
    # image = models.
    access = models.CharField(
        max_length=20, choices=AccessRequirement.choices, default=AccessRequirement.EMAIL_REQUIRED)
    status = models.CharField(
        max_length=20, choices=PublishStatus.choices, default=PublishStatus.DRAFT)

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED
