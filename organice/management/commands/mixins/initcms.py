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

        self.add_cms_page(_('Organice'), plugins=[
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
        project_page = \
            self.add_cms_page(_('Project'), plugins=[
                ('TextPlugin', {
                    'body': "<h1>The django Organice Project</h1>\n"
                            "<p>Organice.io builds on open source software, and django Organice is"
                            " open source software itself. &ndash; We want to make the world a"
                            " better place!</p>\n",
                }),
                ('TextPlugin', {
                    'body': "<h2>Features and Goals</h2>"
                            "<dl>\n"
                            "<dt>Honest collaboration</dt>\n"
                            "  <dd>We implement best-of-breed concepts for collaboration."
                            " Transparency is king, and freedom wins. For people with honest minds,"
                            " bold and open-minded. We know that this is the future. It's simple as"
                            " maths: Because today's businesses lose more with restrictions than"
                            " they can gain with tomorrow's freedom.</dd>\n"
                            "<dt>Usability counts</dt>\n"
                            "  <dd>One of our key goals is to provide an absolutely intuitive,"
                            " consistent user experience. Because in fast-paced, flexible, probably"
                            " small-margin businesses you don’t have the time to invest in training"
                            " your staff. That's why our software also works perfect in very"
                            " demanding environments, such as non-profit organizations with unpaid"
                            " volunteers.</dd>\n"
                            "<dt>Reliable software</dt>\n"
                            "  <dd>We build on promising, reliable Django components, and rather"
                            " invest in those projects than build source code here. We expect to"
                            " continually tune the compilation to keep the source footprint small,"
                            " keeping the project lean and responsive. We give back to the"
                            " community, because everyone profits.</dd>\n"
                            "</dl>\n",
                }),
            ])
        self.add_cms_page(_('Themes'), plugins=[
            ('TextPlugin', {
                'body': "<h1>Themes</h1>\n"
                        "<p>django Organice comes with a default theme, which is fully responsive,"
                        " i.e. optimized for mobile devices. Every new theme can build on its"
                        " features. This way designers can focus on creating a beautiful,"
                        " customized visual appearance for you!</p>\n",
            }),
            ('TextPlugin', {
                'body': "<h2>Documentation</h2>\n"
                        "<p>Wondering how to customize a theme, or to write your own? See the"
                        " documentation at:</p>\n"
                        "<dl>\n"
                        "<dt>Technical documentation on themes</dt>\n"
                        '  <dd><a href="http://docs.organice.io/en/latest/themes.html">'
                        "docs.organice.io</a></dd>\n"
                        "</dl>\n",
            }),
        ])
        self.add_cms_page(_('Jobs'), parent=about_page, plugins=[
            ('TextPlugin', {
                'body': "<h1>Job Vacancies (Demo)</h1>\n"
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
        self.add_cms_page(_('Documentation'), parent=project_page, plugins=[
            ('TextPlugin', {
                'body': "<h2>Documentation</h2>"
                        "<dl>\n"
                        "<dt>Read the docs</dt>\n"
                        '  <dd>The <a href="http://docs.organice.io/en/latest/components.html">'
                        "User Manual chapter</a> in the documentation is targeted at end users."
                        "</dd>\n"
                        "  <dd>Full technical documentation is available at"
                        ' <a href="http://docs.organice.io">docs.organice.io</a>.</dd>\n'
                        "<dt>Demos</dt>\n"
                        '  <dd>Our main demo site <a href="https://demo.organice.io">'
                        "demo.organice.io</a> is an open playground. Register an account there"
                        " and play. This instance is reset every morning.</dd>\n"
                        "  <dd>Of course you can also register with and contribute content to"
                        " any other live Organice site, such as"
                        ' <a href="https://organice.io">organice.io</a> itself.</dd>\n'
                        "</dl>\n",
            }),
        ])
        self.add_cms_page(_('Contribute'), parent=project_page, plugins=[
            ('TextPlugin', {
                'body': "<h2>Get Involved!</h2>"
                        "<dl>\n"
                        "<dt>Source Code</dt>\n"
                        '  <dd>GitHub: <a href="https://github.com/organice/django-organice">'
                        "github.com/organice/django-organice</a></dd>\n"
                        '  <dd>GitLab: <a href="https://gitlab.com/organice/django-organice">'
                        "gitlab.com/organice/django-organice</a></dd>\n"
                        '  <dd>Bitbucket: <a href="https://bitbucket.org/organice/django-organice">'
                        "bitbucket.org/organice/django-organice</a></dd>\n"
                        "</dl>\n",
            }),
            ('TextPlugin', {
                'body': "<p>Find out more about django Organice! Fork us, test, find bugs,"
                        " write code and documentation, translate.</p>\n"
                        "<p>Your contribution is welcome!</p>\n",
            }),
        ])

        self.add_cms_page(_('Imprint'), slug='imprint', in_navigation=False, plugins=[
            ('TextPlugin', {
                'body': "<h1>Imprint</h1>\n"
                        "<p>Organice Demo<br>"
                        'Hosted by the creators of <a href="%(pypi_url)s">django-organice</a>.</p>\n'
                        "\n"
                        "<h2>Privacy Policy</h2>\n"
                        "<p>This website uses cookies to provide a safe and convenient user"
                        " experience. However, no personal data is collected or evaluated."
                        " By using this website you consent our use of cookies.</p>\n" % {
                            'pypi_url': "https://pypi.python.org/pypi/django-organice",
                        },
            }),
        ])
