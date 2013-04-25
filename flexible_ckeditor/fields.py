import re

from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.fields import Field, TextField
from django.forms.fields import CharField

from .widgets import CKEditorWidget


class CKEditorFormField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = CKEditorWidget
        super(CKEditorFormField, self).__init__(*args, **kwargs)


class CKEditorField(TextField):
    def formfield(self, **kwargs):
        """
        Ensure that the form field is our CKEditor one.
        """
        kwargs['form_class'] = CKEditorFormField
        return super(CKEditorField, self).formfield(**kwargs)

    def clean(self, value, model_instance):
        """
        Prevent the site's domain from being stored in the database, so that
        it's portable between different environments.
        """
        # Check their config for a preference on whether or not their domains
        # are cleaned... default to True.
        try:
            clean_domains = (settings.FLEXIBLE_CONTENT['ckeditor']
                             ['clean_domains'])
        except (AttributeError, KeyError):
            clean_domains = True

        if clean_domains:
            # Find out what domains we shouldn't allow.
            forbidden_domains = self.get_forbidden_domains()
            # Remove them and store the cleaned contents of the field.
            value = self.get_domain_agnostic_value(value, forbidden_domains)
        return value

    def get_forbidden_domains(self):
        """
        Based on the project's configuration, figure out what domains shouldn't
        be allowed as fully-qualified URLs. Strip off the 'www.' prefix if it
        has it.
        """
        forbidden_domains = []

        # Are they using Django's sites framework?
        if 'django.contrib.sites' in settings.INSTALLED_APPS:
            # Make note of all the domains in the database.
            forbidden_domains = [s.domain for s in Site.objects.all()]
        # Otherwise, check the config for this app.
        else:
            try:
                site_domain = (settings.
                               FLEXIBLE_CONTENT['ckeditor']['site_domain'])
            except (AttributeError, KeyError):
                pass
            else:
                forbidden_domains = [site_domain]

        # Strip leading 'www.' if it has one.
        cleaned_forbidden_domains = []
        for f in forbidden_domains:
            if f.startswith('www.'):
                f = f[4:]
            cleaned_forbidden_domains.append(f)

        return cleaned_forbidden_domains

    def get_domain_agnostic_value(self, value, domains):
        """
        For the given HTML, remove fully-qualified references to one or more
        domains.
        """
        # Don't allow src or href attributes to contain fully-qualified URLs
        # to those domains
        pattern_template = r'(?P<attr>(src|href))=(?P<quotechar>("|\'))(https?:)?//(www.)?%s(:\d+)?/?'

        # Loop through each domain and remove references to it.
        for domain in domains:
            value = re.sub(pattern_template % domain,
                           '\g<attr>=\g<quotechar>/', unicode(value))
        return value
