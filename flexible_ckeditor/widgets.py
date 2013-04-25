from django.conf import settings
from django.forms.util import flatatt
from django.forms.widgets import Textarea
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class CKEditorWidget(Textarea):
    def render(self, name, value=None, attrs=None):
        """
        Generate the markup for the HTML editor.
        """
        
        # If the value wasn't specified in the calls that led to this render(),
        # set a blank string.
        if value is None: value = ''
        # Set attributes how we want them, so we can call out all the relevant
        # text areas.
        if attrs is None:
            attrs = {}
        attrs.update({'class': 'replace-with-ckeditor'})
        # Build the final attributes.
        final_attrs = self.build_attrs(attrs, name=name)
        
        return mark_safe(render_to_string(
            'flexible_ckeditor/widget.html',
            {
                'content': value,
                'attrs': final_attrs,
                'attr_string': flatatt(final_attrs),
            }
        ))
