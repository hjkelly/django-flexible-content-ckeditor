from django.test import TestCase
from django.test.utils import override_settings
from django.utils.unittest import skip

from mock_project.myapp.models import BlogPost

from .fields import CKEditorField, CKEditorFormField
from .models import CKEditorText


class ModelFieldUnitTest(TestCase):
    def setUp(self):
        self.test_field(

    @skip("not implemented")
    def test_formfield(self):
        assertself.test_field.render()

    @skip("not implemented")
    def test_get_forbidden_domains__sites(self):
        pass

    @skip("not implemented")
    def test_get_forbidden_domains__settings(self):
        pass

    @skip("not implemented")
    def test_get_forbidden_domains__none(self):
        pass

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
