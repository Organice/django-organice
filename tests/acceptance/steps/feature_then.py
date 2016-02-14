"""
Selenium tests for django-organice.  Powered by behave.
'Then' step implementations.
"""
import re
from behave import then


@then(u'a document titled "{title_re}" is loaded')
def step_impl(context, title_re):
    assert re.match(title_re, context.browser.title)


@then(u'"{header_re}" is shown as page header')
def step_impl(context, header_re):
    page_title = context.browser.find('h1')
    assert re.match(header_re, page_title.text)


@then(u'"{header_re}" is shown as a section header')
def step_impl(context, header_re):
    section_titles = context.browser.find_all('h1')
    for title in section_titles:
        if re.match(header_re, title.text):
            return
    titles = '`, `'.join([t.text for t in section_titles])
    assert False, "Section %s not found in [`%s`]." % (header_re, titles)


@then(u'a blog teaser titled "{title_re}" is displayed below')
def step_impl(context, title_re):
    entry_title = context.browser.find('h2.entry-title > a')
    assert re.match(title_re, entry_title.text)


@then(u'a "{widget_id}" widget is displayed in the "{container_id}"')
def step_impl(context, widget_id, container_id):
    container = context.browser.find('#{id}'.format(id=container_id))
    assert container.find('#{id}'.format(id=widget_id))


@then(u'the blog entry "{slug}" titled "{title_re}" is displayed')
def step_impl(context, slug, title_re):
    browser_url = context.browser.current_url
    assert browser_url.endswith('%s/' % slug)

    # TODO: should better be <h1> one day!
    page_title = context.browser.find('h2')
    assert re.match(title_re, page_title.text)


@then(u'the {name} page titled "{title_re}" is shown')
def step_impl(context, name, title_re):
    browser_url = context.browser.current_url
    target_url = context.get_url(name) \
        if name in ['index', 'create'] \
        else context.get_url(name, context.pk)
    assert browser_url == target_url, \
        '{} != {}'.format(browser_url, target_url)

    page_title = context.browser.find('h1')
    assert re.match(title_re, page_title.text)


@then(u'the page shows a "{message}" message')
def step_impl(context, message):
    first_paragraph = context.browser.find('h1 + p')
    assert first_paragraph.text == message


@then(u'I see a list composed of a key, an edit link and a delete link')
def step_impl(context):
    key_lables = context.browser.find_all('.contact-list .key')
    edit_links = context.browser.find_all('.contact-list .edit a')
    delete_links = context.browser.find_all('.contact-list .delete a')
    assert len(key_lables) == len(edit_links) == len(delete_links)


@then(u'the navigation menu has {count} entries: "{names}"')
def step_impl(context, count, names):
    nav_links = context.browser.find_all('#nav li a')
    assert len(nav_links) == int(count), \
        '{} != {}'.format(len(nav_links), count)

    for i, name in enumerate(names.split(', ')):
        label = nav_links[i].text
        assert label == name, "Unexpected navigation link: {} != {}".format(label, name)


@then(u'the 5 input fields labeled "{labels}" are available')
def step_impl(context, labels):
    captions = ['%s:' % label for label in labels.split(', ')]
    form_labels = context.browser.find_all('form label')

    for label in form_labels:
        assert label.text in captions, \
            '{} not in {}'.format(label.text, ','.join(captions))
        captions.remove(label.text)


@then(u'all empty, mandatory fields "{fields}" are highlighted as erroneous')
def step_impl(context, fields):
    error_fields = context.browser.find_all('form .errorlist + p > label + input')
    required_fields = fields.split(', ')

    for name in required_fields:
        field = context.browser.find('form input[name={name}]'.format(name=name))
        if len(field.text) == 0:
            assert field in error_fields, 'Empty, mandatory field not marked erroneous'


@then(u'an error message is displayed and we remain on the {name} page')
def step_impl(context, name):
    target_url = context.get_url(name) if name in ['index', 'create'] \
        else context.get_url(name, context.pk)
    assert target_url == context.browser.current_url
    # TODO: detect browser-side validation triggered (e.g. email field)


@then(u'a success message "{msg_re}" is displayed')
def step_impl(context, msg_re):
    message = context.browser.find('.system-messages .success')
    assert re.match(msg_re, message.text)
