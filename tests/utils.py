"""
Test helper functions
"""


def probe_values_in_tuple(content, tuple_key, required_values):
    """
    Tests a tuple for required values, extracting the tuple beforehand.
    :param content: content string containing the tuple attribute (e.g. Django settings)
    :param tuple_key: attribute name of the tuple
    :param required_values: list or tuple of values for testing the tuple
    :return: None (asserts in case of failure)
    """
    try:
        start_pos = content.find("%s = (\n" % tuple_key)
        assert start_pos != -1, "Tuple not found: %s" % tuple_key
        stop_pos = 1 + content.find("\n)\n", start_pos)
        assert stop_pos > start_pos, "End of tuple not found: %s" % tuple_key

        tuple = content[start_pos:stop_pos]
        for val in required_values:
            val_line = ("    '%s',\n" % val)
            assert val_line in tuple, "Not found in tuple %s: %s" % (tuple_key, val)
        return True
    except AssertionError as ae:
        print(ae.message)
        return False


def pytest_generate_tests(metafunc):
    """
    A test scenarios implementation for py.test, as found at
    http://pytest.org/latest/example/parametrize.html#a-quick-port-of-testscenarios
    Picks up a ``scenarios`` class variable to parametrize all test function calls.
    """
    idlist = []
    argvalues = []
    for scenario in metafunc.cls.scenarios:
        idlist.append(scenario[0])
        items = scenario[1].items()
        argnames = [x[0] for x in items]
        argvalues.append(([x[1] for x in items]))
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")
