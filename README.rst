django-flexible-content-ckeditor
================================
A flexible item type for django-flexible-content that implements a CKEditor

Why?
----
Because ``django-flexible-content`` is designed to be as minimal as possible, its default set of item types was never meant to satisfy everyone. I designed this plugin for my own use, for obvious reasons: sometimes plain text isn't featureful enough, and HTML isn't a user-friendly option.

What does it do?
----------------
It allows user-friendly input of basic text:

- paragraphs
- bold, italic, underline
- lists
- links (these can be configured)

In addition, the underlying CKEditorField itself can optionally clean the submitted HTML, removing all fields except those above. So if you want to strip outside styles and tags at all cost, it can do that. Alternatively, if you want to leave room for small HTML tweaks, you can disable this as well.

What doesn't it do?
-------------------
It intentionally *doesn't* support uploading images or files. One of the ideas behind ``django-flexible-content`` was that those things are style-able and well-managed on the back-end.

A few examples:

* If you want to display an image or download with a heading above it, a caption below it, or a description next to it, your image type can support that. A WYSIWYG editor almost never could.
* If you have the same PDF or image uploaded in 18 different places, you can choose how to handle that in your image type (offer a list of existing files; detect duplicate uploads and point all those references to a single version of the file).

Technically, you could manually link to an uploaded file, or reference an image in the raw HTML... oh well.

How do I set it up?
-------------------

1.  Install the package: ``pip install django-flexible-content-ckeditor``
2.  Update the project's settings to include the package in ``INSTALLED_APPS``:
    ::

        INSTALLED_APPS = (
            # your other apps here
            # ...
            'flexible_ckeditor',
        )
3.  Update the project's settings to include the new CKEditor flexible item type:
    ::

        FLEXIBLE_CONTENT = {
            'ITEM_TYPES': (
                'flexible_ckeditor.CKEditorText',

                # You'll probably want to include some of the default item types,
                # if you hadn't configured FLEXBILE_CONTENT['ITEM_TYPES'] yet.
                'default_item_types.Download',
                'default_item_types.Image',
                'default_item_types.Video',
            ),
        }
4.  Restart your server and go!

Can I use the editor elsewhere in my project?
---------------------------------------------
Yes! Though the editor may be trimmed down, it can be used to support basic formatting on arbitrary models, outside of ``django-flexible-content``'s content areas::

    from django.db import models
    from flexible_ckeditor.fields import CKEditorField

    class Person(models.Model):
        name = models.CharField(max_length=100)
        bio = CKEditorField()

Note that it'll still abide by the settings defined in ``FLEXIBLE_CONTENT['ckeditor']``, such as whether or not to clean the HTML upon submission.
