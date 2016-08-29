"""
Authentication adapters for Organice
"""
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group


class EditorialWorkflowMixin(object):
    """
    We provide a simple editorial workflow (for django CMS) by assigning users
    to specific user groups and give the "Staff" status.  Those groups are created
    by the ``organice initauth`` management command after setting up the project.
    Background reading:
    http://stackoverflow.com/questions/8806705/django-cms-and-editorial-workflows#answer-39128706
    """
    GUESTS_GROUP = 'Guests'
    EDITORS_GROUP = 'Editors'
    PUBLISHERS_GROUP = 'Publishers'

    def add_user_to_group(self, user, group_name=GUESTS_GROUP):
        """Give a user permissions to participate in managing content"""
        user.is_staff = True
        user.groups = [Group.objects.get(name=group_name)]
        return user


class AccountAdapter(EditorialWorkflowMixin, DefaultAccountAdapter):
    """
    Ensures that the CMS editorial workflow is activated for every new user.
    """

    def save_user(self, request, user, form, commit=True):
        user = super(AccountAdapter, self).save_user(request, user, form, commit)
        user = self.add_user_to_group(user)
        if commit:
            user.save()
        return user


class SocialAccountAdapter(EditorialWorkflowMixin, DefaultSocialAccountAdapter):
    """
    Ensures that the CMS editorial workflow is activated for every new user.
    """

    def save_user(self, request, sociallogin, form=None):
        user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form)
        user = self.add_user_to_group(user)
        user.save()
        return user
