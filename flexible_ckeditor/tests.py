from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.unittest import skip

from mock_project.myapp.models import BlogPost

from .fields import CKEditorField, CKEditorFormField
from .models import CKEditorText

# Define a couple scenarios for INSTALLED_APPS.
INSTALLED_APPS_WITH_SITES = settings.INSTALLED_APPS + ('django.contrib.sites',)
INSTALLED_APPS_WITHOUT_SITES = [a for a in settings.INSTALLED_APPS
                                if a!='django.contrib.sites']

# Define a couple scenarios for FLEXIBLE_CONTENT as well.
_ITEM_TYPES = (
    'flexible_ckeditor.CKEditorText',
    'default_item_types.Image',
)
FLEXIBLE_CONTENT_NO_DOMAIN = {
    'ITEM_TYPES': _ITEM_TYPES,
}
FLEXIBLE_CONTENT_WITH_SITE_DOMAIN = {
    'ITEM_TYPES': _ITEM_TYPES,
    'ckeditor': {
        'site_domain': 'www.mydomain.com',
    },
}
FLEXIBLE_CONTENT_WITH_DOMAIN_CLEAN_DISABLED = {
    'ITEM_TYPES': _ITEM_TYPES,
    'ckeditor': {
        'site_domain': 'localhost:8000',
        'clean_domains': False,
    },
}


class ModelFieldUnitTest(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        # Store the only post here on the testcase instance.
        self.post = BlogPost.objects.get(pk=1)
        # Store the CKEditorField as well.
        self.model_field = (self.post.items[1]._meta.
                            get_field_by_name('html')[0])

    def test_formfield(self):
        """
        Given the field on the model, we should be able to get our formfield.
        """
        self.assertIsInstance(self.model_field.formfield(), CKEditorFormField)

    @override_settings(INSTALLED_APPS=INSTALLED_APPS_WITH_SITES)
    def test_get_forbidden_domains__sites(self):
        """
        Make sure that we can get forbidden domains from the Sites framework.
        """
        self.assertEqual(set(self.model_field.get_forbidden_domains()),
                         set(['mydomain.com', 'dev.mydomain.com']))

    @override_settings(INSTALLED_APPS=INSTALLED_APPS_WITHOUT_SITES,
                       FLEXIBLE_CONTENT=FLEXIBLE_CONTENT_WITH_SITE_DOMAIN)
    def test_get_forbidden_domains__settings(self):
        """
        Make sure that we can get forbidden domains from FLEXIBLE_CONTENT
        settings.
        """
        self.assertEqual(set(self.model_field.get_forbidden_domains()),
                         set(['mydomain.com']))

    @override_settings(INSTALLED_APPS=INSTALLED_APPS_WITHOUT_SITES,
                       FLEXIBLE_CONTENT=FLEXIBLE_CONTENT_NO_DOMAIN)
    def test_get_forbidden_domains__none(self):
        """
        Ensure that, with no sites and no FLEXIBLE_CONTENT domain setting,
        we don't forbid any domains.
        """
        self.assertEqual(len(self.model_field.get_forbidden_domains()), 0)

    @skip("not implemented")
    def test_get_value_without_domains(self):
        pass

    @skip("not implemented")
    def test_get_value_without_domains__emptylist(self):
        pass

    @skip("not implemented")
    def test_clean__default(self):
        pass

    @skip("not implemented")
    def test_clean__from_setting(self):
        pass

class FormFieldUnitTest(TestCase):
    @skip("not implemented")
    def test_render(self):
        pass

    @skip("not implemented")
    def test_render__withattrs(self):
        pass
