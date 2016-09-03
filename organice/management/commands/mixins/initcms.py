"""
A label command (sub-command) for the Organice management command.
"""
from django.utils.translation import ugettext as _

from ._helper import HelperMixin


class InitcmsCommandMixin(HelperMixin):
    def initcms_command(self):
        """
        Create some pages with sample content
        """
        if self.verbosity >= 1:
            self.stdout.write(_('Generate menu structure and pages:'))

        self.add_cms_page(_('Home'), plugins=[
            ('TextPlugin', {
                'body': "<h1>Hello at Organice!</h1>\n"
                        "<p>Thank you for your interest in Organice. The Organice platform is powered"
                        " by <a href=\"https://github.com/Organice/django-organice\">django Organice</a>,"
                        " a compilation of the best Django packages, preconfigured for getting you"
                        " started quickly.<p>\n"
                        "<p>With <a href=\"https://www.djangoproject.com/\">Django</a> under the hood"
                        " it's easy for us to promise powerful development speed paired with unparalleled"
                        " flexibility. For Web agencies and independent professionals.</p>\n",
            }),
            ('TextPlugin', {
                'body': "<blockquote>\n"
                        "<h2>It has never been easier.</h2>\n"
                        "<p>With front-end editing getting things done is fast.</p>\n"
                        "<h2>Never been more effective.</h2>\n"
                        "<p>Empower everyone, with no effort.</p>\n"
                        "<h2>Never been more fun.</h2>\n"
                        "<p>Invest your time, but not your anger.</p>\n"
                        "</blockquote>\n",
            }),
            ('TextPlugin', {
                'body': "<h1>This is a Demo Site</h1>\n"
                        "<p>This website is a demo site and your playground at the same time."
                        " The content is re-generated every day. Feel free to log in and apply"
                        " your changes!</p>\n"
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
            self.add_cms_page(_('About Us'), slug='about', plugins=[
                ('TextPlugin', {
                    'body': "<h1>About Us</h1>\n"
                            "<p>We are Demo Company. The greatest place on earth!"
                            " That's what we are.</p>\n",
                }),
            ])
        programs_page = \
            self.add_cms_page(_('Programs'), plugins=[
                ('TextPlugin', {
                    'body': "<h1>Programs</h1>\n"
                            "<p>Demo Company is at the forefront of providing progressive"
                            " education programs to all ages and skill levels, whether recreational"
                            " or competitive, youth or adult.</p>\n"
                            "<p>At the heart of our programs there is always fun."
                            " This is the foundation of our work to develop world-class talents.</p>\n",
                }),
            ])
        self.add_cms_page(_('Sponsors'), plugins=[
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
        self.add_cms_page(_('Jobs'), parent=about_page, plugins=[
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
        self.add_cms_page(_('Contact Us'), slug='contact', parent=about_page, plugins=[
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
        self.add_cms_page(_('Directions'), parent=about_page, plugins=[
            ('MapsPlugin', {
                'city': "Isles of Scilly",
                'title': "How You Find Us",
                'zipcode': "TR24 0QH",
                'width': "100%",
                'address': "Isles of Scilly",
                'height': "400px",
                'zoom': 16,
            }),
        ])
        self.add_cms_page(_('Juniors'), parent=programs_page, plugins=[
            ('TextPlugin', {
                'body': "<h1>Juniors</h1>\n"
                        "<p>Training and education of our young stars.</p>\n",
            }),
        ])
        self.add_cms_page(_('Seniors'), parent=programs_page, plugins=[
            ('TextPlugin', {
                'body': "<h1>Seniors</h1>\n"
                        "<p>Recreational programs for retired professionals and hobbyists.</p>\n",
            }),
        ])

        self.add_cms_page(_('Imprint'), slug='imprint', in_navigation=False, plugins=[
            ('TextPlugin', {
                'body': "<h1>Imprint</h1>\n"
                        "<p>Organice Demo<br>"
                        "Hosted by the creators of <a href=\"%(pypi_url)s\">django-organice</a>.</p>\n"
                        "\n"
                        "<h2>Privacy Policy</h2>\n"
                        "<p>This website uses cookies to provide a safe and convenient user"
                        " experience. However, no personal data is collected or evaluated."
                        " By using this website you consent our use of cookies.</p>\n" % {
                            'pypi_url': "https://pypi.python.org/pypi/django-organice",
                        },
            }),
        ])
