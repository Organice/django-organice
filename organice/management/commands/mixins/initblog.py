"""
A label command (sub-command) for the Organice management command.
"""
from django.utils.translation import ugettext as _

from ._helper import HelperMixin


class InitblogCommandMixin(HelperMixin):

    def initblog_command(self):
        """
        Create sample blog entries
        """
        if self.verbosity >= 1:
            self.stdout.write(_('Generate blog content ...'))

        self.add_blog_category(
            slug='events', title=_('Events'),
            description=_("Articles that are displayed in the Events section of our website."))
        self.add_blog_category(
            slug='press', title=_('Press'),
            description=_("Quotes about us in newspapers, or press releases."
                          " These articles are listed in the Press section of our website."))
        category_jobs = self.add_blog_category(
            slug='jobs', title=_('Jobs'),
            description=_("Job vacancies. Because everyone wants to work with us!"))

        self.add_blog_entry(slug='office-manager', title=_('Office Manager'),
                            categories=[category_jobs], tags='awesome, backoffice',
                            excerpt="We're looking for you. The best office manager (f/m) for a world-class team.",
                            plugins=[
            ('TextPlugin', {
                'body': "<p>We're looking for you."
                        " The best <strong>office manager (f/m)</strong> for a world-class team.</p>\n"
                        "<h3>Your Responsibilities</h3>\n"
                        "<ul>\n"
                        "<li>Answer phone calls, emails, and snail mail</li>\n"
                        "<li>Prepare our meetings facilities</li>\n"
                        "<li>Coordinate facility management staff</li>\n"
                        "<li>Be the nicest person in town &mdash;"
                        " <em>even when your boss has a bad day!</em></li>\n"
                        "</ul>\n"
                        "<h3>Your Qualifications</h3>\n"
                        "<ul>\n"
                        "<li>You're multilingual, ideally grown bilingual</li>\n"
                        "<li>You love communicating &mdash;"
                        " <em>&ldquo;small talk&rdquo; is your middle name!</em></li>\n"
                        "<li>You're funny, you're structured, and a computer freak</li>\n"
                        "</ul>\n"
                        "<p>Do you find yourself in this job description? Then we should talk!</p>\n"
                        "<p>Send your CV to <strong>jobs@example.com</strong></p>\n"
                        "<h2>Who We Are</h2>\n"
                        "<p>Demo Company is the leader in selling dreams and promises."
                        " What makes us different is we keep those promises.</p>\n"
                        "<p>Find more vacancies on our <a href=\"/about/jobs/\">jobs page</a>!</p>\n",
            }),
        ])
        # TODO: Link({'mailto': 'jobs@example.com'}) inside TextPlugin
