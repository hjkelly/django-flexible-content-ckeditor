from distutils.core import setup
from setuptools import find_packages

# Find all packages here and below (should find ipanema and its children).
packages = find_packages()

setup(name='django-flexible-content-ckeditor',
      description="Rich text (WYSIWYG) support for django-flexible-content",
      url='https://github.com/hjkelly/django-flexible-content-ckeditor',
      maintainer='Harrison Kelly',
      maintainer_email='hjkelly@gmail.com',
      version='1.0.0',
      packages=packages,
      include_package_data=True,
      install_requires=['django-flexible-content'])
