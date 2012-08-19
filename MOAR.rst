More Django Testing Tips
========================

RTFM:
 - https://docs.djangoproject.com/en/dev/topics/testing/

Recommended talks:
 - http://pyvideo.org/video/699/testing-and-django
 - http://pyvideo.org/video/634/speedily-practical-large-scale-tests

unittest2 discovery mechanism:
 - https://code.djangoproject.com/ticket/17365
 - http://pypi.python.org/pypi/django-discover-runner

HTTPS testing -- use middleware to fake it
 -- e.g. http://djangosnippets.org/snippets/2009/

Multi-domain testing -- customise Client class

LiveServerTestCase + Selenium:
 - https://docs.djangoproject.com/en/dev/topics/testing/#live-test-server
 - http://seleniumhq.org/ -- web browser automation

Checkout Django's source:
 - https://github.com/django/django/blob/master/django/test/
 - explore Client and TestCase

Handy things in Django 1.4:
 - assertRaisesMessage((expected_exception, expected_message)
 - assertFieldOutput
 - assertContains(html=True)
 - assertTemplateUsed as context manager
 - assertHTMLEqual

Neat stuff inherited from unittest:
 - http://docs.python.org/library/unittest.html
 - assertRaisesRegexp, etc

Messing with settings:
 - with self.settings(FOO='bar'):
 - @override_settings (django.test.utils)
 - django.test.signals.setting_changed

Tools to explore:
 - http://nose.readthedocs.org/ -- "nicer testing for python"
 - + https://github.com/jbalogh/django-nose
 - http://nedbatchelder.com/code/coverage/
 - + https://code.djangoproject.com/ticket/4501
 - http://jenkins-ci.org/ -- Continuous Integration
 - http://tox.readthedocs.org/ -- multple python versions etc
 - http://pypi.python.org/pypi/WebTest/ -- wraps WSGI apps
 - + https://bitbucket.org/kmike/django-webtest
 - http://pypi.python.org/pypi/funkload/
 - http://www.djangopackages.com/grids/g/testing/

Download this from:
 - http://github.com/DrMeers
