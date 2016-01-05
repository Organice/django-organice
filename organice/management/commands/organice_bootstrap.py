"""
Management commands for django Organice.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from cms.api import add_plugin, create_page
from cms.models import Title


def create_user(username, email='testuser@organice.io'):
    print(u"Creating user {} with password {} ...".format(username, username))
    try:
        User.objects.get(username=username).delete()
        print(u"Warning: deleted existing user {} first.".format(username))
    except User.DoesNotExist:
        pass
    User.objects.create_user(username, email, username).save()


def delete_page(title):
    """Delete all pages with the given title."""
    while len(Title.objects.filter(title=title)):
        # Pain! filter, because django CMS creates 2 titles for each page
        page = Title.objects.filter(title=title).first().page
        print(u"Warning: deleting existing page {} first ...".format(title))
        page.delete()
        # TODO: Check, are plugins deleted automatically? (cascading)


def add_cms_page(title, template='cms_base.html', parent=None, lang='en', plugins=()):
    """
    Create or recreate a CMS page including a content plugins with content in them.
    """
    print(u"Creating page {} ...".format(title))
    delete_page(title)
    page = create_page(title, template, language=lang, in_navigation=True, parent=parent)
    placeholder = page.placeholders.get(slot='content')
    for plugin, body in plugins:
        add_plugin(placeholder, plugin, lang, body=body)
    page.publish(lang)
    return page


class Command(BaseCommand):
    help = 'Organice management commands.'

    def handle(self, *args, **options):
        self.stdout.write('Initialize database ...')
        call_command('migrate')

        self.stdout.write('Create admin user ...')
        call_command('createsuperuser', '--username', 'admin', '--email', 'you@example.com', '--noinput')
        u = User.objects.get(username='admin')
        u.set_password('admin')
        u.save()

        self.stdout.write('Generate menu structure and pages ...')
        add_cms_page(_('Home'), plugins=[
            ('TextPlugin', "<h1>Welcome to the Organice Demo Site!</h1>"
                           "<p>You can use the User Menu in the right upper corner to log in or register for an"
                           " account. You can immediately modify the content of this website after logging in.</p>"),
            ('TextPlugin', "<h1>Latest News</h1>"),
            # ('CMSLatestEntriesPlugin', {
            #     "template_to_render": "cmsplugin_zinnia/entry_detail.html",
            #     "number_of_entries": 3,
            # }),
        ])
        about_page = \
            add_cms_page(_('About Us'), plugins=[
                ('TextPlugin', "<h1>About Us</h1>"
                               "<p>We are Demo Company. The greatest place on earth! That's what we are.</p>"),
            ])
        programs_page = \
            add_cms_page(_('Programs'), plugins=[
                ('TextPlugin', "<h1>Programs</h1>"
                               "<p>Demo Company is at the forefront of providing progressive education programs to"
                               " all ages and skill levels, whether recreational or competitive, youth or adult.</p>"
                               "<p>At the heart of our programs there is always fun. This is the foundation of our"
                               " work to develop world-class talents.</p>"),
            ])
        add_cms_page(_('Sponsors'), plugins=[
            ('TextPlugin', "<h1>Sponsors</h1>"
                           "<p>Please applaud our very special sponsors. Say \"thank you\" with us."
                           " They trust in us that we give our best.</p>"),
            ('TextPlugin', "<h2>Gold Sponsors</h2><p>...</p>"),
            ('TextPlugin', "<h2>Silver Sponsors</h2><p>...</p>"),
        ])
        add_cms_page(_('Jobs'), parent=about_page, plugins=[
            ('TextPlugin', "<h1>Job Vacancies</h1>"
                           "<p>We're always looking for great talents."
                           " Do you also want to be part of a world-class team?</p>"),
        ])
        add_cms_page(_('Contact Us'), parent=about_page, plugins=[
            ('TextPlugin', "<h1>Office</h1>"
                           "<p>Demo Company street, 1a<br>12345 Isles of Scilly</p>"
                           "<p>Phone: +123 4567-890</p>"),
            ('TextPlugin', "<h2>Contact Form</h2>"),
            # ('ContactPlugin', {
            #     "content_label": "What you want to say",
            #     "subject_label": "Subject",
            #     "email_label": "Your email address",
            #     "site_email": "support@organice.io",
            #     "submit": "Send Email",
            #     "thanks": "<h2>Thank You!</h2>"
            #               "<p>Thank you very much for your valuable interest in us!</p>"
            #               "<p>We'll get back to you about your request as soon as possible.</p>",
            # }),
        ])
        add_cms_page(_('Directions'), parent=about_page, plugins=[
            # ('GoogleMapPlugin', {
            #     "city": "Isles of Scilly",
            #     "title": "How You Find Us",
            #     "zipcode": "Isles of Scilly",
            #     "width": "100%",
            #     "address": "Isles of Scilly",
            #     "height": "400px",
            # }),
        ])
        add_cms_page(_('Juniors'), parent=programs_page, plugins=[
            ('TextPlugin', "<h1>Juniors</h1>"
                           "<p>Training and education of our young stars.</p>"),
        ])
        add_cms_page(_('Seniors'), parent=programs_page, plugins=[
            ('TextPlugin', "<h1>Seniors</h1>"
                           "<p>Recreational programs for retired professionals and hobbyists.</p>"),
        ])

        # self.stdout.write('Generate blog content ...')
        # zinnia.Category({
        #     "description": "Articles that are displayed in the Events section of our website.",
        #     "title": "Events",
        #     "slug": "events",
        # })
        # zinnia.Category({
        #     "description": "Quotes about us in newspapers, or press releases."
        #                    " These articles are listed in the Press section of our website.",
        #     "title": "Press",
        #     "slug": "press",
        # })
        # zinnia.Category({
        #     "description": "Job vacancies. Because everyone wants to work with us!",
        #     "title": "Jobs",
        #     "slug": "jobs",
        # })
        # zinnia.Entry({
        #     "content_template": "zinnia/_entry_detail.html",
        #     "detail_template": "entry_detail.html",
        #     "excerpt": "We're looking for you. The best office manager (f/m) for a world-class team.",
        #     "title": "Office Manager",
        #     "content": "<p>We're looking for you."
        #                " The best <strong>office manager (f/m)</strong> for a world-class team.</p>"
        #                "<h3>Your Responsibilities</h3>"
        #                "<ul>"
        #                "<li>Answer phone calls, emails, and snail mail</li>"
        #                "<li>Prepare our meetings facilities</li>"
        #                "<li>Coordinate facility management staff</li>"
        #                "<li>Be the nicest person in town -- <em>even when your boss has a bad day!</em></li>"
        #                "</ul>"
        #                "<h3>Your Qualifications</h3>"
        #                "<ul>"
        #                "<li>You're multilingual, ideally grown bilingual</li>"
        #                "<li>You love communicating -- <em>\"small talk\" is your middle name!</em></li>"
        #                "<li>You're funny, you're structured, and a computer freak</li>"
        #                "</ul>"
        #                "<p>Do you find yourself in this job description? Then we should talk!</p>"
        #                "<p>Send your CV to <strong>jobs@example.com</strong></p>"
        #                "<h2>Who We Are</h2>"
        #                "<p>Demo Company is the leader in selling dreams and promises."
        #                " What makes us different is we keep those promises.</p>"
        #                "<p>Find more vacancies on our <a href="/about/jobs/">jobs page</a>!</p>",
        #     "slug": "office-manager",
        # })
        # Link({'mailto': 'jobs@example.com')

        # self.stdout.write('Generate provider data for social authentication ...')
        # TODO: generate auth providers instead of loading fixtures

        self.stdout.write('Have an organiced day!')
