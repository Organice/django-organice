"""
South migrations for integrating Zinnia

1. Integration of django CMS EntryPlaceholder in Zinnia::
   Avoids having to run a schema migration manually after the first ``syncdb``::

    ./manage.py schemamigration zinnia --auto --update && ./manage.py migrate zinnia

   For description of generation see https://github.com/Fantomas42/django-blog-zinnia/issues/115::

    # in ``settings/common.py``
    SOUTH_MIGRATION_MODULES = {
        'zinnia': 'organice.migrations.zinnia',
    }
    # run initial migration without EntryPlaceholder activated in settings
    $ ./manage.py schemamigration zinnia --initial
    # activate EntryPlaceholder in settings and run
    $ ./manage.py schemamigration zinnia --auto entry_placeholder
"""
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        pass

    def backwards(self, orm):
        pass
