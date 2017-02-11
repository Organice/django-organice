"""
Authentication adapters for Organice
"""
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _

from .groups import GUESTS_GROUP

ADMIN_EMAIL_ADDRESSES = [email for name, email in settings.ADMINS]


class EditorialWorkflowMixin(object):
    """
    We provide a simple editorial workflow (for django CMS) by assigning users
    to specific user groups and granting "Staff" status.  Those groups are created
    by the ``organice initauth`` management command after setting up the project.
    """

    def add_user_to_group(self, user, group_name=GUESTS_GROUP):
        """Give a user permissions to participate in managing content"""
        user.is_staff = True
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        return user


class AccountAdapter(EditorialWorkflowMixin, DefaultAccountAdapter):
    """
    Ensures that the CMS editorial workflow is activated for every new user
    signing up using email and password.
    """

    def save_user(self, request, user, form, commit=True):
        user = super(AccountAdapter, self).save_user(request, user, form, commit)
        user = self.add_user_to_group(user)
        if commit:
            user.save()
        return user

    def confirm_email(self, request, email_address):
        """
        Give superuser privileges automagically if the email address of a
        user confirming their email is listed in ``settings.ADMINS``.
        """
        super().confirm_email(request, email_address)

        if email_address.email in ADMIN_EMAIL_ADDRESSES:
            user = email_address.user
            user.is_staff = user.is_superuser = True
            user.save()

            messages.add_message(
                request, messages.INFO,
                _('Welcome Admin! You have been given superuser privileges. '
                  'Use them with caution.')
            )


class SocialAccountAdapter(EditorialWorkflowMixin, DefaultSocialAccountAdapter):
    """
    Ensures that the CMS editorial workflow is activated for every new user
    signing up using a social account.
    """

    def save_user(self, request, sociallogin, form=None):
        user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form)
        user = self.add_user_to_group(user)
        user.save()
        return user
