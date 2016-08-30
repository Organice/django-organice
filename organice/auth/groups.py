"""
Django groups used for permissions in Organice.

Groups for an editorial workflow.
See ``adapters.EditorialWorkflowMixin`` for explanations. Background reading:
http://stackoverflow.com/questions/8806705/django-cms-and-editorial-workflows#answer-39128706
"""

GUESTS_GROUP = 'Guests'
EDITORS_GROUP = 'Editors'
PUBLISHERS_GROUP = 'Publishers'
