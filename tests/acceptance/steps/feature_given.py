"""
Selenium tests for django-organice.  Powered by behave.
'Given' step implementations.
"""
from behave import given
from os.path import exists, join
from subprocess import call


@given(u'the demo project has been generated according to the documentation')
def step_impl(context):
    testproject_name = 'test_project_acceptance'
    testproject_files = [
        'manage.py',
    ] + [join(testproject_name, fname) for fname in [
        '__init__.py', 'urls.py', 'wsgi.py',
    ]] + [testproject_name + dir_tail for dir_tail in [
        '.media', '.static', '.templates',
    ]]

    for f in testproject_files:
        if not exists(f):
            assert call(['organice-setup', testproject_name]) == 0
            return


@given(u'I am on the "{title}" {name} page')
def step_impl(context, title, name):
    context.browser.get(context.get_url(name))
    assert context.browser.title.startswith(title)


@given(u'I am on the "{title}" {name} form')
def step_impl(context, title, name):
    context.execute_steps('''
        Given I am on the "{title}" {name} page
    '''.format(title=title, name=name))
