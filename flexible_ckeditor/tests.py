from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.unittest import skip

from mock_project.myapp.models import BlogPost

from .fields import CKEditorField, CKEditorFormField
from .models import CKEditorText

# Define a couple scenarios for INSTALLED_APPS.
INSTALLED_APPS__WITH_SITES = (settings.INSTALLED_APPS +
                              ('django.contrib.sites',))
INSTALLED_APPS__WITHOUT_SITES = [a for a in settings.INSTALLED_APPS
                                 if a!='django.contrib.sites']

# Define a couple scenarios for FLEXIBLE_CONTENT as well.
_ITEM_TYPES = (
    'flexible_ckeditor.CKEditorText',
    'default_item_types.Image',
)
FLEXIBLE_CONTENT__NO_DOMAIN = {
    'ITEM_TYPES': _ITEM_TYPES,
}
FLEXIBLE_CONTENT__WITH_SITE_DOMAIN = {
    'ITEM_TYPES': _ITEM_TYPES,
    'ckeditor': {
        'site_domain': 'www.mydomain.com',
    },
}
FLEXIBLE_CONTENT__NO_DOMAIN_CLEAN = {
    'ITEM_TYPES': _ITEM_TYPES,
    'ckeditor': {
        'clean_domains': False,
    },
}


class ModelFieldUnitTest(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        # Store the only post here on the testcase instance.
        self.post = BlogPost.objects.get(pk=1)
        self.ckeditor_value = self.post.items[1].html
        # Store the CKEditorField as well.
        self.model_field = (self.post.items[1]._meta.
                            get_field_by_name('html')[0])

    def test_formfield(self):
        """
        Given the field on the model, we should be able to get our formfield.
        """
        self.assertIsInstance(self.model_field.formfield(), CKEditorFormField)

    @override_settings(INSTALLED_APPS=INSTALLED_APPS__WITH_SITES)
    def test_get_forbidden_domains__sites(self):
        """
        Make sure that we can get forbidden domains from the Sites framework.
        """
        self.assertEqual(set(self.model_field.get_forbidden_domains()),
                         set(['mydomain.com', 'dev.mydomain.com']))

    @override_settings(INSTALLED_APPS=INSTALLED_APPS__WITHOUT_SITES,
                       FLEXIBLE_CONTENT=FLEXIBLE_CONTENT__WITH_SITE_DOMAIN)
    def test_get_forbidden_domains__settings(self):
        """
        Make sure that we can get forbidden domains from FLEXIBLE_CONTENT
        settings.
        """
        self.assertEqual(set(self.model_field.get_forbidden_domains()),
                         set(['mydomain.com']))

    @override_settings(INSTALLED_APPS=INSTALLED_APPS__WITHOUT_SITES,
                       FLEXIBLE_CONTENT=FLEXIBLE_CONTENT__NO_DOMAIN)
    def test_get_forbidden_domains__none(self):
        """
        Ensure that, with no sites and no FLEXIBLE_CONTENT domain setting,
        we don't forbid any domains.
        """
        self.assertEqual(len(self.model_field.get_forbidden_domains()), 0)

    @override_settings(INSTALLED_APPS=INSTALLED_APPS__WITH_SITES)
    def test_get_domain_agnostic_value(self):
        """
        For a given list of domains, ensure they're removed from the HTML.
        """
        # Get the Site domains. There should be two of them - the production
        # and dev.
        forbidden_domains = self.model_field.get_forbidden_domains()
        self.assertEqual(len(forbidden_domains), 2)

        # Get the domain agnostic version of the string and make sure it doesn't contain the forbidden domains.
        clean_value = (self.model_field.
                       get_domain_agnostic_value(self.ckeditor_value,
                                                 forbidden_domains))
        for d in forbidden_domains:
            self.assertNotIn(d, clean_value,
                             msg="Found {domain} in what was supposed to be "
                             "the domain-agnostic/cleaned HTML.".
                             format(domain=d))

        # Ensure the safe domain is still in there.
        self.assertIn('externaldomain.com', clean_value,
                      msg="An external domain was also stripped out of the "
                      "domain-agnostic/cleaned HTML!")

    @override_settings(INSTALLED_APPS=INSTALLED_APPS__WITH_SITES)
    def test_clean__from_sites(self):
        """
        When we do find sites, ensure they're properly removed.
        """
        clean_value = self.model_field.clean(self.ckeditor_value, self.post)
        self.assertNotIn('dev.mydomain.com', clean_value)

    @override_settings(INSTALLED_APPS=INSTALLED_APPS__WITH_SITES,
                       FLEXIBLE_CONTENT=FLEXIBLE_CONTENT__NO_DOMAIN_CLEAN)
    def test_clean__when_clean_domains_disabled(self):
        """
        When they have domain cleaning disabled, ensure we honor that.
        """
        clean_value = self.model_field.clean(self.ckeditor_value, self.post)
        self.assertIn('dev.mydomain.com', clean_value)


class FormFieldUnitTest(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        # Store the only post here on the testcase instance.
        self.post = BlogPost.objects.get(pk=1)
        self.ckeditor_value = self.post.items[1].html
        # Store the CKEditorField as well.
        self.model_field = (self.post.items[1]._meta.
                            get_field_by_name('html')[0])

    def test_render(self):
        widget = self.model_field.formfield().widget
        rendered_widget = widget.render('test_field_name')
        # Make sure the Javascript shows.
        self.assertIn('script', rendered_widget)
        self.assertIn('CKEDITOR', rendered_widget)
        # Make sure we have the test field name.
        self.assertIn('test_field_name', rendered_widget)
