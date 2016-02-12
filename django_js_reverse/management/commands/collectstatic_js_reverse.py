# -*- coding: utf-8 -*-
import os
import sys

from django.conf import settings
from django.core import urlresolvers
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand

from django_js_reverse.core import generate_js


class Command(BaseCommand):
    help = 'Creates a static urls-js file for django-js-reverse'

    def add_arguments(self, parser):
        parser.add_argument(
            '--directory', '-d', default=None, type=str,
            help="Define where to store generated file. Defaults to STATIC_ROOT/django_js_reverse/js/")
        parser.add_argument(
            '--name', '-n', default='reverse.js', type=str,
            help="Define name of generated file. Defaults to reverse.js")

    def handle(self, *args, **options):
        file = options['name']
        path = options['directory']
        if path is None:
            if not hasattr(settings, 'STATIC_ROOT') or not settings.STATIC_ROOT:
                raise ImproperlyConfigured('The collectstatic_js_reverse command needs settings.STATIC_ROOT to be set.')
            path = os.path.join(settings.STATIC_ROOT, 'django_js_reverse', 'js')

        fs = FileSystemStorage(location=path)
        if fs.exists(file):
            fs.delete(file)

        default_urlresolver = urlresolvers.get_resolver(None)
        content = generate_js(default_urlresolver)
        fs.save(file, ContentFile(content))
        if len(sys.argv) > 1 and sys.argv[1] in ['collectstatic_js_reverse']:
            self.stdout.write('js-reverse file written to %s' % (os.path.join(path, file)))  # pragma: no cover
