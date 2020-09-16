from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Ptype


@receiver(pre_save,
          sender=Ptype,
          dispatch_uid="generate_ptype_slug")
def generate_ptype_slug(sender, instance, **kwargs):
    """Set slug based on title"""
    slug = slugify(instance.title, allow_unicode=True)

    # To ensure that slug is unique in case of non-unique titles
    unique_slug = slug
    suffix = 1
    while Ptype.objects.filter(slug=unique_slug).exclude(pk=instance.pk):
        unique_slug = "%s-%s" % (slug, suffix)
        suffix += 1
    instance.slug = unique_slug