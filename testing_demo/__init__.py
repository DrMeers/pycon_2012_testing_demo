"""
An assortment of demonstration testing helpers.
"""

import hashlib
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core import exceptions
from django.core.urlresolvers import reverse
from django.db import DEFAULT_DB_ALIAS, connections
from django.test import Client, TestCase
from django.test.testcases import _AssertNumQueriesContext

logger = logging.getLogger('tests.demo')

# You could set up your logging to include something like:
"""
LOGGING['handlers']['console'] = {'class': 'logging.StreamHandler'}
LOGGING['loggers']['tests'] = {'handlers': ['console'], 'level': 'INFO'}
"""

def get_hash(string, length=8):
    """ Shortcut for generating short hash strings """
    return hashlib.sha1(string).hexdigest()[:length]

def reloaded(obj):
    """ Reload an object from the database """
    return obj.__class__._default_manager.get(pk=obj.pk)


class DemoClient(Client):
    """ Add mind-blowing Client customisations in here... """
    def get(self, path, data={}, **kwargs):
        logger.debug(path)
        return super(DemoClient, self).get(path, data, **kwargs)


class DemoTestCase(TestCase):
    """ A customised TestCase for demonstration purposes """

    client_class = DemoClient
    PASSWORDS = {}

    def _assertContains(self, super_method, response, text, **kwargs):
        """
        Logs content on failure and accepts case_sensitive kwarg.
        TODO: modify *copy* of content/text rather than actual...
        """
        case_sensitive = kwargs.pop('case_sensitive', True)
        if not case_sensitive:
            response.content = response.content.lower()
            text = text.lower()
        try:
            super_method(response, text, **kwargs)
        except AssertionError:
            logger.warning(
                'Searched content: """{}"""'.format(response.content))
            raise

    def assertContains(self, *args, **kwargs):
        return self._assertContains(
            super(DemoTestCase, self).assertContains, *args, **kwargs)

    def assertNotContains(self, *args, **kwargs):
        return self._assertContains(
            super(DemoTestCase, self).assertNotContains, *args, **kwargs)

    def create_user(self, username, email=None, password=None, super=False):
        """ Shortcut for creating users """
        params = {
            'username': username,
            'email': email or (u'%s@example.com' % get_hash(username)),
            'password': password or get_hash(username+'PASSWORD'),
        }
        method = (
            User.objects.create_superuser if super else
            User.objects.create_user
        )
        self.PASSWORDS[params['username']] = params['password']
        return method(**params)

    def login(self, username):
        """ Shortcut for logging in which asserts success """
        self.assertTrue(
            self.client.login(
                username=username, password=self.PASSWORDS[username]))

    def _test_urls(self, url_attributes):
        """ Example helper for quick/dirty URL coverage """
        for url, attributes in url_attributes:
            response = self.client.get(url)
            if 'status_code' in attributes:
                self.assertEqual(
                    response.status_code, attributes['status_code'])
            if 'template' in attributes:
                self.assertTemplateUsed(response, attributes['template'])

    def _test_admin(self, MODELS):
        """
        Shortcut for detecting broken admin change lists/forms.
        Beware query expense involved...
        """
        for model in MODELS:
            changelist_url = reverse(
                'admin:%s_%s_changelist' % (
                    model._meta.app_label, model._meta.module_name
                )
            )
            response = self.client.get(changelist_url)
            self.assertTemplateUsed(response, 'admin/change_list.html')

            add_url = reverse(
                'admin:%s_%s_add' % (
                    model._meta.app_label,
                    model._meta.module_name
                )
            )
            response = self.client.get(add_url)
            self.assertTemplateUsed(response, 'admin/change_form.html')

            for instance in model._default_manager.all():
                change_url = reverse(
                    'admin:%s_%s_change' % (
                        model._meta.app_label,
                        model._meta.module_name,
                    ),
                    args=(instance.pk,)
                )
                response = self.client.get(change_url)
                self.assertTemplateUsed(response, 'admin/change_form.html')

    def assertNumQueries(self, num, func=None, *args, **kwargs):
        """ Identical to TransactionTestCase, but with custom Context """
        using = kwargs.pop("using", DEFAULT_DB_ALIAS)
        conn = connections[using]

        context = _VerboseAssertNumQueriesContext(self, num, conn)
        if func is None:
            return context

        with context:
            func(*args, **kwargs)

class _VerboseAssertNumQueriesContext(_AssertNumQueriesContext):
    """
    Modified context manager which logs the unexpected queries.
    """

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            super(_VerboseAssertNumQueriesContext, self).__exit__(
                exc_type, exc_value, traceback)
        except AssertionError as e:
            queries = self.connection.queries[self.starting_queries:]
            logger.warning(
                '\n    '.join(
                    ['Unexpected queries ({0}):'.format(e)] +
                    map(unicode, queries)
                )
            )
            raise
