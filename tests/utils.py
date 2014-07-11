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
        assert start_pos != -1
        stop_pos = 1 + content.find("\n)\n", start_pos)
        assert stop_pos > start_pos

        tuple = content[start_pos:stop_pos]
        for val in required_values:
            val_line = ("    '%s',\n" % val)
            assert val_line in tuple
        return True
    except AssertionError as ae:
        message = ae.args[0]
        start_pos = message.find("'")
        stop_pos = message.find(r',\n" in ')
        print("Not found in tuple: %s" % message[start_pos:stop_pos])
        return False
