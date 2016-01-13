"""
A label command (sub-command) for the Organice management command.
"""
from django.utils.translation import ugettext as _

from ._helper import add_cms_page


class InitcmsCommandMixin(object):

    def initcms_command(self):
        """
        Create some pages with sample content
        """
        self.stdout.write(_('Generate menu structure and pages ...'))
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
            add_cms_page(_('About Us'), slug='about', plugins=[
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
        add_cms_page(_('Contact Us'), slug='contact', parent=about_page, plugins=[
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
