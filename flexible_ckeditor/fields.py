from django.conf import settings
from django.db.models.fields import Field, TextField
from django.forms.fields import CharField

from .widgets import CKEditorWidget


class CKEditorFormField(CharField):
    widget = CKEditorWidget


class CKEditorField(TextField):
    def formfield(self, **kwargs):
        """
        Ensure that the form field is our CKEditor one.
        """
        kwargs['form_class'] = CKEditorFormField
        return super(CKEditorFormField, self).formfield(**kwargs)

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
            cleaned_value = self.get_value_without_domains(value,
                                                           forbidden_domains)
        return cleaned_value

    def get_forbidden_domains(self):
        """
        Based on the project's configuration, figure out what domains shouldn't
        be allowed as fully-qualified URLs.
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
        return forbidden_domains

    def get_value_without_domains(self, value, domains):
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