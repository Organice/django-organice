"""
A label command (sub-command) for the Organice management command.
"""
from django.utils.translation import ugettext as _

from ._helper import add_blog_category, add_blog_entry


class InitblogCommandMixin(object):

    def initblog_command(self):
        """
        Create sample blog entries
        """
        self.stdout.write('Generate blog content ...')

        add_blog_category(
            slug='events', title=_('Events'),
            description=_("Articles that are displayed in the Events section of our website."))
        add_blog_category(
            slug='press', title=_('Press'),
            description=_("Quotes about us in newspapers, or press releases."
                          " These articles are listed in the Press section of our website."))
        category_jobs = add_blog_category(
            slug='jobs', title=_('Jobs'),
            description=_("Job vacancies. Because everyone wants to work with us!"))

        add_blog_entry(slug='office-manager', title=_('Office Manager'),
                       categories=[category_jobs], tags='awesome, backoffice',
                       excerpt="We're looking for you. The best office manager (f/m) for a world-class team.",
                       plugins=[
            ('TextPlugin', "<p>We're looking for you."
                           " The best <strong>office manager (f/m)</strong> for a world-class team.</p>"
                           "<h3>Your Responsibilities</h3>"
                           "<ul>"
                           "<li>Answer phone calls, emails, and snail mail</li>"
                           "<li>Prepare our meetings facilities</li>"
                           "<li>Coordinate facility management staff</li>"
                           "<li>Be the nicest person in town -- <em>even when your boss has a bad day!</em></li>"
                           "</ul>"
                           "<h3>Your Qualifications</h3>"
                           "<ul>"
                           "<li>You're multilingual, ideally grown bilingual</li>"
                           "<li>You love communicating -- <em>\"small talk\" is your middle name!</em></li>"
                           "<li>You're funny, you're structured, and a computer freak</li>"
                           "</ul>"
                           "<p>Do you find yourself in this job description? Then we should talk!</p>"
                           "<p>Send your CV to <strong>jobs@example.com</strong></p>"
                           "<h2>Who We Are</h2>"
                           "<p>Demo Company is the leader in selling dreams and promises."
                           " What makes us different is we keep those promises.</p>"
                           "<p>Find more vacancies on our <a href=\"/about/jobs/\">jobs page</a>!</p>"),
        ])
        # TODO:
        # zinnia.Entry({
        #     "content_template": "zinnia/_entry_detail.html",
        #     "detail_template": "entry_detail.html",
        # })
        # Link({'mailto': 'jobs@example.com')
