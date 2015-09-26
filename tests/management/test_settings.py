import os
from organice.management.settings import DjangoModuleManager, DjangoSettingsManager


def test_create_module():
    """Create a module, and create a submodule (file) in it."""
    content = [
        '# this is a test module',
        'KITCHEN = "Veggie Surprises"',
        'CARROTS = 50',
    ]
    module = DjangoModuleManager('test_project_settings', 'kitchen')
    module.add_file('cook', lines=content)
    module.save_files()

    thefile = module.get_file('cook')
    thefile.seek(0)
    content = thefile.read()
    assert content.startswith(content[0])


def test_read_module():
    """Read a subodule (file) in an existing module."""
    module = DjangoModuleManager('test_project_settings', 'kitchen')
    module.add_file('cook')
    thefile = module.get_file('cook')
    content = module.get_data('cook')
    pathname = os.path.join('test_project_settings', 'kitchen', 'cook.py')
    thefile.seek(0)
    assert thefile.read() == content
    assert len(content) > 40, "Submodule file is too short! Something's wrong. '%s'" % content
    assert thefile.name == pathname


def test_create_settings():
    """Create a settings module with several submodules."""
    project = 'test_project_settings'
    modules = ('__init__', 'foo', 'bar', 'baz')

    settings = DjangoSettingsManager(project, *modules)
    for module in modules:
        thefile = settings.get_file(module)
        assert os.path.isfile(thefile.name), "File not created: %s" % thefile.name
