"""
Selenium tests for django-organice.  Powered by behave.
'When' step implementations.
"""
from behave import when


@when(u'I open the "{target}" page')
def step_impl(context, target):
    context.browser.get(context.get_url(target))


@when(u'I click on the "{caption}" {name} link in the navigation')
def step_impl(context, caption, name):
    anchor = context.browser.find('.{css_class} a'.format(css_class=name))
    assert anchor.text == caption
    anchor.click()


@when(u'I click on the "{element_class}" link of the "{entry_title}" teaser')
def step_impl(context, element_class, entry_title):
    title = context.browser.find('.hentry .entry-title a').text
    assert title == entry_title, "Unexpected blog entry: {} != {}".format(title, entry_title)
    anchor = context.browser.find('.hentry .{css_class} a'.format(css_class=element_class))
    anchor.click()


@when(u'an invalid email was entered in the "{name}" field')
def step_impl(context, name):
    field = context.browser.find('form input[name={name}]'.format(name=name))
    field.clear()
    field.send_keys('@example.com')
