"""
Unit tests and test utilities for django Organice.

NOTE: Having an __init__ file in test directories is bad practice according to
py.test recommendations:
http://pytest.org/latest/goodpractises.html#choosing-a-test-layout-import-rules

However, this makes relative imports work in test modules (e.g. helper from ``utils.py``).
"""

# NOTE 1: This file makes the 'test' folder importable! (i.e. `import tests`) Not good.
#  Though, the test folder is pruned by MANIFEST.in, hence it's not installed anywhere.
# TODO: Consider inlining the tests into the package, or find a solution without relative imports.

# NOTE 2: The import of `DjangoSettingsManager` for probe_values_in_list() makes the
#  test.utils dependent on an installed version of Organice. Also tests are run with
#  helpers from the unit under test! No, not good.
# TODO: Make tests and test helpers independent from the implementation being tested.
