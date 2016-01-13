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
            ('TextPlugin', {
                'body': "<h1>Welcome to the Organice Demo Site!</h1>\n"
                        "<p>You can use the User Menu in the right upper corner to log in"
                        " or register for an account. You can immediately modify the content"
                        " of this website after logging in.</p>\n",
            }),
            ('TextPlugin', {
                'body': "<h1>Latest News</h1>\n",
            }),
            ('CMSLatestEntriesPlugin', {
                'template_to_render': 'cmsplugin_zinnia/entry_detail.html',
                'number_of_entries': 3,
            }),
        ])
        about_page = \
            add_cms_page(_('About Us'), slug='about', plugins=[
                ('TextPlugin', {
                    'body': "<h1>About Us</h1>\n"
                            "<p>We are Demo Company. The greatest place on earth!"
                            " That's what we are.</p>\n",
                }),
            ])
        programs_page = \
            add_cms_page(_('Programs'), plugins=[
                ('TextPlugin', {
                    'body': "<h1>Programs</h1>\n"
                            "<p>Demo Company is at the forefront of providing progressive"
                            " education programs to all ages and skill levels, whether recreational"
                            " or competitive, youth or adult.</p>\n"
                            "<p>At the heart of our programs there is always fun."
                            " This is the foundation of our work to develop world-class talents.</p>\n",
                }),
            ])
        add_cms_page(_('Sponsors'), plugins=[
            ('TextPlugin', {
                'body': "<h1>Sponsors</h1>\n"
                        "<p>Please applaud our very special sponsors. Say &ldquo;thank you&rdquo;"
                        " with us. They trust in us that we give our best.</p>\n",
            }),
            ('TextPlugin', {
                'body': "<h2>Gold Sponsors</h2>\n<p>...</p>\n",
            }),
            ('TextPlugin', {
                'body': "<h2>Silver Sponsors</h2>\n<p>...</p>\n",
            }),
        ])
        add_cms_page(_('Jobs'), parent=about_page, plugins=[
            ('TextPlugin', {
                'body': "<h1>Job Vacancies</h1>\n"
                        "<p>We're always looking for great talents."
                        " Do you also want to be part of a world-class team?</p>\n",
            }),
            ('TextPlugin', {
                'body': "<h2>Administration</h2>\n",
            }),
            ('CMSLatestEntriesPlugin', {
                'template_to_render': 'cmsplugin_zinnia/entry_list.html',
                'number_of_entries': 0,
            }),
        ])
        add_cms_page(_('Contact Us'), slug='contact', parent=about_page, plugins=[
            ('TextPlugin', {
                'body': "<h1>Office</h1>\n"
                        "<p>Demo Company street, 1a<br>12345 Isles of Scilly</p>\n"
                        "<p>Phone: +123 4567-890</p>\n",
            }),
            ('TextPlugin', {
                'body': "<h2>Contact Form</h2>\n",
            }),
            # ('ContactPlugin', {
            #     'content_label': "What you want to say",
            #     'subject_label': "Subject",
            #     'email_label': "Your email address",
            #     'site_email': "support@organice.io",
            #     'submit': "Send Email",
            #     'thanks': "<h2>Thank You!</h2>"
            #               "<p>Thank you very much for your valuable interest in us!</p>"
            #               "<p>We'll get back to you about your request as soon as possible.</p>",
            # }),
        ])
        add_cms_page(_('Directions'), parent=about_page, plugins=[
            ('GoogleMapPlugin', {
                'city': "Isles of Scilly",
                'title': "How You Find Us",
                'zipcode': "TR24 0QH",
                'width': "100%",
                'address': "Isles of Scilly",
                'height': "400px",
                'zoom': 16,
            }),
        ])
        add_cms_page(_('Juniors'), parent=programs_page, plugins=[
            ('TextPlugin', {
                'body': "<h1>Juniors</h1>\n"
                        "<p>Training and education of our young stars.</p>\n",
            }),
        ])
        add_cms_page(_('Seniors'), parent=programs_page, plugins=[
            ('TextPlugin', {
                'body': "<h1>Seniors</h1>\n"
                        "<p>Recreational programs for retired professionals and hobbyists.</p>\n",
            }),
        ])
