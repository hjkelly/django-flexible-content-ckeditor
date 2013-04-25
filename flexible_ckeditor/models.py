from django.db import models
from django.utils.translation import ugettext as _

from flexible_content.models import BaseItem

from .fields import CKEditorField


class CKEditorText(BaseItem):
    html = CKEditorField()

    class FlexibleContentInfo:
        description = _("Add text that's saved as HTML, which supports "
                        "basic formatting.")
        name = "Text"
        type_slug = 'ckeditor-text'

    class Meta:
        verbose_name = _("Text")
